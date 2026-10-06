# Proof-Driven Engineering

Performance-first coding, adversarial review, and verifiable acceptance for coding
agents. One portable skill, with focused references loaded only when needed.

[Vietnamese guide](README.vi.md) | [Skill](skills/proof-driven-engineering/SKILL.md) |
[Research decisions](SOURCES.md) | [Evaluation protocol](evals/README.md)

## What it changes

- Optimize the measured bottleneck under correctness, security, and resource constraints.
- Permit complex techniques when comparable measurements justify their benefit.
- Trace architectural ownership and producer/consumer contracts before changing them.
- Ground dependency identity, resolved versions, imports, APIs, flags, and configuration in primary evidence before integration.
- Challenge authorization, caches, concurrency, malformed input, and failure recovery.
- Keep the current user objective and acceptance criteria across steering and compaction.
- Reconcile ambiguous tool writes, diagnose errors, and verify actual resulting state.
- Omit narrating comments and speculative scaffolding; retain necessary invariants/licenses.
- Require evidence before completion, performance, or security claims.

A skill supplies instructions. It cannot guarantee optimal code, eliminate all
defects, grant tool permissions, or force a model to obey. Automated project gates
remain essential. This release is an initial evaluated workflow, not a claim of
superiority over other skills. See [validation status](VALIDATION.md).

## Install in Codex

Ask the built-in installer:

```text
Use $skill-installer to install skills/proof-driven-engineering from
https://github.com/thanhmuefatty07/proof-driven-engineering.
```

For a reviewed local checkout on Windows:

```powershell
git clone https://github.com/thanhmuefatty07/proof-driven-engineering.git
Set-Location proof-driven-engineering
$skillDestination = Join-Path $env:USERPROFILE '.agents/skills/proof-driven-engineering'
if (Test-Path -LiteralPath $skillDestination) { throw 'Skill already exists; review before updating.' }
New-Item -ItemType Directory -Force -Path (Split-Path $skillDestination) | Out-Null
Copy-Item -LiteralPath './skills/proof-driven-engineering' -Destination $skillDestination -Recurse
```

The supported user discovery location is `~/.agents/skills`; other hosts may use
different locations. Codex allows automatic matching by description and explicit
`$proof-driven-engineering` invocation. See the official
[skill discovery documentation](https://learn.chatgpt.com/docs/build-skills).
If discovery has not refreshed, restart Codex. Installing enables discovery;
automatic selection is not guaranteed on every task.

## Use

```text
Use $proof-driven-engineering to implement this change. Preserve the public
contract, optimize the measured hot path, and verify the relevant negative cases.
```

For optimization, supply the workload, platform, target metric, and resource
limits when known. For review, supply the diff/base and request review explicitly.
The skill treats review as read-only unless fixes are also authorized.

For consistent project routing, merge the small
[AGENTS.md fragment](integrations/AGENTS.fragment.md) into your existing rules
after reviewing conflicts. It references one authority instead of repeating the
full skill. This repository does not automatically edit host rules or settings.

## Layout

```text
skills/proof-driven-engineering/
  SKILL.md
  agents/openai.yaml
  references/                 Architecture, security, dependency grounding, continuity, verification
  scripts/check_evidence.py    Optional recorded-coverage/freshness gate
evals/                        Synthetic behavioral prompts and fixtures
tests/                        Package and evidence-gate checks
integrations/                 Optional host rule fragment
```

The instructions have no runtime dependencies or mandatory sibling skills.
The optional evidence gate uses Python 3.11+ and the standard library. Its checks
cannot attest command execution or infer omitted requirements.

## Validate a checkout

```sh
python -m pip install -r requirements-dev.txt
python -m unittest discover -s tests -v
python -m unittest discover -s evals/fixtures/catalog -v
git diff --check
```

PyYAML is a pinned development dependency for validating the actual YAML consumed
by skill hosts. CI is configured for package/gate/fixture checks on Windows and Linux. It does
not invoke paid models, run performance workloads, or upload raw traces.

Behavioral evaluations are separate: exercise a model on isolated fixture copies,
inspect its artifacts and actions, and score the acceptance rubrics. Compare with
a baseline on held-out tasks before claiming that this skill improves outcomes
or token usage. [Contributing](CONTRIBUTING.md) describes the evidence expected.

## License

Original project content is [MIT licensed](LICENSE). [SOURCES.md](SOURCES.md)
records upstream research and licensing boundaries. No upstream skill bundles
or proprietary project files are vendored.
