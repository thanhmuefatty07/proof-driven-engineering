# Validation Status

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
