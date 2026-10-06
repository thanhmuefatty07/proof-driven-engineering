# Review and Verification

## Review contract

A review request authorizes inspection and relevant bounded verification; it does
not authorize implementation or publication. Confirm scope and inspect the
complete diff and affected dependency/contract closure. Read authoritative
definitions, important callers, tests, configuration, generated boundaries, and
relevant history when it can explain a regression.

Find behavioral defects, security failures, data/concurrency risks, compatibility
breaks, and missing decisive tests. Avoid cosmetic findings without a concrete
effect. Investigate a credible benign explanation before reporting a concern;
validate that upstream guards actually protect every affected path.

Each actionable finding includes:

`priority | file/line | trigger/preconditions | observed behavior | impact |
evidence/reproduction | owning fix direction`.

Order findings by exposure and impact. Mark inference and missing evidence.
Report no findings when appropriate, together with the scope/tests and remaining
limits. Never manufacture findings to sound adversarial. For a fix request,
resolve the root owner and inspect sibling paths rather than repeating symptoms.

## Verification that can fail meaningfully

Map acceptance criteria to their oracle: compiler/type check, direct behavior,
integration/contract, user journey, property/fuzz, security reproduction, load,
or recovery test. Match the oracle to the claim. Source text matching cannot show
that an agent follows an instruction; a green unit suite cannot establish a
rendered interface, deployment, migration recovery, or end-to-end performance.

Use independently derived expectations. A regression test should fail with the
known bad behavior and pass after the fix. Control clock, randomness, locale,
external dependencies, and concurrency when they otherwise cause nondeterminism.
Keep tests for realistic invariants; avoid tests that reproduce implementation
logic or only assert a mock's existence.

Run the smallest decisive checks first, then all gates required by the repository
and affected closure. Broaden when a failure or risk requires it. Read failures
and warnings, including pre-existing failures you observed. Do not rerun unchanged
inputs until a flaky test turns green or disable tests/suppressions to finish.

Recheck only evidence invalidated by new changes, while completing mandatory
gates. Before completion/publication, inspect the full diff, stale references,
generated-source consistency, dependency changes, tracked files/history, private
data, workflow log output, and artifact uploads. Publicity authorization applies
to the requested target and intended content, not adjacent repositories/data.

## Optional evidence gate

Use the bundled script for substantive tasks when mechanical coverage/freshness
checking is useful. Keep the record in the host's approved ignored/private local
location. Run from the target project root:

```sh
python /path/to/skill/scripts/check_evidence.py /path/to/local/evidence.json --root .
```

The record is strict JSON:

```json
{
  "schema_version": 1,
  "goal": "The user's current requested outcome",
  "requirements": [{"id": "R1", "checks": ["regression"]}],
  "checks": [{
    "id": "regression",
    "status": "pass",
    "command": "python -m unittest",
    "exit_code": 0,
    "inputs": {"relative/source.py": "64-character-lowercase-sha256"}
  }]
}
```

Record actual commands and exit codes after reading their output. Each check
includes the relevant source, tests, fixtures, configuration, and lockfile hashes
that can invalidate it. Cover every material requirement with at least one
appropriate check. Hashes are computed from exact file bytes; paths are relative
POSIX paths inside the target root. Empty inputs, duplicates, missing checks,
failed/unverified status, nonzero/noninteger exit codes, unsafe paths, malformed
hashes, and changed inputs fail the gate. Do not store command-line credentials.

The gate validates recorded coverage, exit codes, and current hashes. It does
**not** execute commands, attest that they ran, infer the correct scope, detect
omitted requirements, or verify a narrative claim. Check the actual tool/test
output and task yourself. Passing this gate is not proof of correctness/security.
Input hashes reflect the file bytes observed when read, not a lock against
concurrent writes. The script is a local workflow guard, not a filesystem sandbox.
It uses Python 3.11+ and the standard library only.

## Final evidence and limits

Use concise outcome -> decisive evidence -> unresolved limitation. State measured
metrics with conditions and units. If a check is unavailable, say
`NOT VERIFIED - <check and reason>`. Do not upgrade self-review, scanner silence,
or a synthetic test into production readiness. Produce findings before summaries
for review tasks. Finish authorized implementation instead of stopping at a plan.
