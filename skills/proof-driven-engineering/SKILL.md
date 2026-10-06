---
name: proof-driven-engineering
description: Performance-first implementation, debugging, architecture, and code review with adversarial security checks, requirement continuity, and measured acceptance. Use for substantive repository changes or optimization; keep trivial edits lightweight.
license: MIT
metadata:
  version: "0.1.0"
---

# Proof-Driven Engineering

Deliver the user's requested behavior with the highest demonstrated performance
within correctness, security, compatibility, and resource constraints. Treat
complexity as an available engineering tool: accept it when evidence justifies
the gain. Source brevity, instruction count, and sophistication are not runtime
performance. This workflow supplies bounded evidence, not a universal optimum
or a guarantee of zero defects.

Host instructions, the user's authorization, and applicable repository rules
take precedence. This skill grants no new permissions, tool access, or authority
to exploit, publish, delete, deploy, or contact anyone.

## 1. Preserve the task

Before substantive work, retain a compact task contract in host-native state:

`objective | active user constraints | acceptance checks | authorized effects |
scope/ownership | current inputs | evidence | unresolved issues | next action`.

Keep concrete requirements individually traceable to acceptance evidence. Keep
the original objective during status questions and compatible user steering;
replace it only when the user cancels or requests an incompatible outcome.
Update the contract on new instructions, consequential decisions, failure, and
before a context handoff. Read [continuity-tools.md](references/continuity-tools.md)
for long tasks, interrupted work, external writes, or unreliable tools.

After interruption or compaction, reconcile that state with the latest user
messages and actual files before the next edit or final answer. Missing context
is an unknown, not authorization. Do useful independent work while clarification
is pending; proceed on optional details with a stated reasonable assumption.

## 2. Find the owner and define success

Inspect the working tree and relevant local instructions before editing.
Preserve existing user changes. Locate the authoritative definition, important
callers, consumers, tests, and serialized/configuration boundaries. Inspect actual
dependency/runtime versions when behavior is version-dependent.

Scale evidence to the change:

- **Local:** affected logic, callers, targeted checks.
- **Contract:** producers and consumers, compatibility, affected build/tests.
- **Critical:** assets and trust boundaries, threat/failure model, negative
  tests, concurrency/recovery where relevant, deployment and rollback assumptions.

State observable acceptance before implementation. Identify at least one
credible alternative and a cheap falsifier when the choice is consequential.
For bugs, reproduce and isolate the violated invariant before changing its causal
owner. A bug hypothesis must explain the observed failure.

## 3. Choose and build for performance

For performance work or architecture that affects capacity, read
[architecture-performance.md](references/architecture-performance.md).

Identify the target workload, platform, budgets, and objective metric. Use a
representative baseline and profile the critical path. Optimize the largest
relevant cost first: algorithm/data layout, I/O/query plan, batching, allocation,
serialization, synchronization, then measured low-level costs.

Prefer the fastest demonstrated feasible candidate under the user's constraints.
Permit specialized structures, native code, SIMD, pooling, parallelism, or caching
when the workload and evidence justify them. Require explicit ownership,
invalidation, resource bounds, compatibility, and failure behavior. At comparable
performance, prefer the smaller reversible change. Do not remove security checks,
change numeric/ordering semantics, or assume a particular compiler/hardware to
manufacture a win.

Keep the semantic diff coherent and scoped. Reuse existing project primitives
before adding dependencies or new layers. Do not impose architectures, rewrite
unrelated modules, or change a language/framework without a required benefit.

For meaningful behavior changes, establish a test or executable acceptance oracle
that can detect the relevant mistake. Fixes should leave a regression check when
feasible. Respect required local testing rules and report unavailable checks.
Turn critical invariants into types, validation, constraints, or tests at their
owning boundary instead of relying on future agents to remember them.

Omit comments that narrate code, decorative banners, agent explanations, and
speculative TODOs. Keep a short comment only when it preserves a non-obvious
invariant, protocol quirk, security requirement, concurrency rule, or measured
trade-off. Preserve required license notices and public contract documentation.
Do not minify or obscure source without a measured deployment/runtime benefit.

## 4. Attack the assumptions

For trust boundaries, sensitive operations, or critical changes, read
[security-red-team.md](references/security-red-team.md). Review during design and
implementation as well as at the end.

For each exposed path, ask: what can the caller/attacker control, where is the
decision enforced, and which observable counterexample breaks the invariant?
Exercise relevant denied access, malformed/oversized input, duplicate execution,
concurrent mutation, stale state, dependency failure, cancellation, and partial
deployment. Use isolated synthetic inputs within authorization.

For performance changes, specifically challenge cache ownership, stale values,
aliasing, contention, bounded memory, cancellation, backpressure, timing behavior,
and adversarial worst cases. If a claim is seriously wrong, identify the most
likely hidden failure and attempt to expose it. Record the check and its limit;
an empty scanner report is not proof of security.

## 5. Use tools with state awareness

Choose the smallest reliable capability that resolves the current unknown.
Prefer structured APIs and parsers; inspect schemas/help/version instead of
guessing flags. Search before broad reads; fetch relevant ranges; cache evidence
until inputs change. Batch independent reads and serialize dependent mutations.

Check tool exit codes, errors, truncation, pagination, partial results, and actual
post-write state. Diagnose failures and change the method when evidence rejects
it. A missing tool or permission must remain visible. Never fabricate tool output,
silently disable checks, retry forever, or exceed authorization to finish.

A timeout after a write leaves its outcome unknown: inspect the receipt/target
before retrying. Do not replay a non-idempotent effect blindly. Follow host job
semantics, use event-driven completion where provided, and avoid status polling
that adds no decision-relevant evidence. Continue independent work while waiting.

Delegate only when authorized, useful, and supported. Give disjoint ownership,
minimal relevant context, concrete acceptance, and bounded effects. Review the
actual artifacts and rerun affected checks before trusting a worker's conclusion.

## 6. Review, verify, and finish

Read [review-verification.md](references/review-verification.md) for formal review,
contract/critical changes, or disputed verification. A review request is read-only
unless the user also authorizes fixes.

Map each requirement to current evidence. Run the required affected checks and
read their results. Invalidate evidence after changes to its inputs. Inspect the
complete final diff, stale references, generated boundaries, unintended files,
local/private data, and publication scope. Remove changes without a requirement,
invariant, compatibility need, or verification purpose.

For long or critical work, the optional
[check_evidence.py](scripts/check_evidence.py) validates a JSON completion record
against current input hashes. Its
[record contract](references/review-verification.md#optional-evidence-gate) is
loaded only when using it. It never executes recorded commands and cannot prove
that an agent ran them or included every relevant input.

Report the result, decisive checks, and residual uncertainty. Distinguish
`MEASURED`, `VERIFIED within scope`, `SOURCE-BACKED`, `INFERRED`, and
`NOT VERIFIED - reason` when material. No invented confidence scores, benchmark
wins, completeness, security, or production-readiness claims. For implementation
requests, resolve actionable in-scope failures; for review-only tasks, report
them. Report remaining blockers honestly. Stop optional investigation
when it is unlikely to change the result, while completing required verification.
