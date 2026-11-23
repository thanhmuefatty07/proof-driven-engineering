# Evaluation and Recovery Record: Unmerged Remote Branch `origin/codex/test-quality-portfolio-20261016`

## 1. Executive Summary

In accordance with Requirement R3 of the project upgrade mandate, this document records the comprehensive review, evaluation, and adopt/decline decisions for the unmerged remote branch `origin/codex/test-quality-portfolio-20261016`.

The branch contains 16 commits authored between 2026-10-16 and 2026-10-17 that advanced the skill through releases 0.4.1 to 0.4.5, focusing on minimal discriminating test sets, runtime verification, test-runner trust boundaries, and targeted mutation testing.

When commit `2f50e21` on `main` implemented Release 0.5.0 ("Add outcome-first architecture and bounded agent execution"), the majority of the testing quality text from this branch was integrated into `skills/proof-driven-engineering/references/testing-quality.md`. However, several high-leverage constraints, source citations, historical validation audit records, and Vietnamese translations were inadvertently condensed, omitted, or dropped.

This evaluation restores those omitted assets into `main` while declining changes that would regress 0.5.0 features. Furthermore, this record explicitly confirms that the remote branch `origin/codex/test-quality-portfolio-20261016` is preserved on GitHub and will not be deleted.

---

## 2. Branch Topology and Commit Chronology

- **Branch Name**: `origin/codex/test-quality-portfolio-20261016`
- **Base / Target Branch**: `main` (commit `2f50e21`, v0.5.0)
- **Common Ancestor**: Commit `374782b29db354d0e5f60090c0f123b8f7363094` ("Require realistic tests and bounded artifact lifecycles", 2026-10-16 02:20:31 +0700)
- **Total Divergent Commits**: 16 commits (`31141e1` through `4544825`)
- **Files Modified Across Branch**: Exactly 5 documentation/instruction files:
  1. `skills/proof-driven-engineering/references/testing-quality.md`
  2. `skills/proof-driven-engineering/SKILL.md`
  3. `SOURCES.md`
  4. `VALIDATION.md`
  5. `README.vi.md`
  *(Zero executable product files, test files, scripts, or evaluation cases were modified or added on this branch).*

### Commit Log Summary

| Commit | Author Date (UTC+7) | Version | Subject / Summary | Modified Files |
|---|---|---|---|---|
| `31141e1` | 2026-10-16 03:19:45 | 0.4.1 | Guide focused behavioral test portfolios | `README.vi.md`, `VALIDATION.md`, `SKILL.md`, `testing-quality.md` |
| `e169175` | 2026-10-16 09:56:14 | - | Clarify targeted mutation testing guidance | `testing-quality.md` |
| `f486214` | 2026-10-16 09:56:15 | 0.4.2 | Bump proof-driven-engineering to 0.4.2 | `SKILL.md` |
| `ce444ac` | 2026-10-16 09:56:17 | - | Document 0.4.2 mutation guidance | `README.vi.md` |
| `7f38387` | 2026-10-16 09:56:18 | - | Record test-quality research sources | `SOURCES.md` |
| `7439a1f` | 2026-10-16 09:56:20 | - | Record 0.4.2 validation status | `VALIDATION.md` |
| `b5b6710` | 2026-10-16 09:57:45 | - | Normalize testing-quality document newline | `testing-quality.md` |
| `06abd17` | 2026-10-16 10:46:28 | - | Clarify test runner evidence trust limits | `testing-quality.md` |
| `4a3f1bd` | 2026-10-16 10:46:35 | 0.4.3 | Bump proof-driven-engineering to 0.4.3 | `SKILL.md` |
| `5690da7` | 2026-10-16 13:55:06 | 0.4.4 | Require project-pinned runtimes for test evidence | `SKILL.md` |
| `9b0e583` | 2026-10-16 13:55:13 | - | Document runtime selection in test quality guidance | `testing-quality.md` |
| `8943e5f` | 2026-10-17 07:32:38 | - | Document test quality guidance through 0.4.4 | `README.vi.md` |
| `3c7c26d` | 2026-10-17 07:32:39 | - | Record validation limits for 0.4.3 and 0.4.4 | `VALIDATION.md` |
| `92e52f7` | 2026-10-17 11:41:20 | 0.4.5 | Require a minimal discriminating test case map | `SKILL.md` |
| `3653b40` | 2026-10-17 11:41:21 | - | Strengthen test portfolio selection and stop criteria | `testing-quality.md` |
| `4544825` | 2026-10-17 11:41:23 | - | Record validation limits for test portfolio guidance | `VALIDATION.md` |

---

## 3. Detailed File-by-File Survey and Evaluation

### 3.1 `skills/proof-driven-engineering/references/testing-quality.md`
- **Branch Content**: Defined compact case mapping formula, smallest discriminating test sets, stop criteria, targeted mutation testing sensitivity checks, runtime resolution from metadata/lockfiles, runner evidence trust boundaries, and primary citations to Google Testing Blog.
- **Main Status (`2f50e21`)**: `main` already incorporates 100% of the branch's substantive guidance and further adds lines 8–16: `## Diagnose before expanding tests` (instructing agents to inspect first failure, inputs, and invariants before multiplying cases).
- **Decision**: **Decline branch file / Retain `main`'s superset**. Overwriting `main` with the branch file would regress the causal diagnosis directive added in 0.5.0.

### 3.2 `skills/proof-driven-engineering/SKILL.md`
- **Branch Content**: Contained tight operational rules in Section 2 (runtime verification) and Section 3 (case mapping, fixture extension, stop criteria, and evidence-based removal).
- **Main Status (`2f50e21`)**: In condensing Section 3 to fit outcome-first architecture, several critical anti-bloat constraints were omitted.
- **Decision**: **Adopt / Recover specific omitted phrases into `main`**:
  1. Section 2: Append "...confirm the runtime it actually selected before interpreting failures."
  2. Section 3: Add "expected run/artifact cost" to the task-note case map requirement.
  3. Section 3: Add "extend the owning suite and fixtures by default".
  4. Section 3: Add stop condition: "report remaining boundaries as `NOT VERIFIED` instead of growing a speculative test matrix".
  5. Section 3: Add test removal constraint: "Remove tests only with behavior, boundary, and consumer evidence."

### 3.3 `SOURCES.md`
- **Branch Content**: Added `[Google Testing Blog: Keep Tests Focused (2018)]` to the primary sources table and added explanatory prose on 0.4.2 targeted mutation heuristics under "Chosen approach".
- **Main Status (`2f50e21`)**: Commit `2f50e21` retained links to the 2021 and 2024 Google Testing Blog posts in 0.5.0 but accidentally dropped the 2018 post from the table and condensed the mutation prose to a single sentence.
- **Decision**: **Adopt both recoveries into `SOURCES.md`**:
  1. Restore `[Google Testing Blog: Keep Tests Focused (2018)]` in the primary sources table.
  2. Restore the 0.4.2 mutation guidance prose explaining why mutation testing is a diagnostic sensitivity check rather than an acceptance gate.

### 3.4 `VALIDATION.md`
- **Branch Content**: Maintained rigorous validation logs and explicit `NOT VERIFIED` boundary tables for Releases 0.4.1, 0.4.2, 0.4.3, 0.4.4, and 0.4.5.
- **Main Status (`2f50e21`)**: Commit `2f50e21` replaced all five release records with a single summary sentence in Release 0.5.0.
- **Decision**: **Adopt / Restore Releases 0.4.1 through 0.4.5 into `VALIDATION.md`** between Release 0.5.0 and Release 0.4.0. Preserving the historical audit trail directly adheres to Requirement R2 and the core principles of proof-driven engineering.

### 3.5 `README.vi.md`
- **Branch Content**: Included a rich 13-line paragraph in Vietnamese explaining the 0.4.4 test quality guidance, mutation testing criteria, runner trust limits, and independent OS observer requirements.
- **Main Status (`2f50e21`)**: Condensed into a generic 6-line summary that lost all explanation of mutation testing and runner trust.
- **Decision**: **Adopt rich Vietnamese translation into `README.vi.md`**, ensuring conceptual and documentation parity for Vietnamese readers.

### 3.6 Other Repository Files (`README.md`, `agents/openai.yaml`, `evals/`, `tests/`)
- **Branch Content**: Retained older 0.4.x text; contained no new evals or tests.
- **Main Status (`2f50e21`)**: Updated `README.md` and `agents/openai.yaml` to 0.5.0 outcome-first architecture; added two behavioral eval cases (`diagnosis-before-test-growth`, `exhausted-pr-review-budget`).
- **Decision**: **Decline branch versions / Retain `main`'s versions**.

---

## 4. Itemized Adopt / Decline Decision Matrix (Requirement R3)

| Recommendation ID | Component / Target | Proposed Action | Rationale |
|---|---|---|---|
| **REC-01** | `testing-quality.md` | **Decline branch file / Retain `main`'s superset** | `main` incorporates all branch material and adds `## Diagnose before expanding tests`. Overwriting would regress `main`. |
| **REC-02** | `SKILL.md` (Sec. 2) | **Adopt** | Adding "...confirm the runtime it actually selected before interpreting failures" prevents agents from confusing runtime version mismatches with product bugs. |
| **REC-03** | `SKILL.md` (Sec. 3) | **Adopt** | Mandating "expected run/artifact cost" in the task-note case map prevents runaway test execution costs. |
| **REC-04** | `SKILL.md` (Sec. 3) | **Adopt** | Mandating "report remaining boundaries as `NOT VERIFIED` instead of growing a speculative test matrix" prevents hallucinated tests. |
| **REC-05** | `SKILL.md` (Sec. 3) | **Adopt** | Requiring "Remove tests only with behavior, boundary, and consumer evidence" prevents reckless test deletion. |
| **REC-06** | `SKILL.md` (Sec. 3) | **Adopt** | Directing agents to "extend the owning suite and fixtures by default" avoids test file sprawl. |
| **REC-07** | `SOURCES.md` (Table) | **Adopt** | Restores citation `[Google Testing Blog: Keep Tests Focused (2018)]` linked by `testing-quality.md`. |
| **REC-08** | `SOURCES.md` (Prose) | **Adopt** | Restores 0.4.2 mutation testing heuristics under "Chosen approach". |
| **REC-09** | `VALIDATION.md` | **Adopt** | Restores historical validation audit records and `NOT VERIFIED` tables for Releases 0.4.1–0.4.5 between 0.4.0 and 0.5.0. |
| **REC-10** | `README.vi.md` | **Adopt** | Restores rich 13-line Vietnamese translation of test quality, mutation, and runner trust rules. |
| **REC-11** | `README.md` & `openai.yaml` | **Decline branch versions** | Superseded by 0.5.0 outcome-first architecture framing on `main`. |
| **REC-12** | Remote Branch Retention | **Retain Branch** | Branch `origin/codex/test-quality-portfolio-20261016` is preserved on GitHub and will not be deleted per R3. |

---

## 5. Branch Preservation Confirmation

Per Requirement R3 ("Do not delete the branch"):
- Remote tracking branch: `refs/remotes/origin/codex/test-quality-portfolio-20261016`
- **Confirmation**: The branch `origin/codex/test-quality-portfolio-20261016` remains intact on GitHub. No commands deleting, force-pushing over, or modifying this remote branch will be executed. It remains permanently available as historical reference and derivation provenance.

---

## 6. Verification and Integrity Check

1. **Test Suite Verification**:
   - `python -m pytest -v`: 23 passed, 1 skipped (symlink test on Windows).
2. **Link and Reference Resolution**:
   - `tests/test_package.py:test_local_references_resolve_within_the_distribution`: passed with all relative markdown references resolving.
3. **Diff Whitespace Check**:
   - `git diff --check`: clean exit (code 0).
