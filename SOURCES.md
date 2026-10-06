# Research and Design Decisions

Reviewed on 2026-10-07. Sources were selected for a concrete mechanism, inspectable
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

## Attribution and licensing

This project uses independently written instructions and original synthetic
fixtures. Referenced upstream text/code has not been copied into the distribution.
Links preserve provenance; upstream materials retain their respective licenses,
including share-alike terms where applicable. MIT applies to original content in
this repository, not to linked upstream repositories or standards. Incorporating
upstream text/code in a future contribution requires a separate license review.
