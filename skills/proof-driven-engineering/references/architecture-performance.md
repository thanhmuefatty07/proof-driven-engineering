# Architecture and Performance

## Outcome-first system model

Begin with the user's intended result, observable acceptance, hard constraints,
and non-goals. Distinguish these from a proposed implementation. Implementation
freedom does not authorize changing the product, dropping a constraint, widening
external effects, or pursuing a preferred pattern instead of the outcome.

Build a compact project-level map from authoritative docs, entry points, manifests,
and relevant code: component responsibilities, dependency direction, data/source
of truth, public contracts, and trust, failure, and deployment boundaries. Then
trace the affected request/data path and its producers and consumers in depth.
Do not claim whole-project understanding from a local read; keep decision-relevant
unknowns explicit. Unaffected details need not be loaded file by file.

Turn the important quality attributes into scenarios: workload or failure stimulus,
environment, expected system response, and observable budget/invariant. Consider
performance alongside required security, availability, consistency, recovery,
compatibility, and resource limits. Resolve conflicting objectives explicitly.

For a consequential choice, compare the current or simplest sufficient design
with a credible alternative against those scenarios. Identify the evidence that
would reject the preferred choice, consequences for consumers, and migration or
rollback where needed. Select boundaries for domain/data ownership and actual
failure or scaling needs, not pattern names. Record a significant decision in an
existing architectural authority; do not create a diagram or ADR for every edit.

## Define the optimization problem

Name the actual outcome: throughput, latency at a stated percentile, CPU time,
peak memory, allocations, startup, energy, binary/bundle size, or cost. Record
units and which metrics are hard constraints. Establish workload size/distribution,
concurrency, platform/runtime, deployment, and data ownership. If no target is
given, infer the relevant metric from the request and disclose the assumption;
ask when different objectives would change the implementation.

Correctness, authorization, privacy, durability, and compatibility constrain the
feasible candidates. Within that set, prioritize the user's performance objective.
If faster CPU time causes unacceptable p99 latency or memory, it is not a win.
Multiple conflicting objectives require a stated trade-off rather than a hidden
weighted score. Report the fastest candidate tested for this workload; do not
claim a global optimum.

Keep the best feasible measured candidate, the alternatives tested, uncertainty,
and remaining limits explicit. Continue exploration only when a concrete supported
alternative or discriminating probe could materially improve the requested result.
Stop speculative tuning when no such next step remains; report the fastest tested
candidate, never that no better line or design could exist.

## Performance-aware generation

Apply cost reasoning during substantive feature design, not only after a request
to optimize existing code. Estimate input size/distribution, execution frequency,
algorithmic complexity, memory behavior, and the costs on the expected path.
Choose suitable structures and layouts; use the impact ladder below to avoid
needless allocations, copies, conversions, repeated work, synchronization, and
abstraction overhead where they matter. Cold paths do not need exhaustive tuning.

For confirmed performance-critical functionality, compare credible implementation
alternatives before finalizing the design. Use the current implementation as a
baseline when available; for new functionality, use a straightforward correct
candidate. Treat cost estimates as hypotheses, not measurements or speedup claims.

## Architecture before instruction-level tuning

Trace `workload -> critical path -> resource cost -> owner -> consumers`.
Use profiles, traces, query plans, runtime counters, or controlled experiments.
Perform systematic bottleneck triage using Brendan Gregg's **USE Method** (Systems
Performance, 2020) for every hardware/software resource (CPU, memory, storage I/O,
network, lock/synchronization):
- **Utilization:** % of time the resource was busy servicing active work.
- **Saturation:** Degree of queued work waiting for an overloaded resource.
- **Errors:** Count and rate of error events on that resource.

For request-driven architectures, complement USE with Tom Wilkie's **RED Method**:
- **Rate:** Requests serviced per second.
- **Errors:** Failed requests per second / error percentage.
- **Duration:** Latency distribution (median, p95, p99 percentiles).

Apply Jon Bentley's **Hierarchy of Optimization** (*Writing Efficient Programs*, 1982)
in descending order of expected leverage:
1. **System Architecture & Workload Elimination:** Eliminate unnecessary work;
   the fastest code is code that never executes.
2. **Algorithmic Asymptotics:** Reduce complexity class ($O(N^2) \to O(N \log N) \to O(N)$)
   and design efficient database/index queries.
3. **Data Layout & Memory Locality:** Improve spatial/temporal cache locality,
   pre-allocate contiguous buffers, and minimize garbage collection/allocator pressure.
4. **Code Tuning & Instruction Optimizations:** Unroll loops or tune compiler/native
   instructions only on confirmed hot paths after higher tiers are exhausted.

Apply the **Roofline Model** (Williams et al., CACM 2009): determine whether the
critical kernel is memory-bandwidth bound or arithmetic/compute bound. Optimizing
instructions on a memory-bandwidth-bound algorithm produces zero speedup; focus
instead on data compaction and cache reuse. On confirmed CPU/memory hot paths,
pair Roofline with **Top-Down Microarchitecture Analysis (TMAM)** and the full
mechanical-sympathy handbook in [systems-performance.md](systems-performance.md).

Evaluate in descending expected impact, adapting to measured evidence:

1. Avoid unnecessary work; improve algorithmic complexity and query/index design.
2. Reduce transfers, round trips, repeated scans, copies, and serialization.
3. Batch/vectorize compatible work; consider data-oriented layout and cache locality.
4. Bound allocation and retention; reuse storage only with clear ownership.
5. Address concurrency limits, lock contention, backpressure, and scheduling.
6. Tune compiler/runtime/native instructions only on a measured remaining hot path.

Every changed hot-path operation should serve the required semantics or a measured
cost reduction. Optimize a whole path before claiming that fewer lines or CPU
instructions improve the system. Inlining can increase instruction-cache pressure;
parallelism can add contention; pooling can retain memory; memoization can leak
tenant data. Inspect generated code only when the profiler makes it useful.

Choose boundaries around domain/data ownership and demonstrated failure/scaling
needs. Existing local modules are often sufficient. New services, queues, caches,
abstractions, languages, or dependencies need a concrete requirement or measured
gain, along with new failure modes, operational cost, migration, and recovery.
Allow substantial complexity when its verified benefit warrants it. Do not impose
an arbitrary file/line/agent-count limit that blocks a required result.

## Compiler and runtime decisions

On a confirmed hot path, inspect the actual execution environment only when the
result can change a consequential decision. Use version-matched documentation
and the [dependency/tool grounding rules](dependency-grounding.md); verify
optimization/build settings, runtime behavior, and target capabilities rather
than guessing flags.

Relevant probes may include optimization remarks, assembly/IR, inlining,
devirtualization, vectorization, JIT warmup/optimization/deoptimization, allocation
and GC behavior, or counters for cache misses, bandwidth, and branch behavior.
Choose the probe that tests the suspected bottleneck, not an exhaustive checklist.
Consider PGO, LTO, target-specific builds, SIMD/native code, memory reuse, or
parallel execution only as candidates with measured benefit and bounded costs.
Account for build/startup time and code size where relevant. Preserve required
portability, CPU-feature fallbacks, and defined numerical/concurrency semantics;
undefined behavior or unsafe shortcuts cannot justify a benchmark win.

## Comparable measurement

Use the existing benchmark runner where suitable. Record source revisions/input
hashes, command, runtime/compiler flags, hardware, dataset/seed, sizes, units,
concurrency, and cold/warm state. Keep sensitive raw output in an approved private
location, never in public logs or artifacts. Publish concise reviewed findings.
Use deployment-representative builds/settings and account for intentional
compiler/runtime differences; unrelated debug/release or instrumentation settings
must not masquerade as an implementation comparison.

Check equivalent outputs before comparing speed. Prevent dead-code elimination,
constant folding of artificial inputs, or measuring fixture construction instead
of the requested operation. Retain/consume benchmark results. Include realistic
boundaries and worst-case inputs when they can invalidate the choice.
Separate fixture/one-time setup from execution when that reflects real usage;
include construction, conversion, cleanup, and amortization costs actually paid
by the target path. Report what is included rather than silently moving costs.

Warm up JIT/cache paths when representative; measure cold paths separately when
they matter. Control environmental bias (Mytkowicz et al., ASPLOS 2009: thread
pinning, power/turbo governor, identical flags, identical workload sizes, and
memory-layout sensitivity). Use repeated interleaved A-B-A-B runs (`N >= 7` for
consequential claims). Report sample count, central tendency (median), dispersion
(IQR/MAD), outliers, and nonparametric confidence intervals (optionally validated
with [compare_bench.py](../scripts/compare_bench.py)). Do not accept a difference
indistinguishable from measurement noise as an optimization. Include warm-cache
and cold-cache costs, build time, allocations, and memory when relevant.

For tail claims, use enough samples and an open-loop load generator (fixed
scheduled arrival times `t_sched`, avoiding Gil Tene's coordinated omission).
Report errors/timeouts/drops alongside latency (`p50/p95/p99/p99.9/max`); dropped
requests are not a speedup. Keep offered versus achieved load explicit, and sweep
core counts against **Gunther's Universal Scalability Law (USL)** for concurrent
services. A microbenchmark does not establish end-to-end latency or capacity.
Prefer demonstrated end-to-end improvements over isolated microbenchmark wins.
Accept an optimization only when the relevant gain is established and its
correctness, security, stability, portability, and resource costs remain feasible.

For lower-is-better measurements: speedup is `baseline / candidate`; percentage
reduction is `(baseline - candidate) / baseline * 100`. Preserve units and use
comparable nonzero values. Never extrapolate beyond measured conditions.

## Specialized mechanisms and their obligations

| Mechanism | Required challenge |
| --- | --- |
| Cache | Complete mediation: tenant/user/permission cryptographic key binding, invalidation, freshness, eviction, bounded memory, stampede, revocation |
| Parallelism | dependency/order semantics, cancellation, bounded concurrency, saturation, races, USL multi-core scaling |
| Lock-free / Atomics / SeqLock | explicit Acquire/Release happens-before proof, weak memory model (ARM64/RISC-V) verification, 128B false-sharing isolation, ABA/reclamation, bounded reader retries, Miri/Loom/TSan |
| Pool/arena/zero-copy | lifetime, aliasing, initialization, ownership, NUMA first-touch, retention, use-after-free |
| Native/SIMD/unsafe | target CPU/runtime support, runtime CPUID dispatch + scalar fallback, AVX-512 frequency check, alignment, page-safe tails, UB, scalar differential oracle, generated assembly/IR |
| I/O / Storage / Kernel bypass | `fsync`/durability honesty, short reads/`EINTR`, alignment (`O_DIRECT`), `mmap` fault/TLB shootdowns, bounded backpressure |
| Numeric optimization | overflow, precision, rounding, NaN, determinism, hidden libcalls (`__muloti4`), contractual equivalence |
| Index/materialized state | source of truth, update cost, consistency, rebuild, storage, migration |
| Retry/asynchrony | idempotency, duplicate effects, deadline, retry budget, ordering, shutdown |

Benchmark authorized bounded workloads. Establish runtime/resource limits and a
stop condition before expensive load experiments. Stop a failed approach when
its evidence is decisive; pursue the next supported candidate. Recheck behavior,
compatibility, negative cases, and end-to-end costs after optimization.

## Primary references

- [Brendan Gregg: Systems Performance & USE Method](https://www.brendangregg.com/usemethod.html)
- [Jon Bentley: Writing Efficient Programs (1982)](https://dl.acm.org/doi/book/10.5555/578130)
- [Williams et al.: Roofline Model (CACM 2009)](https://dl.acm.org/doi/10.1145/1498765.1498785)
- [Extreme Systems Performance Engineering (TMAM, Memory, Lock-Free, SIMD, I/O, Stats)](systems-performance.md)
