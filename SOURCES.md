# Research and Design Decisions

Initial review on 2026-10-07. Sources were selected for a concrete mechanism, inspectable
primary material, applicability, and evaluability. This is a scoped comparison,
not a ranking of the world's best skills. Popularity was used only for discovery.

| Primary source | Mechanism used in this project | Boundary |
| --- | --- | --- |
| [OpenAI skill documentation](https://learn.chatgpt.com/docs/build-skills) | Portable manifest, precise trigger, progressive loading, local discovery | Discovery is not guaranteed compliance |
| [OpenAI skill eval guidance](https://developers.openai.com/blog/eval-skills) | Observable outcome/process criteria and consuming-agent evaluation | Manifest tests alone cannot assess behavior |
| [OpenAI instruction/context guidance](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra) | Compact scope and conditional references | More instruction text is not evidence of higher quality |
| [Superpowers debugging](https://github.com/obra/superpowers/blob/8ca22dba9a94f28898bbce59f2537ff4d87c747d/skills/systematic-debugging/SKILL.md) | Reproduction, causal investigation, discriminating experiments | Avoid rigid ritual for low-impact work or printing sensitive diagnostics |
| [Anthropic skill creator](https://github.com/anthropics/skills/blob/683bc88e56f3e09ba94f7055977f3d3aa499f202/skills/skill-creator/SKILL.md) | Realistic test prompts, independent execution, iterative evaluation | Host-specific tools/procedures are not copied |
| [Trail of Bits differential review](https://github.com/trailofbits/skills/blob/82fe8226252622fa807643bdca1710901198553a/plugins/differential-review/skills/differential-review/SKILL.md) | Risk, callers, contract impact, concrete adversarial findings | No mandatory public audit dump or automatic high severity |
| [Trail of Bits sharp edges](https://github.com/trailofbits/skills/blob/82fe8226252622fa807643bdca1710901198553a/plugins/sharp-edges/skills/sharp-edges/SKILL.md) | Misuse-resistant defaults and boundary invariants | Do not force incompatible migrations without a safe path |
| [Vercel performance skills](https://github.com/vercel-labs/agent-skills/blob/063bee94c3f4df8453406c830b0a7df0f2860278/skills/react-best-practices/SKILL.md) | Prioritize high-impact costs before small instruction-level changes | React-specific recommendations remain domain-specific |
| [OWASP ASVS](https://owasp.org/projects/asvs) | Applicable security requirements become explicit controls/tests | No implied ASVS certification; record versions for conformance claims |
| [NIST SSDF](https://csrc.nist.gov/projects/ssdf) | Secure development and response grounded in risk and outcomes | This skill is not an organizational compliance program |
| [USENIX package-hallucination research, authors' summary](https://www.usenix.org/publications/loginonline/we-have-package-you-comprehensive-analysis-package-hallucinations-code) | Explicit checks against invented dependency names and their supply-chain consequences | Historical model observations do not predict this skill's failure rate |
| [PyPA distribution/import distinction](https://packaging.python.org/en/latest/discussions/distribution-package-vs-import-package/) | Verify installation-name to import-name mapping; do not install by guessed import | Python naming rules are not imposed on other ecosystems |
| [pip secure installs](https://pip.pypa.io/en/stable/topics/secure-installs/) | Inspect execution/integrity risks before installation; preserve approved hash controls | Artifact integrity does not prove benign behavior; flags depend on the actual tool version |
| [pip index-source warning](https://pip.pypa.io/en/stable/cli/pip_install/#cmdoption-extra-index-url) | Treat private/public index substitution as a dependency-confusion boundary | No automatic registry rewrites |
| [npm lockfile reference, v11](https://docs.npmjs.com/cli/v11/configuring-npm/package-lock-json/) | Check resolved artifact identity, version, integrity, and installation-script metadata | npm-specific fields require the matching CLI/lockfile format |
| [Python hashlib reference, 3.11](https://docs.python.org/3.11/library/hashlib.html) | Version-matched API and digest behavior for the synthetic grounding eval | The local runtime must still be inspected; later patch-level docs are not exact-binary evidence |
| [Google Testing Blog: Keep Tests Focused (2018)](https://testing.googleblog.com/2018/06/testing-on-toilet-keep-tests-focused.html) | Give each independently failing scenario a clear assertion and name | Multi-step integration journeys can still form one scenario |

## Chosen approach

The 0.4.0 test lifecycle sources below were reviewed on 2026-10-16. The update uses the official
[pytest temporary-directory guide](https://docs.pytest.org/en/stable/how-to/tmp_path.html)
and [fixture teardown guide](https://docs.pytest.org/en/stable/how-to/fixtures.html#teardown-cleanup-aka-fixture-finalization).
They inform ownership, retention and teardown decisions, including the danger of
reusing an explicit base temporary directory. Actual runner versions and cleanup
behavior must still be verified. Mutation guidance reviewed for 0.4.2 treats
mutation runs as targeted sensitivity checks, not stand-alone acceptance scores;
mutants that are equivalent, redundant, or disconnected from observable behavior
must not drive brittle test additions. The sources describe practical heuristics,
not guarantees that agents will follow them. The
[official Codex instruction guide](https://developers.openai.com/codex/guides/agents-md)
informs optional host integration; editing a skill does not itself change global
instructions or enforce a filesystem quota.

Keep one performance-first engineering workflow with specialized references.
Performance is optimized among candidates that preserve required correctness,
security, compatibility, and resources. Complexity is allowed when its benefit
is demonstrated; it is never the objective itself. A per-line aesthetic cannot
substitute for the behavior and cost of the complete path.

A broad always-loaded constitution was considered but would repeat host/project
policies and unrelated details. A bundle of many mandatory skills was considered
but would depend on host discovery and add conflicting process rules. This
project instead keeps one portable entry point, optional mechanical evidence
validation, and explicit project integration.

## Outcome and execution policy, 0.5.0

Reviewed on 2026-10-18 using Exa discovery followed by the primary pages below
and the OpenAI skill-evaluation source already listed above. These are decision
inputs, not copied instructions or comparative skill scores.

| Primary source | Applied mechanism | Boundary |
| --- | --- | --- |
| [SEI software architecture](https://www.sei.cmu.edu/software-architecture/) | Relate system structure and quality attributes to the user's outcome before implementation | Use a task-sized system model, not a mandatory heavyweight architecture exercise |
| [Google code review standard](https://google.github.io/eng-practices/review/reviewer/standard.html) | Evidence over preferences; resolve review deadlock rather than pursue unattainable perfection | Google does not prescribe this skill's three-round cap |
| [Google review scope](https://google.github.io/eng-practices/review/reviewer/looking-for.html) | Inspect design, behavior, concurrency and whether test assertions reject broken code | A checklist or clean scan alone is not correctness evidence |
| [Anthropic effective agents](https://www.anthropic.com/engineering/building-effective-agents) | Match decomposition and tools to the task; use environmental feedback and stopping criteria | The engineering patterns are not evidence for current SDK flags, host permissions, or automatic performance gains |
| [Google mutation testing](https://testing.googleblog.com/2021/04/mutation-testing.html) | Challenge material assertions with relevant wrong behavior rather than generate redundant mutants | No mandatory mutation-score target or exhaustive mutant matrix |
| [Google test fidelity](https://testing.googleblog.com/2024/02/increase-test-fidelity-by-avoiding-mocks.html) | Prefer the smallest real boundary that supports the claim; disclose substitutes | This does not authorize production calls or prohibit controlled failure doubles |

The maximum of three coordinated review rounds and the default prohibition on
generated explanatory code comments are explicit user policy choices, not claims
that these sources require them. Required legal/functional/contract content and
higher-priority instructions remain intact. Exhausted review budgets with
unresolved blockers require handoff, not approval. Existing local 0.4.5 guidance
on test portfolios, runtime selection, targeted mutation, and evidence authenticity
is retained. The update makes no claim of globally optimal lines, exhaustive
diagnosis, or guaranteed model compliance.

## Empirical research and reasoning upgrade sources

The following primary sources inform the research-backed upgrade across planning,
hypothesis-driven debugging, self-verification, dependency grounding, mutation testing,
performance triage, security mediation, and context preservation.

| Primary source | Applied mechanism | Boundary |
| --- | --- | --- |
| [Language Agent Tree Search (LATS)](https://arxiv.org/abs/2310.04406) | Tree-search planning with deliberate backtracking and external environment value functions | MCTS search trees are budgeted for consequential decisions, not low-impact single-line edits |
| [Limits of Intrinsic Self-Correction in LLMs](https://arxiv.org/abs/2310.01798) | Require extrinsic execution feedback (compilers, test runners, linters); prohibit purely introspective verbal self-correction | External feedback availability depends on tooling; unavailable checks remain NOT VERIFIED |
| [Reflexion: Verbal Reinforcement Learning](https://arxiv.org/abs/2303.11366) | Verbal reflection over concrete external execution failures stored in task memory to prevent cyclic errors | Reflections must cite observable tool receipts, not internal confidence |
| [Agentless: Hierarchical Localization](https://arxiv.org/abs/2407.01489) | Hierarchical localization pipeline (Repo -> File -> Function -> Invariant) before code modification | Does not eliminate the need for cross-component integration verification |
| [Why Programs Fail: Systematic Debugging](https://www.whyprogramsfail.com/) | Infection chain discipline (Defect -> Infection -> Failure) and minimal delta reproducer | A minimal reproducer does not prove absence of other defect modes |
| [Chain-of-Verification (CoVe)](https://arxiv.org/abs/2309.11495) | Factored verification: generate independent, isolated verification questions to eliminate confirmation bias | Independent questions must target authoritative docs/runtime, not recursive model queries |
| [CRITIC: Tool-Interactive Critiquing](https://arxiv.org/abs/2305.11738) | External tool-interactive validation of intermediate agent outputs | Tool execution must remain bounded within authorized scratch environments |
| [USENIX Security: Package Hallucinations](https://www.usenix.org/conference/usenixsecurity24/presentation/lazaar) | Defense against package hallucination and slopsquatting via strict identity-surface-probe verification | Local inspection cannot attest to external package repository integrity |
| [Empirical Mutation Testing (Just et al., FSE 2014)](https://homes.cs.washington.edu/~mernst/pubs/mutation-testing-fse2014.pdf) | Targeted mutation as an oracle sensitivity check; explicit tests for the 27% uncoupled semantic faults | Mutation testing is not an exhaustive substitute for domain-specific contract testing |
| [Google Mutation Testing (Petrovic & Ivankovic, ICSE 2018)](https://testing.googleblog.com/2021/04/mutation-testing.html) | AST-delta scoped mutants to prevent mutant explosion and equivalent mutant fatigue | Scoping must still exercise the complete modified contract boundary |
| [Industrial TDD Defect Study (Nagappan et al., EMSE 2008)](https://www.microsoft.com/en-us/research/publication/realizing-quality-improvement-through-test-driven-development-results-and-experiences-of-four-industrial-teams/) | Define independent acceptance oracles before implementation to drive defect density reduction | Upfront test authoring effort must be scaled to change consequence |
| [Brendan Gregg: Systems Performance & USE Method](https://www.brendangregg.com/usemethod.html) | Resource-oriented performance triage (Utilization, Saturation, Errors) before instruction tuning | Checklist triage does not replace application-level latency profile analysis |
| [Saltzer & Schroeder: Information Protection (IEEE 1975)](https://ieeexplore.ieee.org/document/1451869) | Complete mediation and fail-safe defaults applied to authorization, caches, and async jobs | Formal models do not guarantee bug-free implementation of the security controls |
| [Lost in the Middle (Liu et al., TACL 2024)](https://arxiv.org/abs/2307.03172) | Working context boundary pinning and raw log isolation to prevent attention degradation in long tasks | State pinning requires active discipline; compaction must not discard active constraints |

## Extreme systems performance engineering sources (0.6.0)

Reviewed on 2026-11-23. These primary systems engineering papers, manuals, and
architecture references ground `references/systems-performance.md` and
`scripts/compare_bench.py` across microarchitecture, memory hierarchy, lock-free
memory models, SIMD/vectorization, high-performance I/O, and statistical
measurement.

| Primary source | Applied mechanism | Boundary |
| --- | --- | --- |
| [Yasin: Top-Down Microarchitecture Analysis Method (ISPASS 2014)](https://doi.org/10.1109/ISPASS.2014.6844459) | Classify CPU hot-path stalls into Frontend, Bad Speculation, Memory Bound, and Core Bound via PMU counters before tuning | Counter availability varies by CPU vendor, virtualization layer, and host permissions |
| [Drepper: What Every Programmer Should Know About Memory (2007)](https://www.akkadia.org/drepper/cpumemory.pdf) | Cache hierarchy, SoA/hot-cold locality, cache-line alignment, TLB/huge pages, prefetching, non-temporal stores, and NUMA placement | Exact cache sizes, latencies, and prefetcher rules must be verified on the target CPU |
| [Boehm & Adve: Foundations of the C++ Concurrency Memory Model (PLDI 2008)](https://doi.org/10.1145/1375581.1375591) | Data-race-free semantics (zero benign races), formal Acquire/Release happens-before proofs, and weak memory model soundness | Language-level proofs still require empirical testing under Miri/Loom/TSan/weak-memory targets |
| [Mytkowicz et al.: Producing Wrong Data Without Doing Anything Obviously Wrong (ASPLOS 2009)](https://doi.org/10.1145/1508244.1508275) | Control and disclose measurement bias (pinning, governor, flags, memory/link layout sensitivity, interleaved A-B runs, nonparametric CI) | Eliminating every environmental confounder is infeasible on shared or virtualized hosts; disclose limits |
| [Gil Tene: HdrHistogram & Coordinated Omission](https://github.com/HdrHistogram/HdrHistogram) | Open-loop scheduled-arrival latency measurement (`t_sched`), offered vs achieved load, and distortion-free tail percentiles | Open-loop generators must still match realistic workload distributions and burst profiles |
| [Gunther: Universal Scalability Law (arXiv:0808.1431)](https://arxiv.org/abs/0808.1431) | Multi-core scaling sweeps capturing serialization (`alpha`) and cache-coherency crosstalk (`beta`) to detect retrograde scaling | Analytical model fits require measured multi-core samples on the target machine |
| [McKenney: Is Parallel Programming Hard, And, If So, What Can You Do About It?](https://www.kernel.org/pub/linux/kernel/people/paulmck/perfbook/perfbook.html) | Contention-elimination hierarchy, shared-nothing partitioning, RCU/EBR/hazard-pointer reclamation, and memory barrier discipline | Lock-free complexity is justified only when profiling shows contention on a real bottleneck |
| [Langdale & Lemire: Parsing Gigabytes of JSON per Second (VLDB Journal 2019)](https://doi.org/10.1007/s00778-019-00578-5) | SIMD/SWAR branchless structural parsing, runtime ISA dispatch, and scalar fallback with differential correctness verification | SIMD gains depend on ISA support, data width, and avoiding frequency throttling or page-boundary OOB |
| [Boncz, Zukowski & Nes: MonetDB/X100 Hyper-Pipelining Query Execution (CIDR 2005)](http://cidrdb.org/cidr2005/papers/P19.pdf) | Columnar L1/L2-sized batch vectorized execution amortizing virtual dispatch, branches, and synchronization | Batch sizing must respect tail-latency budgets on low-latency streaming pipelines |
| [Axboe: Efficient IO with io_uring (2019)](https://kernel.dk/io_uring.pdf) | Batched async submission/completion rings, registered buffers, and syscall amortization | Linux-specific kernel interface; requires kernel version/seccomp verification and portability fallbacks |
| [Bakhvalov: Performance Analysis and Tuning on Modern CPUs](https://book.easyperf.net/perf_book) | Practical `perf`, `perf c2c`, `llvm-mca`, optimization remarks, branch/ILP tuning, and compiler/PGO/BOLT verification | Microarchitectural tuning applies only to measured hot paths after algorithmic/layout tiers |
| [Agner Fog: Software Optimization Resources](https://www.agner.org/optimize/) | Execution port throughput/latency, dependency-chain breaking, calling/aliasing costs, and instruction-level trade-offs | Instruction tables are CPU-microarchitecture specific; verify with generated assembly and profiling |
| [TigerBeetle: TIGER_STYLE Engineering Discipline](https://github.com/tigerbeetle/tigerbeetle/blob/main/docs/TIGER_STYLE.md) | Upfront static memory allocation, explicit resource bounds, zero-ambiguity invariants, and deterministic simulation testing | Static allocation applies to bounded systems workloads; adapt bounds explicitly for dynamic workloads |

## Attribution and licensing

This project uses independently written instructions and original synthetic
fixtures. Referenced upstream text/code has not been copied into the distribution.
Links preserve provenance; upstream materials retain their respective licenses,
including share-alike terms where applicable. MIT applies to original content in
this repository, not to linked upstream repositories or standards. Incorporating
upstream text/code in a future contribution requires a separate license review.
