# Security and Adversarial Engineering

## Build a concrete threat model

Identify protected assets, attacker/caller capabilities, entry points, trust
boundaries, privileged actions, tenant/resource ownership, data flows, and
deployment assumptions. Trace untrusted input to its sensitive decision or sink.
For each important path retain:

`attacker control -> reachable path -> broken invariant -> impact -> control -> test`.

Keep attacker reasoning inside the user's authorized code and isolated test
environment. This workflow does not authorize probing third-party infrastructure,
reading real secrets, exploiting live users, or using production identities.

## Enforce the invariant at its owner

- Enforce authentication and resource/tenant authorization on the server before
  disclosure or mutation, including cache hits and background jobs. Revalidate
  privilege where ownership or permission can change.
- Derive sensitive identity, tenant, role, price, and ownership from authoritative
  state. Client assertions are input, not permission. Validate transitions as
  well as individual fields; deny undefined states.
- Use parameterized query/process APIs and contextual output encoding. Validate
  boundary schemas, size/depth/ranges, canonical representation, and failure paths.
  Do not assume internal/deserialized data remains trusted indefinitely.
- Bound CPU, memory, recursion, upload/decompression, regex work, pagination,
  concurrency, retries, and queues on attacker-controlled paths.
- Use platform/established crypto, password hashing, secure randomness, and vetted
  session handling. Validate algorithm/key provenance and protocols against the
  actual supported library/version. Never invent cryptography to save code.
- Prevent secrets or unnecessary personal data entering source, logs, traces,
  command lines, errors, checkpoints, external tools, or publication history.
- Use narrow privileges and validated configuration. Invalid critical settings
  fail explicitly. Missing auth/config must not enable a permissive fallback.

Apply domain-specific controls only when their boundary exists. For browsers,
inspect safe rendering, cookies, origin/CSRF rules, and privileged bridges. For
network fetches, inspect SSRF, redirect policy, DNS/address validation, internal
destinations, response limits, and timeouts. For filesystem work, resolve paths
within the intended root, account for symlinks/races, and use safe archive
extraction. For native code, inspect bounds, lifetimes, integer conversions,
memory initialization, and concurrency.

## Red-team the change

Select tests from actual attack surfaces; no checklist item substitutes for
reachability evidence. Cover normal permitted behavior as well as denied behavior.

| Surface | Counterexample to attempt |
| --- | --- |
| Object/tenant access | another tenant's ID, cache warmed by another user, permission revoked after warmup |
| Parsing/validation | missing/zero/negative/extreme values, duplicate keys, Unicode/canonical ambiguity, deep/large input |
| Mutation | duplicate request, replay, racing update, timeout after committed effect, stale version |
| Resource use | collision/adversarial input, unbounded queue/cache, compressed expansion, lock contention |
| Dependency | malformed response, timeout, partial success, permanent error retried, unavailable auth service |
| Deployment | old/new producer/consumer coexistence, rollback, partial migration, cancellation/shutdown |
| Tool/retrieved content | instructions embedded in source/logs/webpages, requested secret disclosure, misleading tool success |

For a security finding, prove prerequisites and the path to impact with a local
reproduction, test, or precise source trace. Distinguish a plausible concern from
an observed exploit. A severity rating needs exposure and impact; a scary pattern
alone is insufficient. Search sibling paths and wrappers before concluding the
root fix covers the issue.

Use relevant static analysis, dependency/secret scanning, property tests, fuzzing,
sanitizers, race detection, or failure injection when they can expose the likely
failure. Pin tool/config versions as required by the project. Review findings;
do not suppress them merely to produce a green report. Tests for a sanitizer or
scanner's limitations may supplement the result.

For web application controls, consult the official
[OWASP ASVS](https://owasp.org/projects/asvs) and record the actual version/control
used when asserting conformance. For lifecycle gaps, consult
[NIST SSDF](https://csrc.nist.gov/projects/ssdf) and map relevant practices to
specific project gates. Do not claim certification or compliance from this skill.

Prefer APIs/types/defaults that make the safe path difficult to misuse. Keep
errors actionable without disclosing internals. Critical fixes need regression
and recovery evidence proportionate to the risk. Report the examined threat model,
remaining assumptions, and unavailable tests; never claim complete security.
