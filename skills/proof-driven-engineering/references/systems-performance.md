# Extreme Systems Performance Engineering

Use this reference when designing, implementing, optimizing, or reviewing
hot paths, low-latency or high-throughput services, native code (Rust/C/C++/Zig),
lock-free concurrency, memory/cache-sensitive kernels, SIMD/vectorized code,
storage/network I/O engines, or runtime-critical boundaries. Every technique
below is conditional on workload physics and measured proof: never guess a
bottleneck or trade soundness, security, or durability for speed.

## 1. Top-Down Hardware & Roofline Triage

Before modifying code on a confirmed hot path, classify where CPU cycles and
memory transactions actually go using Ahmad Yasin's **Top-Down Microarchitecture
Analysis (TMAM)** alongside Gregg's USE/RED and Williams's Roofline Model:

| TMAM Slot | Hardware Counters / Probes | Primary Root Causes | First-Line Countermeasures | Traps to Avoid |
| --- | --- | --- | --- | --- |
| **Frontend Bound** | `perf stat --topdown`, `L1-icache-load-misses`, `iTLB-load-misses`, DSB/LSD stalls | Bloated hot loops, cold error/logging code inline, excessive inlining, virtual calls | `#[cold]`/`noinline` cold-path splitting, PGO/BOLT layout, deduplicate hot code, monomorphize hot dispatch | Blindly slapping `inline(always)` everywhere (blows L1 I-cache) |
| **Bad Speculation** | `branch-misses`, `machine_clears.*`, `perf annotate` | Unpredictable data-dependent branches (20%–80% taken), memory-ordering clears | Branchless `cmov`/masks/lookup tables, partition/sort by predicate, separate hot predictable cases | Making predictable branches (>95%/<5%) branchless (lengthens critical dependency chain) |
| **Backend: Memory Bound** | `L1-dcache-load-misses`, `LLC-load-misses`, `dTLB-load-misses`, `perf c2c` (HITM), bandwidth counters | AoS cache-line waste, pointer chasing, false sharing, working set > L2/L3, TLB thrash, 4K aliasing | SoA/AoSoA, hot/cold splitting, flat arena indices, 128B false-sharing alignment, huge pages, prefetch, NT stores | Instruction micro-tuning on a memory-bandwidth-bound kernel (zero speedup under Roofline) |
| **Backend: Core Bound** | Low IPC with low cache/branch misses, `llvm-mca`, disassembly | Long loop-carried dependency chains, port saturation, integer division (`div`), hidden libcalls | Multiple independent accumulators for ILP, SIMD/SWAR, power-of-2 mask / Barrett-Lemire fast div, eliminate hidden libcalls | Ignoring generated assembly/IR when assuming LLVM auto-vectorized or inlined |

Verify whether the hot kernel is **latency-bound** (pointer chasing, cross-core
bounces), **memory-bandwidth-bound** (streaming large working sets with low
arithmetic intensity), or **compute-bound** (high arithmetic intensity saturating
execution ports). Never optimize ALU ops on a bandwidth-bound kernel; compact
data, eliminate copies, or fuse passes to cut bytes transferred instead.

## 2. Data-Oriented Layout, Cache Hierarchy & NUMA Physics

Hardware memory latency spans two orders of magnitude (L1 ~1 ns, L2 ~3–5 ns,
L3 ~10–20 ns, cross-core HITM ~40–100+ ns, local DRAM ~60–100 ns, remote NUMA
DRAM ~120–300+ ns). Design data structures around cache lines first:

- **SoA / AoSoA over AoS for scans & filters:** Never stream 80–256B structs
  when a hot loop touches 8–16B per element. Split hot numeric columns into
  contiguous arrays (`SoA`) or fixed-width cache-line blocks (`AoSoA`) so every
  fetched 64B cache line carries 100% hot payload and feeds contiguous SIMD loads.
- **Hot/Cold Struct Splitting & Alignment Packing:** Move cold metadata (`String`,
  audit fields, error details) to cold side-tables or arena handles. Order struct
  fields by descending alignment (`u64`/`i64` -> `u32` -> `u16` -> `u8`) to
  eliminate silent padding waste; enforce tight sizes with compile-time
  `assert!(size_of::<T>() == ...)` / `static_assert`.
- **Eliminate Pointer Chasing:** Replace linked lists, red-black trees, boxed
  trait objects, and per-node heap allocations with contiguous flat arrays,
  arena-indexed 32-bit handles (halving pointer footprint vs 64-bit pointers),
  open-addressing / SwissTable / Robin Hood hash tables, B-trees / B+trees sized
  to cache lines, or CSR/CSC compressed sparse layouts.
- **False-Sharing Elimination (`128B` Coherency Boundary):** Isolate independently
  mutated cross-core atomics, producer/consumer indices, and reader-polled vs
  writer-mutated hot slots with `#[repr(align(128))]` / `alignas(128)`. 128-byte
  isolation covers both 64B x86-64 lines with Intel adjacent-line spatial
  prefetcher pairs and native 128B ARM64/Apple Silicon cache lines. Verify zero
  unexpected cross-core HITM contention with `perf c2c` where available.
- **Conflict Misses, 4K Aliasing & TLB Pressure:** Avoid power-of-2 matrix/ring
  strides that thrash identical cache sets or trigger 4K store-to-load aliasing
  stalls. When working sets exceed L1/L2 dTLB reach, measure 2MB/1GB explicit
  huge pages (`MAP_HUGETLB` / `Large Pages`) — and explicitly measure Transparent
  Huge Pages (THP) compaction/defrag tail-latency spikes before enabling THP on
  latency-critical services.
- **Hardware vs Software Prefetch & Non-Temporal Stores:** Sequential and
  fixed-stride scans engage hardware stream/stride prefetchers automatically.
  Add explicit software prefetch (`_mm_prefetch` / `__builtin_prefetch`) ONLY for
  irregular pointer/hash/index gathers with measured prefetch distance
  `ceil(memory_latency_cycles / iter_cycles)`. Use non-temporal streaming stores
  (`movnt*` / `_mm_stream_*`) ONLY for write-only output buffers exceeding L3
  cache to bypass Read-For-Ownership (RFO) cache pollution; follow with `sfence`
  when required by ordering rules.
- **NUMA First-Touch & Core Placement:** Allocate, zero, and prefault
  (`mlockall` + page-touch) hot arenas, rings, and tables **on the pinned owning
  thread/NUMA node** (OS first-touch page placement), not on an arbitrary startup
  thread. Pin latency-critical threads to isolated physical cores (`isolcpus` /
  `nohz_full` / affinity masks) on the same NUMA socket without SMT sibling
  contention where deployment permits.

## 3. Zero-Allocation, Zero-Copy & Deterministic Memory

- **Zero Heap Allocation & Hidden Refcount Traffic on Hot Paths:** No
  `malloc`/`new`/`Box`/`String`/`Vec` growth, `format!`, GC object churn, or
  atomic refcount copies (`Arc::clone`, `std::shared_ptr` pass-by-value) inside
  hot loops; borrow `&T` or split field borrows instead. Pre-allocate bounded
  working sets upfront (static allocation: deterministic upper memory bound,
  zero mid-flight OOM or allocator-lock tail spikes).
- **Lifetime-Matched Custom Allocators:**
  - *Arena / Bump / Region:* O(1) pointer bump, O(1) bulk reset per request/batch/frame.
  - *Slab / Pool / Intrusive Freelist:* O(1) fixed-size alloc/free, zero fragmentation.
  - *Small Buffer Optimization (SBO / SSO):* Inline stack storage for common small payloads.
  - When general heap allocation cannot be eliminated, keep allocations thread-local
    and compare `jemalloc`/`mimalloc`/`tcmalloc` empirically on the real workload.
- **Zero-Copy Pipelines & Compact Representations:** Pass non-owning slices/views
  (`&[u8]`, `std::span`, `memoryview`, `ReadOnlySpan<T>`). Parse directly in-place
  over wire/storage buffers instead of decode -> DOM/AST -> re-encode copies.
  Use scatter-gather vectored I/O (`readv`/`writev`), `splice`/`sendfile`,
  bit-packing, prefix/delta/dictionary/RLE columnar encodings, string/symbol
  interning (dense integer IDs on the hot path, strings strictly on the cold
  control path), and SWAR (SIMD Within A Register) for delimiter/ASCII scans.
- **Managed & Interpreted Runtimes (Python, JVM, Go, JS/TS, .NET):** Enforce
  escape-analysis stack promotion (`go build -gcflags='-m'`, JVM escape checks),
  avoid boxing/closures/megamorphic inline caches in hot loops, batch work across
  FFI boundaries into vectorized native kernels (NumPy/Arrow/C/Rust) accounting
  for marshaling overhead, and never block async event loops or hold the GIL
  across heavy compute/sync I/O.

## 4. Lock-Free Concurrency, Memory Models & Shared-Nothing Scaling

Eliminate contention architecturally before micro-tuning locks:

1. **Synchronization Cost Ladder (Pick the Cheapest Sound Primitive):**
   `Thread-local / Shared-Nothing (Thread-per-Core, Single-Writer)` ->
   `Immutable / Epoch-Published Snapshot` ->
   `Boehm UB-Free Atomic SeqLock (single-writer, bounded reader retries)` ->
   `Cache-Padded SPSC Ring (local shadow head/tail, batched commits)` ->
   `Bounded Vyukov MPSC/MPMC Ring` ->
   `Sharded / Striped Locks (watch Zipfian hot-key collapse!)` ->
   `RWLock / RCU` -> `Coarse Mutex (cold paths only)`.
2. **Thread-Per-Core & Single-Writer Architecture:** Partition mutable state by
   shard/core so each partition has exactly one writer (zero lock/CAS contention,
   warm L1/L2 cache). Connect cores with bounded cache-padded SPSC rings using
   local shadow indices (`cached_head`/`cached_tail`) so cross-core atomic loads
   happen only when the local shadow indicates full or empty, and batch consumer
   head commits (bounded `BATCH_LIMIT` so bursty producers cannot starve siblings
   or violate tail latency). Keep cross-thread flags (e.g., `shutdown`) off the
   per-item hot path whenever possible (check on full/empty/batch boundaries).
3. **Formal Memory-Model Discipline (Boehm & Adve, PLDI 2008):**
   - There are **no "benign" data races** in C/C++/Rust: every concurrent
     unsynchronized access where at least one is a write is immediate UB.
   - Document and prove the exact **`synchronizes-with` / `happens-before` edge**
     for every atomic operation.
   - Use `Relaxed` ONLY for single-owner loads, independent telemetry counters,
     or payloads bracketed by verified `Acquire`/`Release` fences (e.g., Boehm
     atomic SeqLock where ALL payload fields are `Atomic*`, never plain non-atomic
     reads!). Never use bare `Relaxed` to publish or reclaim buffer slots.
   - Use `Acquire`/`Release` pairs for publication and slot reclamation; reserve
     `SeqCst` for algorithms genuinely requiring a single global modification
     order (on ARM64/RISC-V, `SeqCst` emits costly full barriers).
   - Encode single-producer / single-consumer / single-writer exclusivity in the
     type system (`&mut self`, `!Sync`, `!Clone`, `UnsafeCell<MaybeUninit<T>>`,
     panic-safe `Drop` commit guards) so safe callers cannot trigger UB.
   - **x86-64 TSO vs ARM64/RISC-V Weak Memory Trap:** Passing all unit tests on
     x86-64 CI proves NOTHING about weak-memory ordering. Missing `Acquire`/`Release`
     barriers pass x86-64 TSO and silently corrupt state on ARM64/RISC-V or after
     LLVM instruction reordering. Verify via Loom / CDSChecker / GenMC / TSan /
     ARM64 stress tests, or mark weak-memory correctness `NOT VERIFIED`.
4. **Reclamation, Progress & Bounded Backpressure:**
   - Guard lock-free linked/dynamic structures against ABA and use-after-free
     via version-tagged pointers, Epoch-Based Reclamation (EBR), Hazard Pointers,
     or QSBR.
   - Bound every retry loop (e.g., `MAX_SEQLOCK_RETRIES` returning `Err(Contended)`
     to prevent reader livelock under 100% hot-key write storms).
   - In short spin-waits, emit CPU pause hints (`spin_loop()` / `_mm_pause()` /
     `yield`) to avoid memory-order pipeline nukes and power burn; use bounded
     spin-then-park where cores are shared to prevent priority inversion.
   - Enforce **Little's Law (`L = lambda * W`)** bounded queues with explicit
     backpressure (`Result<(), T>` ownership return, shed with explicit drop
     counter, or bounded wait) — never unbounded queues or silent drops.

## 5. Vectorization, SIMD, Branching & Instruction-Level Parallelism

- **Columnar / Batch Vectorized Execution (MonetDB/X100):** Process contiguous
  batches sized to L1/L2 cache (typically 256–4096 elements) rather than
  item-at-a-time virtual dispatch or per-item atomic publication. Amortize
  control flow, bounds checks, and synchronization over the batch.
- **Auto-Vectorization First, Verified by Compiler Remarks:** Inspect compiler
  vectorization diagnostics (`-Rpass=loop-vectorize`, `-Rpass-missed=loop-vectorize`,
  `-fopt-info-vec-missed`) or disassembly. Eliminate silent vectorization killers:
  pointer aliasing (`restrict` / `&mut` / slicing with identical length proofs),
  loop-carried dependencies, mixed integer widths, hidden panic/bounds branches,
  and dynamic dispatch.
- **Instruction-Level Parallelism (ILP) & Strength Reduction:** Break loop-carried
  dependency chains using 2–4 independent accumulators matched to target ALU/FMA
  latency × throughput. Replace runtime modulo/division (`% N`) on hot paths with
  compile-time power-of-two bitmasks (`idx & (N - 1)`) or Barrett/Lemire
  multiply-shift reciprocals.
- **Branch Prediction vs Branchless Trade-Off:** Keep predictable branches
  (<5% or >95% taken) as branches (splitting cold error paths with `#[cold]` /
  `unlikely`). Convert unpredictable data-dependent branches (20%–80%) to
  branchless `cmov`/bitmasks/SIMD blends ONLY when verified to reduce total cycles
  (not merely `branch-misses` while regressing IPC via long data dependencies).
- **Explicit SIMD & Portability Contract (SSE4.2 / AVX2 / AVX-512 / NEON / SVE):**
  - Gate target-specific SIMD behind runtime feature detection (`is_x86_feature_detected!`,
    CPUID/HWCAP dispatch table, `ifunc`) with a verified scalar fallback.
  - NEVER ship `-C target-cpu=native` / `-march=native` to heterogeneous fleets
    without explicit fleet ISA homogeneity (`SIGILL` crash hazard).
  - Benchmark whole-application throughput when enabling AVX-512/heavy AVX2 to
    detect CPU frequency downclocking penalties.
  - Handle vector tails cleanly (masked ops, scalar epilogue, or proven-in-bounds
    overlapping tail load) — NEVER read past a buffer end across a 4KB page boundary.

## 6. High-Performance I/O, Syscalls & Honest Durability

- **Amortize Syscalls & Context Switches:** Batch I/O submissions and completions
  via `io_uring` (ring batching, `IORING_REGISTER_BUFFERS`, fixed files, SQPOLL
  only when core budget justifies it), `epoll`/`kqueue`/`IOCP` batching,
  `recvmmsg`/`sendmmsg`, and vectored `readv`/`writev`. Handle partial reads/writes
  and `EINTR` explicitly.
- **Storage, Page Cache & `mmap` Trade-Offs:** Use `O_DIRECT` with sector-aligned
  buffers + explicit user-space page cache when OS page-cache double-buffering or
  dirty-writeback stalls break tail latency. Before choosing `mmap` on latency-critical
  paths, account for blocking major page faults (stalling the entire thread/executor),
  `munmap` cross-core TLB shootdowns, and `SIGBUS` I/O error handling.
- **Honest Durability:** Accelerate durable writes through group commit,
  sequential append-only WAL batching, and hardware-accelerated CRC32C checksums.
  NEVER manufacture a benchmark win by silently removing `fsync`/`fdatasync`,
  disabling checksums, or weakening durability/crash-recovery contracts.
- **Kernel Bypass (DPDK / AF_XDP / RDMA):** Adopt only when measured kernel
  network stack overhead dominates end-to-end latency/throughput and dedicated
  NIC/core ownership plus operational complexity are explicitly authorized.

## 7. Compiler, Codegen & Zero-UB Mastery

- **Zero Abstraction Tax on Hot Loops:** Use static dispatch (generics,
  monomorphization, CRTP, closed enum dispatch) instead of `&dyn Trait` / virtual
  calls per item. Annotate error/overflow/slow paths `#[cold]` /
  `__attribute__((cold, noinline))` to preserve L1 I-cache density and avoid
  register spills on the hot path.
- **Inspect Generated Assembly / IR on Confirmed Hot Paths:** Audit critical loops
  (`objdump`, `cargo-asm`, `-S`, `llvm-mca`, `perf annotate`) specifically for:
  - Hidden compiler-rt/runtime libcalls (e.g., `i128::checked_mul` emitting
    `call __muloti4` when domain bounds like `i64 * u64` mathematically fit in
    `i128` without overflow, soft-float/128-bit division, `memcpy` vs inline).
  - Unhoisted loads/stores caused by pointer aliasing, accidental atomic
    refcount churn (`Arc::clone` / `shared_ptr`), or repeated shared-atomic
    reads inside inner loops.
  - Surviving bounds-check panics inside tight loops (hoist length proofs via
    iterators, `chunks_exact`, or checked slice sub-ranges outside the loop).
  - Unexpected register spills or heap allocations/escapes.
- **Build & Link Pipeline Candidates:** Benchmark ThinLTO/Full LTO, PGO, BOLT,
  `codegen-units=1`, and approved fleet ISA targets against an identical baseline;
  record build-time, binary-size, and startup-time costs alongside runtime gain.
- **Zero-UB Strict Contract:**
  - Never cast unaligned byte pointers (`*(ptr as *const u64)` is immediate UB);
    use `from_le_bytes` / `from_be_bytes` / `memcpy`, which compile to a single
    unaligned load instruction with explicit wire endianness and zero UB.
  - Respect strict aliasing / Stacked & Tree Borrows (`UnsafeCell` for interior
    mutability behind shared references), explicit integer overflow semantics
    (checked/widened/saturating/wrapping per contract — never silent wraparound
    on financial/size/offset math), and strict bounds checks on all external inputs.

## 8. Anti-Illusion Benchmarking & Statistical Proof

Follow Mytkowicz et al. (ASPLOS 2009), Gil Tene (Coordinated Omission), and
Neil Gunther's Universal Scalability Law (USL):

- **Control & Record Environment Bias:** Pin benchmark threads to distinct
  isolated physical cores on one NUMA node; record git SHA, compiler/runtime
  version, exact build flags (identical between baseline and candidate unless the
  flag itself is the tested variable), CPU model, governor/turbo state, memory
  layout/ASLR sensitivity, dataset size, key distribution (uniform + realistic
  Zipfian skew + 100% hot-key worst case), and RNG seed.
- **Zero Measurement Illusions:**
  - Assert **bit-exact / contract-equivalent output** between baseline and
    candidate before timing; route outputs through `std::hint::black_box` /
    `DoNotOptimize` / checksum sinks to defeat Dead-Code Elimination (DCE) and
    constant folding.
  - Measure and report the **clock read overhead itself**; never hammer `Instant::now()`
    or syscalls in a nanosecond spin loop without verifying vDSO / calibrated
    invariant-TSC cost.
  - Use **identical workload sizes** for baseline and candidate; separate cold-cache
    and warm-cache phases; discard warmup before recording samples.
- **Open-Loop Tail Latency (Zero Coordinated Omission):** Never report p99/p99.9
  from a closed-loop tight loop or from `elapsed / N` division. Pace arrivals on
  a fixed open-loop schedule (`t_sched = t_start + i * interval`), measure
  end-to-end latency from `t_sched` (not post-backpressure `t_enqueue`) into
  pre-allocated zero-alloc histograms, and always report **offered rate**,
  **achieved rate**, **drop/backpressure counts**, and `p50/p95/p99/p99.9/max`.
- **Statistical Decision Gate:** Run repeated **interleaved A-B-A-B trials**
  (`N >= 7` paired samples for consequential claims; minimum 3 for quick local
  probes). Report sample count, median, IQR/MAD, and nonparametric confidence
  intervals (bootstrap 95% CI + Cliff's delta / Mann-Whitney U). Optionally run
  [compare_bench.py](../scripts/compare_bench.py) on recorded sample JSON:
  ```sh
  python /path/to/skill/scripts/compare_bench.py /path/to/local/bench.json
  ```
  Reject any "speedup" whose 95% CI crosses `1.0` or sits inside the observed
  noise floor.
- **Multi-Core Scalability Proof (Amdahl & Gunther USL):** For concurrent systems,
  sweep core counts (`1, 2, 4, ...`) to verify throughput scaling and detect
  retrograde scaling caused by coherency (`beta`) or serialization (`alpha`).

## 9. Differential Oracles, Sanitizers & Deterministic Verification

- **Mandatory Scalar Reference Differential Oracle:** Pair every SIMD, branchless,
  SWAR, lock-free, custom-index, or zero-copy implementation with a simple,
  obviously-correct scalar reference oracle. Fuzz/property-test equivalence across:
  lengths `0, 1, 2, ..., W-1, W, W+1` (vector width `W`), unaligned offsets
  `+1..+63`, page boundaries (`4095, 4096, 4097`), numeric extrema (`INT_MIN`,
  `INT_MAX`, `u32::MAX`, `u64::MAX`, `NaN`, `-0.0`, `Inf`), duplicates,
  out-of-order sequences, and adversarial skew.
- **Systems Verification Toolchain Gate:** Run the applicable tools available in
  the environment and explicitly mark unavailable tools `NOT VERIFIED - reason`:
  - Memory/UB safety: `Miri` (Stacked/Tree Borrows, provenance, leaks), `ASan`,
    `UBSan`, `MSan`.
  - Concurrency & weak memory models: `Loom` / `CDSChecker` / `GenMC`, `TSan`,
    and multi-threaded torn-read stress tests under core oversubscription (and on
    ARM64/weak-memory hardware when targeting cross-arch deployments).
  - Fault & state-machine resilience: fuzzing (`cargo-fuzz`/`libFuzzer`/Hypothesis)
    and Deterministic Simulation Testing (DST) with injected partial I/O, crashes,
    full-ring backpressure, and panics inside callbacks.

## 10. Extreme Systems Rationalization Counters

| Rationalization / Red Flag | Reality & Required Action |
| --- | --- |
| "All unit tests pass on x86-64 CI, so our lock-free code is sound." | x86-64 TSO masks missing `Acquire`/`Release` barriers and unaligned/aliasing UB; verify with Miri + Loom/TSan + ARM64 or report `NOT VERIFIED`. |
| "Keep Mutex/HashMap/dyn Fn for readability; don't over-engineer." | When the workload violates latency/throughput budgets, measured feasibility outranks brevity; benchmark naive baseline as falsifier, then build the fastest sound design. |
| "Our microbenchmark shows 12x speedup and p99 = 110ns from `elapsed / N`." | Unconsumed outputs (DCE), single unpinned runs, mismatched workloads, and closed-loop averages are illusions; require black-box equivalence, open-loop `t_sched` histograms, and interleaved statistical CI. |
| "Just add `-C target-cpu=native` and cast `*const u64` for zero overhead." | Causes `SIGILL` fleet crashes and immediate alignment/endianness UB; use `from_le_bytes`/`memcpy` + runtime CPUID dispatch with scalar fallback. |
| "Use `i128::checked_mul` / bounds checks everywhere on the hot loop just in case." | Audit generated assembly/IR for hidden runtime libcalls (`__muloti4`) and unhoisted checks; prove mathematical/slice bounds at loop entry so safety costs zero hot-path cycles. |
| "Optimize instructions first; we can fix memory layout later." | On a memory-bandwidth or cache-miss-bound kernel (TMAM/Roofline), instruction tuning yields ~0% gain; fix data layout, allocations, and false sharing first. |
| "Drop `fsync` or silently drop full-ring events to hit the throughput target." | Dropped work or broken durability/security is contract corruption, not speedup; preserve Complete Mediation, durability, and explicit lossless/counted backpressure. |

## Primary references

- [Yasin: Top-Down Microarchitecture Analysis Method (ISPASS 2014)](https://doi.org/10.1109/ISPASS.2014.6844459)
- [Drepper: What Every Programmer Should Know About Memory (2007)](https://www.akkadia.org/drepper/cpumemory.pdf)
- [Boehm & Adve: Foundations of the C++ Concurrency Memory Model (PLDI 2008)](https://doi.org/10.1145/1375581.1375591)
- [Mytkowicz et al.: Producing Wrong Data Without Doing Anything Obviously Wrong (ASPLOS 2009)](https://doi.org/10.1145/1508244.1508275)
- [Gil Tene: HdrHistogram & Coordinated Omission](https://github.com/HdrHistogram/HdrHistogram)
- [Gunther: Universal Scalability Law (arXiv:0808.1431)](https://arxiv.org/abs/0808.1431)
- [McKenney: Is Parallel Programming Hard, And, If So, What Can You Do About It?](https://www.kernel.org/pub/linux/kernel/people/paulmck/perfbook/perfbook.html)
- [Langdale & Lemire: Parsing Gigabytes of JSON per Second (VLDB Journal 2019)](https://doi.org/10.1007/s00778-019-00578-5)
- [Boncz, Zukowski & Nes: MonetDB/X100 Hyper-Pipelining Query Execution (CIDR 2005)](http://cidrdb.org/cidr2005/papers/P19.pdf)
- [Axboe: Efficient IO with io_uring (2019)](https://kernel.dk/io_uring.pdf)
- [Bakhvalov: Performance Analysis and Tuning on Modern CPUs](https://book.easyperf.net/perf_book)
- [Agner Fog: Software Optimization Resources](https://www.agner.org/optimize/)
- [TigerBeetle: TIGER_STYLE Engineering Discipline](https://github.com/tigerbeetle/tigerbeetle/blob/main/docs/TIGER_STYLE.md)
