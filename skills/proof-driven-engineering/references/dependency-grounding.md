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
release, and artifact source separately. These names need not match: in Python,
distribution names do not establish which import modules they provide. Verify
the mapping from trusted project metadata or upstream documentation/source.

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

Prefer version-matched official reference/specification and upstream source,
then shipped types/stubs, actual schemas/help, and safe inspection of already
trusted local code. A latest-version example, generated answer, search snippet,
or unrelated package with a similar name cannot establish support.

For each new assumption, check the applicable export/import path, signature,
parameter names/types/defaults, return shape, sync/async behavior, errors,
cancellation, units, side effects, and platform/version constraints. Record only
decision-relevant facts, not a copied manual. If a signature is unavailable to
reflection, use source/types/docs and a bounded behavior probe; do not fabricate
it. Resolve disagreements with the actual target version and its changelog.

Exercise a minimal real integration in the target environment, then the affected
project compiler/type/build and behavioral checks. Include negative/boundary
cases where important assumptions can fail. A mock that accepts invented members
cannot validate a third-party contract; successful import/compilation alone does
not prove runtime semantics. Never patch a dependency or invent a compatibility
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
