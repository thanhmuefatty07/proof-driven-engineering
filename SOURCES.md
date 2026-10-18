# Research and Design Decisions

Initial review on 2026-10-07. Sources were selected for a concrete mechanism, inspectable
primary material, applicability, and evaluability. This is a scoped comparison,
not a ranking of the world's best skills. Popularity was used only for discovery.

| Primary source | Mechanism used in this project | Boundary |
| --- | --- | --- |
| [OpenAI skill documentation](https://learn.chatgpt.com/docs/build-skills) | Portable manifest, precise trigger, progressive loading, local discovery | Discovery is not guaranteed compliance |
| [OpenAI skill eval guidance](https://developers.openai.com/blog/eval-skills) | Observable outcome/process criteria and consuming-agent evaluation | Manifest tests alone cannot assess behavior |
| [OpenAI instruction/context guidance](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra) | Compact scope and conditional references | More instruction text is not evidence of higher quality |
| [Superpowers debugging](https://github.com/obra/superpowers/blob/8ca22dba9a94f28898bbce59f2537ff4d87c747d/skills/systematic-debugging/SKILL.md) | Reproduction, causal investigation, discriminating experiments | Avoid rigid ritual for low-impact work or printing sensitive diagnostics |
| [Anthropic skill creator](https://github.com/anthropics/skills/blob/683bc88e56f3e09ba94f7055977f3d3aa499f202/skills/skill-creator/SKILL.md) | Realistic test prompts, independent execution, iterative evaluation | Host-specific tools/procedures are not copied |
| [Trail of Bits differential review](https://github.com/trailofbits/skills/blob/82fe8226252622fa807643bdca1710901198553a/plugins/differential-review/skills/differential-review/SKILL.md) | Risk, callers, contract impact, concrete adversarial findings | No mandatory public audit dump or automatic high severity |
| [Trail of Bits sharp edges](https://github.com/trailofbits/skills/blob/82fe8226252622fa807643bdca1710901198553a/plugins/sharp-edges/skills/sharp-edges/SKILL.md) | Misuse-resistant defaults and boundary invariants | Do not force incompatible migrations without a safe path |
| [Vercel performance skills](https://github.com/vercel-labs/agent-skills/blob/063bee94c3f4df8453406c830b0a7df0f2860278/skills/react-best-practices/SKILL.md) | Prioritize high-impact costs before small instruction-level changes | React-specific recommendations remain domain-specific |
| [OWASP ASVS](https://owasp.org/projects/asvs) | Applicable security requirements become explicit controls/tests | No implied ASVS certification; record versions for conformance claims |
| [NIST SSDF](https://csrc.nist.gov/projects/ssdf) | Secure development and response grounded in risk and outcomes | This skill is not an organizational compliance program |
| [USENIX package-hallucination research, authors' summary](https://www.usenix.org/publications/loginonline/we-have-package-you-comprehensive-analysis-package-hallucinations-code) | Explicit checks against invented dependency names and their supply-chain consequences | Historical model observations do not predict this skill's failure rate |
| [PyPA distribution/import distinction](https://packaging.python.org/en/latest/discussions/distribution-package-vs-import-package/) | Verify installation-name to import-name mapping; do not install by guessed import | Python naming rules are not imposed on other ecosystems |
| [pip secure installs](https://pip.pypa.io/en/stable/topics/secure-installs/) | Inspect execution/integrity risks before installation; preserve approved hash controls | Artifact integrity does not prove benign behavior; flags depend on the actual tool version |
| [pip index-source warning](https://pip.pypa.io/en/stable/cli/pip_install/#cmdoption-extra-index-url) | Treat private/public index substitution as a dependency-confusion boundary | No automatic registry rewrites |
| [npm lockfile reference, v11](https://docs.npmjs.com/cli/v11/configuring-npm/package-lock-json/) | Check resolved artifact identity, version, integrity, and installation-script metadata | npm-specific fields require the matching CLI/lockfile format |
| [Python hashlib reference, 3.11](https://docs.python.org/3.11/library/hashlib.html) | Version-matched API and digest behavior for the synthetic grounding eval | The local runtime must still be inspected; later patch-level docs are not exact-binary evidence |

## Chosen approach

The 0.4.0 test lifecycle sources below were reviewed on 2026-10-16. The update uses the official
[pytest temporary-directory guide](https://docs.pytest.org/en/stable/how-to/tmp_path.html)
and [fixture teardown guide](https://docs.pytest.org/en/stable/how-to/fixtures.html#teardown-cleanup-aka-fixture-finalization).
They inform ownership, retention and teardown decisions, including the danger of
reusing an explicit base temporary directory. Actual runner versions and cleanup
behavior must still be verified. The
[official Codex instruction guide](https://developers.openai.com/codex/guides/agents-md)
informs optional host integration; editing a skill does not itself change global
instructions or enforce a filesystem quota.

Keep one performance-first engineering workflow with specialized references.
Performance is optimized among candidates that preserve required correctness,
security, compatibility, and resources. Complexity is allowed when its benefit
is demonstrated; it is never the objective itself. A per-line aesthetic cannot
substitute for the behavior and cost of the complete path.

A broad always-loaded constitution was considered but would repeat host/project
policies and unrelated details. A bundle of many mandatory skills was considered
but would depend on host discovery and add conflicting process rules. This
project instead keeps one portable entry point, optional mechanical evidence
validation, and explicit project integration.

## Outcome and execution policy, 0.5.0

Reviewed on 2026-10-18 using Exa discovery followed by the primary pages below
and the OpenAI skill-evaluation source already listed above. These are decision
inputs, not copied instructions or comparative skill scores.

| Primary source | Applied mechanism | Boundary |
| --- | --- | --- |
| [SEI software architecture](https://www.sei.cmu.edu/software-architecture/) | Relate system structure and quality attributes to the user's outcome before implementation | Use a task-sized system model, not a mandatory heavyweight architecture exercise |
| [Google code review standard](https://google.github.io/eng-practices/review/reviewer/standard.html) | Evidence over preferences; resolve review deadlock rather than pursue unattainable perfection | Google does not prescribe this skill's three-round cap |
| [Google review scope](https://google.github.io/eng-practices/review/reviewer/looking-for.html) | Inspect design, behavior, concurrency and whether test assertions reject broken code | A checklist or clean scan alone is not correctness evidence |
| [Anthropic effective agents](https://www.anthropic.com/engineering/building-effective-agents) | Match decomposition and tools to the task; use environmental feedback and stopping criteria | The engineering patterns are not evidence for current SDK flags, host permissions, or automatic performance gains |
| [Google mutation testing](https://testing.googleblog.com/2021/04/mutation-testing.html) | Challenge material assertions with relevant wrong behavior rather than generate redundant mutants | No mandatory mutation-score target or exhaustive mutant matrix |
| [Google test fidelity](https://testing.googleblog.com/2024/02/increase-test-fidelity-by-avoiding-mocks.html) | Prefer the smallest real boundary that supports the claim; disclose substitutes | This does not authorize production calls or prohibit controlled failure doubles |

The maximum of three coordinated review rounds and the default prohibition on
generated explanatory code comments are explicit user policy choices, not claims
that these sources require them. Required legal/functional/contract content and
higher-priority instructions remain intact. Exhausted review budgets with
unresolved blockers require handoff, not approval. Existing local 0.4.5 guidance
on test portfolios, runtime selection, targeted mutation, and evidence authenticity
is retained. The update makes no claim of globally optimal lines, exhaustive
diagnosis, or guaranteed model compliance.

## Attribution and licensing

This project uses independently written instructions and original synthetic
fixtures. Referenced upstream text/code has not been copied into the distribution.
Links preserve provenance; upstream materials retain their respective licenses,
including share-alike terms where applicable. MIT applies to original content in
this repository, not to linked upstream repositories or standards. Incorporating
upstream text/code in a future contribution requires a separate license review.
