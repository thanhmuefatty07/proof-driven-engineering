# Test Quality and Artifact Lifecycle

Use this reference when designing, adding, selecting, running, or interpreting
tests. The objective is evidence that rejects plausible defects in the requested
behavior. More tests, files, coverage, or repetitions are not acceptance criteria.
Preserve mandatory repository gates and all required behavioral boundaries.

## Define a discriminating check

For each material requirement, identify:

`requirement -> plausible defect -> independent expected result -> exercised
boundary -> decisive assertion -> verification limit`.

Derive expectations from the contract, trusted examples, protocol, or an
independent reference. Do not copy the implementation into the oracle, generate
expected output with the candidate being tested, or approve snapshots without
checking their meaning. Assert returned values, persisted state, externally
visible effects, and required absence of effects where relevant. A success flag,
mock call count, file existence, or source-text match alone is insufficient for a
behavioral claim; structural checks remain useful for actual structural rules.

Before adding a case, inspect existing tests and name the missing defect class it
will detect. Reuse or extend the owning suite. Parameterize meaningful partitions;
do not make separate files for equivalent examples, multiply arbitrary inputs,
or generate a Cartesian product without a contract or failure model requiring it.
Do not add tests for reversible prose or mechanical edits merely to raise counts.

For a regression, observe the intended behavioral failure against the known bad
behavior, then the pass after the fix. An import, collection, syntax, environment,
or unrelated failure does not establish that the regression test is sensitive.
When practical, challenge an important oracle with a controlled wrong result or
minimal mutation in an isolated copy. Never rewind dirty user work, weaken a live
system, or keep a mutated implementation. If this cannot be done safely, describe
the missing sensitivity evidence rather than inventing a red/green history.

## Keep the test portfolio focused

Before adding or removing tests, map the relevant existing checks to their
contract, plausible defect, independent oracle, exercised boundary, and decisive
assertion. Add the smallest set that covers each distinct defect class and each
interaction required by the failure model. Combine cases when one run can make
clear independent assertions; separate them when they exercise different owners,
boundaries, setup/lifecycle rules, or recovery paths. Do not create one test file
or case per requirement, branch, or input value. Extend the owning suite by
default. A new file needs a concrete reason, such as a distinct owner, runner
setup, or fixture lifecycle.

Names, source-code similarity, shared fixture values, and line-coverage overlap
do not prove behavioral redundancy. Consolidate or delete a test only after
confirming that the surviving check preserves the same contract, oracle,
boundary, and failure signal; that the removed test contributes no independent
assertion or failure mode; and that no discovery rule, CI job, manifest, or
document relies on it. Where practical, verify that the surviving check still
rejects a representative wrong behavior. Preserve a test when it protects a
distinct behavior or boundary. If equivalence or consumer impact is uncertain,
keep it and report the unresolved review instead of deleting speculatively.

Do not set arbitrary test-count or file-count targets. Do not delete valid
boundary, failure, or recovery cases to make a suite smaller or faster. Report
material consolidation with the removed check, its former coverage, the retained
check that now supplies that evidence, and any verification limit.

## Match realism to the claim

Use the smallest real path sufficient to expose the defect. Synthetic data can
exercise real code and real local boundaries without containing private data.

| Claim | Relevant evidence | Limit to preserve |
| --- | --- | --- |
| Domain behavior | Real function, contract-derived edge and invalid cases | Does not establish integration |
| Persistence or file handling | Real driver/filesystem, reload or fresh process, required failure/atomicity cases | An in-memory substitute does not establish durability or platform semantics |
| API or event compatibility | Actual serializer and producer/consumer contract, malformed and denied cases | A mocked response does not establish provider behavior |
| User journey or native platform | Running application on the claimed platform and critical path | Browser preview does not establish native behavior; local simulation does not establish another OS |
| Security or recovery | Concrete denied operation, failure/restart scenario, and protected-state assertion | A happy path or empty scan is insufficient |
| Performance | Comparable workload, consumed outputs, repeated measurements and units | A timing assertion or one fast run is not a general speed claim |

Use doubles for controlled dependency failure, time, randomness, or an unavailable
external boundary. Keep the implementation under test real, verify the actual
boundary separately when the claim needs it, and label the unexercised part
`NOT VERIFIED`. Do not contact production or incur external effects merely to
make a test realistic. Existing authorization still governs live verification.

Select relevant boundaries: empty/minimum/maximum input, malformed data, denied
access, duplicate/reordered/concurrent operations, stale state, interruption,
timeout, and dependency failure. Do not impose every category on every change.
Use bounded property/fuzz runs for valuable input spaces; retain the seed and
smallest failing example. Large fixtures require a defect they uniquely expose.

## Execute and report honestly

Run a focused decisive check first, then required gates and the affected contract
closure. Broaden for changed shared boundaries, discovered failures, or unresolved
risk. Do not rerun a full suite after every edit or run unchanged checks until
green. Retest evidence invalidated by changed inputs; complete mandatory gates.

For a consequential check, retain its command, working directory, input revision
or hashes, runtime/platform, selected scope, actual exit status, meaningful
counts, and decisive output. Observe completion; launching a job is not a pass.
Inspect collection and execution errors, skips/xfails and warnings. Zero executed
tests, an all-skipped target, a timeout, or a pipeline hiding the runner's failure
cannot satisfy a behavioral gate. Expected negative-control failures are recorded
as such, separately from acceptance passes.

Separate unit, integration, end-to-end, static, and manual evidence. Do not report
unrun checks, stale output, generated receipts, self-review, or mock-only tests as
real execution. A check unavailable locally stays `NOT VERIFIED` with its reason
and the appropriate next gate. Record observed unrelated failures; fix them only
when in scope. Never delete assertions, broaden exception acceptance, suppress
warnings, change expected values, or disable gates simply to obtain green output.

## Own temporary data before creating it

Before a check that writes data, declare its owner and scratch root, expected
file/byte growth, time/workload bounds, available capacity, and disposition. Use
estimates appropriate to the run, not invented universal quotas. Check free space
on both source and archive volumes for material writes. Use existing runner
limits; if a hard limit is unavailable, say so and avoid an unbounded workload.

Keep fixture state isolated per test or worker; share immutable expensive setup
only when isolation still holds. Reuse compatible build caches keyed by relevant
toolchain, target, flags, features and dependency inputs. Do not allocate another
checkout, virtual environment, dependency tree, or Cargo target for every retry
unless the required isolation justifies it. Never copy caches/private data into
a fixture that needs only a few synthetic inputs.

Use the host-approved temporary root and scoped lifetime mechanisms such as
context-managed directories, fixture finalizers, or RAII. Close processes, files,
database connections and mappings before removal. Verify cleanup on success and
on a representative assertion/setup failure when introducing lifecycle code.
Normal teardown is not crash recovery: identify interrupted runs and clean only
confirmed abandoned, owned paths through the repository's recovery procedure.

Cleanup belongs to the test infrastructure for disposable data it created. Keep
required fixtures, active gate inputs, user changes and reproducibility metadata.
On failure, preserve the smallest sufficient sanitized diagnostic/reproducer;
retain larger data only for a named consumer and retention reason. Do not keep a
whole successful run by default or recursively delete another run's directory.
Resolve and verify deletion targets, reject links/junction escapes, and respect
the host's authorization rules. This document grants no bulk-cleanup permission.

With pytest, inspect the installed version's retention behavior. Unique
`--basetemp` paths prevent concurrent collisions but do not prune older uniquely
named roots; that option clears its selected directory. Never point it at a
shared cache, evidence store, repository, or another active run. Verify the
chosen lifecycle rather than assuming the word temporary implies cleanup.

## Close the evidence loop

At the milestone, update the existing private checkpoint with the requirement,
decision, actual checks and limits, evidence pointers, retained artifact owner,
cleanup outcome, and next unresolved action. Follow
[continuity-tools.md](continuity-tools.md) for private destination selection and
verified archival. Keep source tests in their owning suite and reviewed findings
in the project's existing authority. Avoid duplicate reports and copied logs.

These instructions guide test decisions; they cannot mechanically guarantee an
agent's honesty, enforce operating-system quotas, or prove exhaustive coverage.
Use actual repository gates and inspect the resulting behavior and artifacts.

## Primary references

- [pytest temporary directory ownership and retention](https://docs.pytest.org/en/stable/how-to/tmp_path.html)
- [pytest fixture teardown and safe cleanup](https://docs.pytest.org/en/stable/how-to/fixtures.html#teardown-cleanup-aka-fixture-finalization)
