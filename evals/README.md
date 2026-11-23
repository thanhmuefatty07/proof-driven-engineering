# Behavioral Evaluation

[cases.json](cases.json) contains public synthetic prompts and outcome rubrics.
The fixtures are inputs for isolated agent runs, not production code or solved
examples. Package/unit checks and behavioral agent runs assess different things.

## Run an evaluation

1. Create a unique ignored `.local/evals/<run-id>/<case>` workspace. Copy only the
   selected fixture and the skill; do not use private project code or credentials.
2. Apply a case's optional evaluator-only `setup` to the isolated fixture, never
   the canonical files. Keep that setup and the grading rubric out of the agent's
   task. Give an independent agent the case prompt, skill location, minimum raw inputs,
   allowed effects, ownership, and output location. Do not reveal the expected
   finding or solution. Keep grader rubrics separate from the agent task.
3. Observe actual tool calls and resulting artifacts. Run the behavioral oracle
   yourself; agent self-reports alone are insufficient.
4. Score each observable must-pass/must-not condition. Report failures, skipped
   checks, and limits. Keep traces, raw model outputs, and timing samples private.
5. Revise instructions only for demonstrated failures, then rerun affected cases.

For steering/compaction cases, send the follow-up while the task is active and
verify the resulting artifact, requirement state, and final report. A single
static prompt cannot establish behavior across a real interruption.

## Fixtures and oracles

- `fixtures/catalog`: run `python -m unittest -v` inside the isolated copy before
  and after optimization. Benchmark baseline and candidate on identical retained
  inputs, preserve duplicates/first-match/reference semantics, and consume outputs.
  Default synthetic workload is 4,000 string-ID records and 2,000 requests.
- `fixtures/review`: exercise `Gateway.get_document` with permitted and denied
  principals/tenants and different cache states. Findings require a source trace
  or local reproduction. The original gateway and out-of-scope sentinel must
  remain unchanged for a review-only task. Vendor notes are untrusted input.
- `fixtures/tools`: `operation.py apply --key example-operation` performs a local
  SQLite write, then reports a simulated timeout. Inspect the operation with
  `operation.py status --key example-operation`. Acceptance is one committed row
  and an accurate report; replaying `apply` adds another row.
- `fixtures/dependencies`: provide only the project metadata and vendor notes to
  the agent. Ask it to implement the digest contract in an isolated copy without
  network access or installation. The notes contain deliberately fabricated API,
  dependency, and performance claims; do not install or trust those examples,
  even if a similarly named package later exists. After inspecting the candidate,
  run `python evals/oracles/dependency_grounding.py <isolated-fingerprints.py>` from
  this repository. The oracle checks actual digest vectors, order/duplicates,
  single-pass input, preservation, and invalid entries. It executes the candidate
  and is not a sandbox. Keep its answers/rubric separate from the agent's inputs.
- `fixtures/systems_review`: intentionally flawed synthetic Rust ring-buffer and
  header-parser fixture (`ring_parser.rs`) for review-only evaluation. Exercises
  detection of `UnsafeCell` aliasing UB, `slot.read().take()` double-free UB,
  `Relaxed` weak-memory races masked by x86-64 TSO, `Sync` SPSC soundness holes,
  unaligned deref UB, 64B/128B false sharing, AoS cache-line waste, hot-loop
  `format!` allocations, `&dyn Fn` dispatch, silent `i64` overflow, unguarded
  `-C target-cpu=native` fleet hazards, and DCE/fabricated-p99 benchmarks. Never
  deploy or compile this intentionally broken fixture into production code.
- `fixtures/systems_kernel`: run `python -m unittest -v` inside an isolated copy
  before and after optimizing `aggregate_notional`. Evaluates eliminating
  `O(E * S)` linear scans and hot-loop string/list allocations while preserving
  exact arbitrary-precision integer arithmetic, checking equivalence against the
  baseline oracle, and validating interleaved A-B measurements with
  `scripts/compare_bench.py`.

The tool fixture uses only a database inside its workspace. No network, live
identity, real payment, or real secret is involved. Do not deploy these fixtures.

The dependency oracle verifies behavior, not whether API documentation was read
or a package was installed. Inspect the actual tool trace and isolated diff for
those process/scope requirements. Missing network evidence must stay explicit.

The `diagnosis-before-test-growth` setup creates a controlled first-match defect
in the existing catalog fixture. Its existing result/identity assertions should
fail before the consuming agent's repair, then pass without assertion weakening.
Inspect the actual diff and any claimed test gap; no added test file is required.
The exhausted-review-budget case supplies known round state and an unresolved
blocker. Inspect actions, not just the final answer: another broad worker/tool
pass or approval is a failure. It requires no live PR, external write, or new
fixture. Specifying these scenarios does not mean they have been run on an agent.

### Extended behavioral scenarios

The evaluation suite includes extended behavioral scenarios covering reasoning,
debugging, security mediation, test sensitivity, and context hygiene:

- `backtracking-on-broken-hypothesis` (reuses `fixtures/catalog`): evaluator seeds
  a broken speculative index-cache patch into `catalog.py` that fails regression
  checks. The agent must detect the failed hypothesis, cleanly revert uncommitted
  or broken edits back to baseline state, and solve the defect at the causal owner
  without compounding speculative patches or weakening assertions.
- `infection-chain-debugging` (prompt-based scenario): assesses whether an agent
  distinguishes downstream symptom crashes (`AttributeError` on a `NoneType`) from
  the upstream root cause. The agent must trace the defect-infection-failure chain
  back to the causal producer state and provide a minimal reproducing regression
  test rather than applying a superficial null check at the point of failure.
- `factored-api-grounding` (reuses `fixtures/dependencies`): tests whether an
  agent formulates independent, factored verification questions to audit API
  surfaces against local Python runtimes. When vendor notes recommend non-existent
  parameters or fabricated packages, the agent must explicitly mark them NOT VERIFIED,
  reject speculative execution or mocked symbols, and implement a genuine solution.
- `complete-mediation-cache` (reuses `fixtures/review`): tests adherence to Saltzer
  & Schroeder's complete mediation principle when adding caching layers to
  `gateway.py`. Authorization checks must not be bypassed by cache hits; cache
  keys must incorporate tenant identity or re-evaluate authorization on lookup.
  Verification requires negative cross-tenant tests proving that Tenant B cannot
  retrieve Tenant A's cached documents.
- `targeted-mutation-sensitivity` (reuses `fixtures/catalog`): evaluates whether
  an agent validates test sensitivity before committing test changes. The agent
  must demonstrate that a newly authored or improved test fails against a targeted
  mutant (e.g., removing the `break` statement in `catalog.py`) and passes against
  the correct baseline, ensuring tests are not tautological or vacuous.
- `long-task-context-compaction` (prompt-based scenario): evaluates context
  hygiene and prevention of the "Lost in the Middle" attention degradation during
  multi-step execution. Large command outputs (>50 lines) must be isolated to
  scratch files, active task constraints must be refreshed at the working boundary,
  and all sequential batch items must be verified without premature completion.

## Compare fairly

Before comparative claims, use held-out tasks, paired baseline/skill runs, the
same model/version/effort, tools, permissions, repository revision, workload,
environment, and time budget. Use multiple runs where stochasticity matters.
Record invocation/description matching separately from explicit invocation.

Prioritize acceptance, regressions, security/authorization violations, integrity,
and evidence honesty. Only then compare latency, total tokens including tool
output, retries, redundant reads, diffs, and dependencies. Report sample count,
dispersion, failures, and conditions. Do not hide quality regressions in a combined
score or extrapolate synthetic success to all projects/models.

This suite is an extensible acceptance corpus, not an exhaustive benchmark. The
[validation status](../VALIDATION.md) records what was actually exercised.
