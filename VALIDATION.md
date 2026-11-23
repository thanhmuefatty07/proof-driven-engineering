# Validation Status

## Release 0.6.0: Extreme Systems Performance & Research-Backed Engineering

Updated on 2026-11-23. Preserves 100% of Release 0.5.0 capabilities and recovers
omitted 0.4.1–0.4.5 test-portfolio, mutation, runtime-selection, citation, and
Vietnamese-documentation assets from `origin/codex/test-quality-portfolio-20261016`
(recorded in `BRANCH_EVALUATION.md`; remote branch retained untouched). Adds:

- Empirical research upgrades across core references: LATS 2-strike backtracking,
  Zeller infection-chain debugging, Gregg USE/RED, Bentley hierarchy, Roofline
  Model, Saltzer-Schroeder Complete Mediation + OWASP API Top 10, 3-stage
  dependency grounding (slopsquatting ban), Just et al. 27% uncoupled mutation +
  Google AST-delta scoping, CoVe factored self-verification, CRITIC extrinsic
  feedback primacy, and Lost-in-the-Middle context boundary pinning.
- Dedicated extreme systems performance engineering reference
  (`references/systems-performance.md`) covering TMAM hardware triage, data-oriented
  SoA/hot-cold/pointer-chasing elimination, 128B false-sharing isolation, NUMA
  first-touch, zero hot-path allocation and hidden refcount-churn elimination,
  formal Boehm/Adve Acquire-Release lock-free memory ordering and x86-64 TSO vs
  ARM64/RISC-V weak-memory verification, columnar batching and runtime-dispatched
  SIMD, `io_uring`/`O_DIRECT`/honest durability, compiler/assembly libcall audits,
  Mytkowicz/Gil Tene/Gunther anti-illusion benchmarking, and scalar differential
  oracles.
- Optional zero-dependency statistical A/B benchmark comparator
  (`scripts/compare_bench.py`, Python 3.11+ stdlib) with nonparametric paired/unpaired
  bootstrap 95% CI, Cliff's delta, Mann-Whitney U, and noise-floor gating, plus
  unit and adversarial tests (`tests/test_bench_compare.py`).
- Extended behavioral evaluation suite (18 total cases in `evals/cases.json`),
  including `fixtures/systems_review/ring_parser.rs` and
  `fixtures/systems_kernel/` (`kernel.py` + `test_kernel.py`).

### Automated Package, Tool & Fixture Checks (2026-11-23)

Checked on Windows AMD64, Python 3.11.9 with PyYAML 6.0.3 (matching CI 3.11 target).
Tests and runner are trusted for ordinary local checks, not independently attested.

| Check | Observed result |
| --- | --- |
| `python -B -m unittest discover -s tests -v` | 30 discovered: 29 passed, 1 skipped (Windows symlink); exit 0 |
| `python -B -m unittest discover -s evals/fixtures/catalog -v` | 3 passed; exit 0 |
| `python -B -m unittest discover -s evals/fixtures/systems_kernel -v` | 3 passed; exit 0 |
| `python -B scripts/check_preservation.py` | 0 unmapped removals vs `2f50e21`; 38/38 capabilities (`CAP-01..38`); `SKILL.md` 248 lines (`< 250`), description 361 chars (`<= 1024`); exit 0 |
| `git diff --check` | No whitespace errors; exit 0 |

### Paired Synthetic Behavioral Evaluations (RED vs. GREEN, 2026-11-23)

Evaluations ran on fresh subagents in isolated read-only / `.local/` scratch
workspaces; temporary `.local/` artifacts were deleted after parent verification.
These are bounded synthetic acceptance examples, not a statistical proof of
universal model compliance or superiority across all repositories.

| Scenario | RED Baseline (v0.5.0) | GREEN Upgraded (v0.6.0) |
| --- | --- | --- |
| Rust 4-producer 10M/s telemetry codegen (`flash`) | Scattered 3-`Box` per-symbol heap allocations, 6B struct padding, unbounded SeqLock reader spin livelock, per-item `shutdown` atomic in `try_push`, mismatched 1M vs 20M single-run benchmarks, 16 inline comments/banners, unguarded `-C target-cpu=native` | Flat inline `[f64; 64]` per symbol, packed 24B `TelemetryEvent` with `size_of` assert, bounded `MAX_SEQLOCK_RETRIES`, `HeadCommitGuard` panic safety, `#[cold]` splitting, zero-alloc histogram, matched 7-round interleaved A-B-A-B runs, `perf --topdown`/`perf c2c`/Miri/Loom/ARM64 plan; caught `Arc::clone` in `drain_batch` and added explicit refcount-churn rule in REFACTOR |
| Rust 10M/s market-tick aggregator design (`XHigh`) | `i128::checked_mul` on every tick (hidden `__muloti4` libcall), 64B slot alignment, startup-thread slot allocation (no NUMA first-touch), no TMAM/Mytkowicz/USL framing | Mathematically proved overflow-free `(i64 as i128).wrapping_mul(u32/u64)` (zero `__muloti4`), 128B isolated `PublishedSymbolSlot`, NUMA first-touch on pinned shard thread, formal Boehm fence-fence proof + ARM64 codegen, TMAM + USL + open-loop `t_sched` + `compare_bench.py` plan |
| Live isolated `systems_kernel` optimization (`flash`, executed) | N/A (new 0.6.0 fixture) | Eliminated `O(E*S)` scan & per-event string/list allocations with `__slots__` + single pre-seeded lookup; parent reran 3/3 contract tests (exit 0) and verified canonical fixture unchanged; 9x5 differential oracle passed; 10 interleaved A-B runs validated via `compare_bench.py --require-improvement`: `66.90x` median speedup (`1496.85 ms -> 22.38 ms`, paired bootstrap 95% CI `[53.68x, 98.26x]`, Cliff's delta `+1.000`, `p=0.000157`) on shared Windows host |

### Explicit `NOT VERIFIED` Limits (Release 0.6.0)

- Escaping-symlink runtime test skipped on Windows (`NOT VERIFIED` locally; covered by Ubuntu CI matrix).
- Generated Rust designs/code skeletons in the read-only design/codegen evals were not compiled or executed under Miri/Loom/TSan/ARM64 hardware (`NOT VERIFIED`).
- Live `systems_kernel` timings ran on a shared Windows host without isolated physical core pinning or locked CPU power governor (`NOT VERIFIED` for hardware-isolated low-variance benchmarking).
- Cross-platform Linux/Python 3.13 CI runs remain `NOT VERIFIED` until GitHub Actions executes on the pushed commit.

## Release 0.5.0: Outcome-First Systems Engineering

Instruction and documentation update on 2026-10-18. The update preserves the
installed 0.4.5 test-portfolio, runtime-selection, mutation, and evidence-integrity
guidance, adds outcome-first system modeling, diagnosis before test growth,
progress-based stopping, coordinated delegation, and a three-round logical-PR
review budget. It prohibits generated explanatory code comments while preserving
mandatory legal, functional, public-contract, and higher-priority requirements.
No executable product code, production test, dependency, or CI workflow changes.

Checked with Windows AMD64, Python 3.11.9 and the pinned PyYAML 6.0.3. The approved
repository unittest runner used its verified Python 3.11 installation, matching
the CI 3.11 target; the additional CI 3.13 and Linux targets were not run locally.
Tests/runner are trusted for these ordinary checks, not independently attested.

| Check | Observed result |
| --- | --- |
| `python -B -m unittest discover -s tests -p test_package.py -v` | 5 package/reference checks passed; exit 0 |
| `python -B -m unittest discover -s tests -v` | 21 discovered: 20 passed, 1 skipped; exit 0 |
| `python -B -m unittest discover -s evals/fixtures/catalog -v` | Existing 3 contract tests passed; exit 0 |
| `python -B -m unittest -v` in the isolated catalog control | 3 executed; first-match/duplicate assertion failed with the intended wrong result, 2 passed; expected exit 1 |
| Same control after restoring only its implementation | All 3 passed; exit 0; existing test file byte-identical |
| Bundled Codex skill manifest validator | Source and both installed copies valid; exit 0 |
| Installed distribution comparison | All 9 files match source by SHA-256 in both local copies |

The negative control removed the first-match loop termination in a small isolated
copy. Its existing assertion rejected extra duplicate records; this was not an
import, setup, or collection failure. Public fixture and test sources remained
unchanged; no test method/file or weakened assertion was added. The gate tests'
owned temporary directory was empty afterward. Two restored synthetic control
files (1479 bytes total) remain ignored/private because the explicit cleanup
command was denied before execution. No successful explicit cleanup is claimed;
no alternate deletion route was attempted. Rollback copies are retained privately.
The skipped escaping-symlink runtime path is NOT VERIFIED on this Windows host.

The existing acceptance corpus is extended in place with diagnosis-first and
exhausted-review-budget scenarios. A controlled catalog defect can establish the
existing assertions' sensitivity, not that a consuming agent diagnoses it or
obeys the new rules. No new consuming-agent run, paired comparison, cross-platform
run, live PR/plugin review, native security scan, or independent anti-tamper
observer is claimed. Exact compiler/runtime optimization remains workload-specific;
no per-line/global optimum, exhaustive diagnosis, or future compliance is proven.

## Release 0.4.5: Minimal Discriminating Test Portfolio

Published on 2026-10-17 to branch `codex/test-quality-portfolio-20261016`. This instruction-only update requires a compact task-note case map before adding, removing, or selecting tests: requirement, plausible wrong behavior, nearest existing check and exact gap, independent expected result, exercised boundary, decisive assertion, run/artifact cost, and verification limit. It defaults to the owning suite, requires a concrete distinct owner/boundary/runner/lifecycle/CI-selection reason for a new test file, and sets a stop condition once required defect classes have sensitive checks; inaccessible boundaries remain NOT VERIFIED. No executable code, test case, or dependency changed.

| Check | Observed result |
| --- | --- |
| Bundled skill manifest validator | Passed locally on Windows Python 3.14.7 with PyYAML 6.0.3; exit 0 |
| Local Markdown integrity | 22 relative links resolved; no missing targets or trailing whitespace |
| Executable suites and consuming-agent evaluation | Not run for this instruction-only update; test quality and agent adoption remain NOT VERIFIED |
| GitHub CI | No CI result is claimed by this validation record; remote execution remains NOT VERIFIED |

## Release 0.4.4: Runtime Selection for Test Evidence

Reviewed on 2026-10-17 from branch commit 9b0e583c4465c34668f5e3682abbcf950432cd25. This instruction-only update requires resolving the supported runtime from project metadata, lockfiles, toolchain pins, and CI, then verifying the runtime selected by the approved runner. It also distinguishes unsupported-runtime collection or syntax errors from product regressions. No executable code, test case, or dependency changed in the 0.4.4 commits.

| Check | Observed result |
| --- | --- |
| Distributed skill metadata and runtime guidance | Inspected on the published branch: metadata is 0.4.4 and the runtime-selection rule is present in both the core skill and testing-quality reference |
| GitHub status checks | No checks were returned for branch HEAD 9b0e583c4465c34668f5e3682abbcf950432cd25; remote CI remains NOT VERIFIED |
| Executable suites and consuming-agent evaluation | Not run in this validation update; agent adoption and runtime behavior across projects remain NOT VERIFIED |

## Release 0.4.3: Test-Runner Evidence Trust Limits

Reviewed on 2026-10-17 from commits 06abd17a6c3046762de4f1c76f3b3131b5588ac1 and 4a3f1bdf6d6a276a5701e2e9c55162694236c037. This instruction-only update clarifies that runner output, reports, and hashes are evidence from a process, not independent proof that intended tests executed. It requires inspecting selected IDs, decisive assertions and host-observed exit status for ordinary checks; anti-tamper claims require an independent observer protected by an OS boundary. It adds no executable code, test case, or dependency.

| Check | Observed result |
| --- | --- |
| Published reference content | Inspected on the branch; trust limits and the 0.4.3 skill metadata are present |
| Executable suites and consuming-agent evaluation | Not run in this validation update; no new behavioral or anti-tamper result is claimed |
| Remote CI status | The later 0.4.4 branch HEAD has no reported status checks; CI for these releases remains NOT VERIFIED |

## Release 0.4.2: Targeted Mutation Sensitivity

Reviewed on 2026-10-16. This instruction-only update clarifies when mutation
checks add evidence and how to distinguish a killed mutant from a broken test
run. It adds no runtime code, test case, or dependency.

| Check | Observed result |
| --- | --- |
| Local testing-quality document integrity | Passed: the mutation guidance is present, its relative link resolves, whitespace is clean, and the skill metadata is 0.4.2 |
| Primary-source review | Three first-party Google Testing Blog pages fetched and reviewed: Mutation Testing (2021), Increase Test Fidelity By Avoiding Mocks (2024), and Keep Tests Focused (2018) |
| Executable package and catalog suites | Not rerun: this release changes instructions and release notes only; no executable files, tests, or dependencies changed. The 0.4.1 results below are historical evidence for that release, not a fresh 0.4.2 run. |

No consuming-agent evaluation was run for the new mutation guidance. Whether agents consistently apply it remains NOT VERIFIED; the skill cannot mechanically enforce compliance.

## Release 0.4.1: Evidence-Based Test Portfolio

Checked on 2026-10-16 with Windows and Python 3.11.9. This instruction-only
update adds a minimal-discriminating-set rule and evidence requirements before
consolidating or deleting tests. It adds no executable code, test case, or
dependency.

| Check | Observed result |
| --- | --- |
| `python -m unittest discover -s tests -v` | 21 discovered: 20 passed, 1 skipped; exit 0 |
| `python -m unittest discover -s evals/fixtures/catalog -v` | 3 passed; exit 0 |
| `git diff --check` | No whitespace errors; exit 0 |
| Scratch cleanup | Run-owned scratch root was empty and removed; verified absent |

The skipped symlink test could not create a symlink in this environment; that
runtime path remains `NOT VERIFIED`. No consuming-agent evaluation of the new
test-consolidation rule was run. The 0.4.0 acceptance example predates this rule
and is not evidence that agents follow it. Skill instructions guide behavior
but do not mechanically enforce test quality or guarantee agent compliance.

## Release 0.4.0: Test Quality and Artifact Lifecycle

Checked on 2026-10-16 with Windows AMD64, Python 3.11.9 and PyYAML 6.0.3.
This release changes instructions and optional host guidance, with no new runtime
code or dependency. It adds a focused test-quality reference and private milestone
practice; operating-system quotas remain the host's responsibility.

| Check | Observed result |
| --- | --- |
| `python -B -m unittest discover -s tests -v` | 21 discovered: 20 passed, 1 skipped; exit 0 |
| `python -B -m unittest discover -s evals/fixtures/catalog -v` | 3 passed; exit 0 |
| Bundled Codex skill manifest validator | Valid; exit 0 |
| Owned scratch after package checks | No remaining entries |
| Isolated known-bad catalog control | Existing 3-test suite executed; duplicate/first-match test failed for the intended wrong result; exit 1 |
| Consuming-agent example and parent verification | One-line repair, existing 3 tests passed; no added test files; parent checked 7 independent contract vectors and rejected a controlled wrong result |

The consuming agent received the candidate skill, a small isolated faulty catalog
and its existing tests, without a supplied repair or grading oracle. The parent
observed the failing baseline, inspected the resulting one-line change, verified
the existing tests' exact hash was unchanged, and reran the suite. Independent
vectors covered order, duplicate requests, first-match object identity, missing
and empty inputs, input preservation, equality semantics and unhashable IDs. The
original public fixtures, tests and evidence-gate script stayed unchanged. The
owned workspace retained only its two source/test files and instruction file;
no generated run data was present. Raw evidence remains private.

This is one synthetic in-process acceptance example. Model settings were
inherited; the exact consuming model identifier was not captured. It does not
establish comparative effectiveness, exhaustive test quality, real external or
cross-platform behavior, interruption recovery, automatic quota enforcement, or
future agent compliance. The Windows symlink test was skipped because creating
the link was unavailable; that runtime path remains NOT VERIFIED locally.

## Earlier Release Evidence

Local version 0.3.0 executable checks were refreshed on 2026-10-08.
Earlier forward runs remain attributed to versions 0.1.0 and 0.2.0 below.

The executable checks cover skill discovery metadata, distributed references,
recorded acceptance coverage, exit/status validation, source-hash freshness, and
workspace path containment. Synthetic fixtures separately exercise catalog
behavior, security review, ambiguous tool writes, and dependency/API grounding.

## Executable Checks

Local environment: Windows AMD64, Python 3.11.9, PyYAML 6.0.3.

| Check | Observed result |
| --- | --- |
| Codex bundled `skill-creator/scripts/quick_validate.py` on the distributed skill | Valid manifest |
| `python -m unittest discover -s tests -v` | 21 tests: 20 passed, 1 skipped |
| `python -m unittest discover -s evals/fixtures/catalog -v` | 3 tests passed |
| Additional independent evidence-gate adversarial tests | 20 tests: 19 passed, 1 skipped; includes 16 original gate tests |
| Publication diff, source/reference, and private-data review | Intended public files reviewed; generated local evidence excluded |
| Dependency oracle against a deliberately incorrect local control | Exit 1; all five test methods rejected the candidate, including invalid-input subcases |

The skipped test is escaping-symlink rejection: Windows denied creating the test
symlink. Containment was inspected statically, but this runtime path remains
NOT VERIFIED locally. Linux/other Python CI execution is configured separately;
this local record does not assert remote CI success.

## Release 0.1.0 Forward Tests

Three independent runs used `gpt-6.1-sol` with high reasoning effort, explicit
skill invocation, isolated synthetic copies, and disjoint file ownership. The
parent inspected actual artifacts, reran behavioral tests, reconciled persisted
state, and checked input hashes. These are acceptance examples, not a paired
comparison of skill effectiveness or independent statistical replication.

| Scenario | Observed outcome |
| --- | --- |
| Catalog optimization | 12 contract tests passed; 100 seeded differential cases checked identity/input preservation; final source hashes matched the measurement record |
| Review-only tenant gateway | Two distinct authorization defects reproduced; one positive and three failing denial tests exposed the intentionally unsafe fixture; original files and sentinel unchanged |
| Ambiguous local write | One apply call returned exit 1 after committing; subsequent status returned exactly one effect; no blind replay; tool source unchanged |
| Compatible steering during the tool task | Status question and Vietnamese-report requirement retained the original objective; final report included the verified effect count |

The catalog candidate used a first-occurrence index with compatibility fallbacks.
Measurements included 4,000 records, 2,000 requests, seven alternating pairs,
three calls per sample, and one warmup per implementation. Inputs were prepared
outside timing; index construction was included; outputs were retained/consumed.

Mixed-request median decreased from 401.124 to 2.974 ms/call, and all-missing
median from 1,487.381 to 7.433 ms/call in that run. Traced peak Python allocation
for mixed requests increased from 14,400 to 155,784 bytes. Variability was large:
mixed baseline ranged 283.086-977.788 ms/call and candidate 2.630-35.310 ms/call.
These are workload-specific observations; no tail-latency, process-memory,
hardware-independent, or end-to-end speed claim follows. The solved catalog and
raw measurements are private, not part of the distributed skill.

The review-only wording was clarified after the forward review to remove an
ambiguity between fixing implementation failures and reporting review findings.

## Release 0.2.0 Grounding Test

One isolated forward run used explicit invocation of the updated skill, only the
project metadata and vendor notes, and no provided solution/oracle. Host model
settings were inherited; an exact model identifier was not captured. This is an
exploratory acceptance example, not a matched model comparison.

The parent reviewed the implementation and 17 recorded command-return receipts,
confirmed both fixture hashes were unchanged, independently inspected the runtime
API, and reran the candidate's eight tests and the five-test external oracle.
Both suites passed on Windows Python 3.11.9. The oracle separately rejected a
deliberately incorrect local control. The worker's first test run failed on a
missing candidate module; that import failure is not a behavioral regression
test by itself.

The candidate uses the standard-library SHA-256 constructor and hexadecimal
digest method, validates bytes entries, and traverses the input once. Local
inspection confirmed the suggested batch symbol was absent on this runtime.
The proposed external distribution/import mapping, universal compatibility, and
32-times speed claim stayed NOT VERIFIED and were not implemented. No external
dependency was added to the unchanged project metadata. Recorded commands showed
no package installation or network call; these local receipts are not a sandbox
or cryptographic execution attestation.

## Not Verified

The 0.3.0 instruction update was inspected against the requested generation,
selection, compiler/runtime, and benchmark rules. Existing security, dependency
grounding, continuity, and verification instructions remain unchanged. It adds
no executable optimization or new dependency. No new consuming-agent performance
evaluation was run; earlier forward outcomes do not establish consistent steering
or improved performance under the revised instructions.

No paired baseline/skill benchmark, automatic invocation study, real compaction
evaluation, exhaustive object compatibility/concurrent-mutation test, production
security audit, or universal optimality proof has been performed. The standalone
unsafe-speedup and unavailable-dependency cases are specified for future runs;
they were not executed as separate tasks. This release makes no quantitative
claim about improving agent quality, runtime, or token usage across projects.
The grounding run did not exercise a live package registry, a vendor SDK, other
ecosystems, or every possible invented flag/configuration/protocol field.

Raw traces, timing samples, generated evaluation workspaces, and local paths are
excluded from publication. Reviewed outcomes are kept concise in this document.
