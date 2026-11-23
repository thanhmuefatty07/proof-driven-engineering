# Dependency and API Grounding

Use before introducing or changing an unfamiliar/version-sensitive dependency,
API call, tool option, configuration key, or protocol integration. Apply the
same discipline to standard libraries; familiarity is not evidence for a newly
proposed symbol. Reuse verified unchanged evidence instead of researching every
line again.

## Establish identity before installation

Inspect the project manifest, lockfile, configured registry/source, installed
metadata, runtime, target platform, and relevant build settings. Distinguish a
declared version range from the resolved and actually running version. Do not
silently upgrade the project to match a newer documentation example.

Confirm the ecosystem's distribution name, import/namespace name, owner/upstream,
release, and artifact source separately. Under PyPA and packaging standards (PEP 508,
PEP 517, PEP 621), distribution names (what a package manager installs) often differ
from import module namespaces (e.g., `PyYAML` provides `yaml`, `beautifulsoup4` provides
`bs4`, `scikit-learn` provides `sklearn`). Never assume an import name can be installed
directly. Verify the mapping from trusted project metadata or upstream source.

Large language models hallucinate package names at rates between 5.2% and 21.7%
(Lazaar et al., USENIX Security 2024). Attackers actively exploit this via "slopsquatting,"
monitoring generated code patterns to register phantom package names on PyPI, npm, or
crates.io containing malicious payloads. Agents are strictly forbidden from speculative
dependency installation: never run `pip install`, `npm install`, or `cargo add` to resolve
a `ModuleNotFoundError` or missing import unless the user explicitly requested adding that
specific package.

For a new dependency, cross-check the official upstream release against trusted
registry metadata before any installation. A registered name, popularity, or
successful download does not establish intended identity or safety. Challenge
typosquatting, model-invented names later registered by attackers, private/public
dependency confusion, unexpected aliases, and transitive/lifecycle execution.
Do not probe an unknown package by installing or importing it. Inspect metadata
and source without execution first; authorized execution belongs in an isolated
environment. Keep credentials and private package names out of public searches.

Use the project's approved sources, locking, artifact-integrity, and provenance
controls. Review meaningful lockfile/transitive changes. Pinning or hashes retain
the selected artifact; neither proves that its code is benign. Do not disable
integrity checks or add an untrusted registry to satisfy a missing import.

## Prove the surface and its behavior

Execute the strict **3-Stage Grounding Protocol**:

1. **Stage 1 (Identity):** Confirm package identity and exact resolved version
   in project lockfiles or manifests (`pyproject.toml`, `requirements.txt`,
   `package-lock.json`, `Cargo.lock`). Distinguish declared ranges from installed versions.
2. **Stage 2 (Surface Inspection):** Inspect version-matched export symbols, classes,
   and functions using safe runtime reflection (e.g. `python -c "import mod; print(dir(mod))"`,
   `inspect.signature()`, or static type stubs `.pyi`). Never guess parameter names,
   optional flags, or return shapes. If a signature is unavailable to reflection,
   use official version-matched documentation and source; do not fabricate it.
3. **Stage 3 (Target Probe):** Execute a minimal 1-line or 1-call integration probe
   in the target environment before writing consumer code. Include negative and
   boundary cases where important assumptions can fail. A mock that accepts invented
   members cannot validate a third-party contract; successful import/compilation alone
   does not prove runtime semantics. Never patch a dependency or invent a compatibility
   shim merely to hide an unsupported call.

Unsupported symbol/argument errors reject the current hypothesis. Reinspect the
installed version, import shadowing, documented surface, and call shape before
changing code. Do not try random names/flags, broad catches, unsafe type escapes,
fabricated responses, or skipped validation until something appears to work.

## Evidence and stopping conditions

Keep a compact record when needed: `assumption -> identity/version -> primary
source or local path/hash -> probe/check and actual result -> remaining limit`.
Invalidate it when dependency resolution, source, configuration, platform, or
runtime changes. Project evidence stays in an approved local/private location.

When offline or documentation is incomplete, use trusted installed source/types
and a bounded local probe, or a verified existing primitive. If the required
contract remains unknown, mark that requirement `NOT VERIFIED - reason` and ask
only for the missing access/decision that actually blocks it. Do not substitute
an unrequested architecture or invent an implementation of a vendor contract.

Broaden research when primary sources disagree or leave a material assumption
open. Stop when identity, version, surface, behavior, and affected acceptance are
established at the required risk level. Source count is not a quality metric.

## Primary references

- [USENIX Security: Package Hallucinations (Lazaar et al., 2024)](https://www.usenix.org/conference/usenixsecurity24/presentation/lazaar)
- [PyPA Distribution Package vs Import Package](https://packaging.python.org/en/latest/discussions/distribution-package-vs-import-package/)
- [PEP 508 - Dependency specification for Python Software](https://peps.python.org/pep-0508/)
