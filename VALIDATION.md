# Validation Status

Initial release validated within the following scope on 2026-10-07.

The executable checks cover skill discovery metadata, distributed references,
recorded acceptance coverage, exit/status validation, source-hash freshness, and
workspace path containment. Synthetic fixtures separately exercise catalog
behavior, security review, and ambiguous tool writes.

## Executable Checks

Local environment: Windows AMD64, Python 3.11.9, PyYAML 6.0.3.

| Check | Observed result |
| --- | --- |
| Codex bundled `skill-creator/scripts/quick_validate.py` on the distributed skill | Valid manifest |
| `python -m unittest discover -s tests -v` | 20 tests: 19 passed, 1 skipped |
| `python -m unittest discover -s evals/fixtures/catalog -v` | 3 tests passed |
| Additional independent evidence-gate adversarial tests | 20 tests: 19 passed, 1 skipped; includes 16 original gate tests |
| Publication diff, source/reference, and private-data review | Intended public files reviewed; generated local evidence excluded |

The skipped test is escaping-symlink rejection: Windows denied creating the test
symlink. Containment was inspected statically, but this runtime path remains
NOT VERIFIED locally. Linux/other Python CI execution is configured separately;
this local record does not assert remote CI success.

## Behavioral Forward Tests

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

## Not Verified

No paired baseline/skill benchmark, automatic invocation study, real compaction
evaluation, exhaustive object compatibility/concurrent-mutation test, production
security audit, or universal optimality proof has been performed. The standalone
unsafe-speedup and unavailable-dependency cases are specified for future runs;
they were not executed as separate tasks. This release makes no quantitative
claim about improving agent quality, runtime, or token usage across projects.

Raw traces, timing samples, generated evaluation workspaces, and local paths are
excluded from publication. Reviewed outcomes are kept concise in this document.
