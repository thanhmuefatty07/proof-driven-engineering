## Engineering workflow

For substantive implementation, debugging, architecture, performance work, and
code review, use the installed `proof-driven-engineering` skill. Explicitly invoke
`$proof-driven-engineering` when automatic selection is uncertain. Read its entry
point and only the references needed by the task.

Keep the user's current objective, constraints, authorization, and acceptance
checks recoverable across interruptions. Optimize measured performance within
correctness, security, compatibility, and resource constraints. Verify the actual
result and invalidate evidence when its inputs change. Keep trivial work light.

For testing, read the skill's `references/testing-quality.md`: identify the real
defect and independent oracle, exercise the boundary needed by the claim, and
complete required gates without redundant reruns. Own and bound temporary data
before generating it; reuse compatible build caches and verify cleanup. Update
one milestone checkpoint in the configured private location. Keep local archive
paths and raw evidence out of published files.

The skill does not override host/user/repository rules or grant new permissions.
If it is unavailable, apply the existing project rules and report that limit;
do not claim the skill ran. Use existing automated project gates for enforcement.
