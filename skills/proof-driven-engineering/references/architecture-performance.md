# Architecture and Performance

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

## Architecture before instruction-level tuning

Trace `workload -> critical path -> resource cost -> owner -> consumers`.
Use profiles, traces, query plans, runtime counters, or controlled experiments.
Consider a rival cause: CPU versus I/O, allocation versus contention, compute
versus serialization. Choose the measurement that separates them.

Evaluate in descending expected impact, adapting to measured evidence:

1. Avoid unnecessary work; improve algorithmic complexity and query/index design.
2. Reduce transfers, round trips, repeated scans, copies, and serialization.
3. Batch/vectorize compatible work; use suitable data layout and locality.
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

## Comparable measurement

Use the existing benchmark runner where suitable. Record source revisions/input
hashes, command, runtime/compiler flags, hardware, dataset/seed, sizes, units,
concurrency, and cold/warm state. Keep sensitive raw output in an approved private
location, never in public logs or artifacts. Publish concise reviewed findings.

Check equivalent outputs before comparing speed. Prevent dead-code elimination,
constant folding of artificial inputs, or measuring fixture construction instead
of the requested operation. Retain/consume benchmark results. Include realistic
boundaries and worst-case inputs when they can invalidate the choice.

Warm up JIT/cache paths when representative; measure cold paths separately when
they matter. Use repeated comparable runs and alternate order when drift matters.
Report sample count, central tendency, dispersion, and outliers. A tiny timing
difference inside observed variability is unresolved. Include warm-cache and
cold-cache costs, build time, allocations, and memory when relevant.

For tail claims, use enough samples and an appropriate load generator. Report
errors/timeouts alongside latency; dropped requests are not a speedup. Keep
offered versus achieved load explicit and avoid coordinated omission. A
microbenchmark does not establish end-to-end latency or capacity.

For lower-is-better measurements: speedup is `baseline / candidate`; percentage
reduction is `(baseline - candidate) / baseline * 100`. Preserve units and use
comparable nonzero values. Never extrapolate beyond measured conditions.

## Specialized mechanisms and their obligations

| Mechanism | Required challenge |
| --- | --- |
| Cache | tenant/permission key, invalidation, freshness, eviction, bounded memory, stampede, revocation |
| Parallelism | dependency/order semantics, cancellation, bounded concurrency, saturation, races |
| Pool/arena/zero-copy | lifetime, aliasing, initialization, ownership, retention, use-after-free |
| Native/SIMD/unsafe | target CPU/runtime support, fallback, alignment, bounds, UB, actual generated behavior |
| Numeric optimization | overflow, precision, rounding, NaN, determinism, contractual equivalence |
| Index/materialized state | source of truth, update cost, consistency, rebuild, storage, migration |
| Retry/asynchrony | idempotency, duplicate effects, deadline, retry budget, ordering, shutdown |

Benchmark authorized bounded workloads. Establish runtime/resource limits and a
stop condition before expensive load experiments. Stop a failed approach when
its evidence is decisive; pursue the next supported candidate. Recheck behavior,
negative cases, and end-to-end costs after optimization.
