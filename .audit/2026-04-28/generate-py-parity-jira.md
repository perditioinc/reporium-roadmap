# KAN-ROADMAP-generate-py-parity — JIRA fallback

**Lane:** generate-py-parity
**Date:** 2026-04-28
**Branch:** `claude/feature/KAN-ROADMAP-generate-py-parity`
**Base / target:** `main`
**JIRA:** unavailable in shell at time of writing; this file is the
JIRA-first fallback per the lane process rule.
**Owned files:** `generate.py`, `tests/test_generate.py`,
`.audit/2026-04-28/generate-py-parity-jira.md`

---

## Why this lane exists

PR #10 (`KAN-ROADMAP: roadmap sync v0.8.0 → v0.8.3`, merged 2026-04-26T00:08:03Z)
added the following hand-written sections to `README.md`:

- `## Solved Lanes — do not re-open` (8 entries, sourced from
  `roadmap.json:solved_lanes.entries`)
- `## Historical Targets` (1 entry, sourced from
  `roadmap.json:historical_targets`)
- Per-repo `Main HEAD <sha>` strings inside working entries' `evidence` fields
- All v0.8.x changelog entries (v0.8.4 / v0.8.3 / v0.8.2 / v0.8.1 / v0.8.0)
- A `Last updated:` footer date tied to the roadmap `as_of` field

The nightly `update.yml` workflow runs `generate.py` and force-commits the
regenerated README. Three post-merge nightly runs (build 41 on 2026-04-26,
build 42 on 2026-04-27, build 43 on 2026-04-28) **silently overwrote** the
`## Solved Lanes` and `## Historical Targets` sections because `build_readme`
did not read those keys from `roadmap.json`.

This was anticipated in the PR #10 body:
> **`generate.py` parity gap.** The README contains hand-written sections
> (Solved Lanes, Historical Targets, explicit per-repo HEADs in Working
> evidence, the v0.8.x changelog blocks) that `generate.py:build_readme`
> does not produce. The next nightly auto-build workflow will overwrite
> these unless `generate.py` is taught about them.
> Suggested separate lane: `KAN-ROADMAP-generate-py-parity`.

---

## Gap validation (2026-04-28)

```
python -c "from generate import load_roadmap, build_readme; \
  print(build_readme(load_roadmap(), {}, '2026-04-28'))" \
  > /tmp/regenerated_readme.md
diff README.md /tmp/regenerated_readme.md
# → empty diff: live README and generated README are identical
# → confirmed: solved_lanes and historical_targets already overwritten
```

The live `README.md` on `main` as of 2026-04-28 has no `## Solved Lanes` or
`## Historical Targets` sections. The nightly has already caused the loss.

### Keys NOT read by build_readme (pre-fix)

| roadmap.json key | Pre-fix | Post-fix |
|---|---|---|
| `solved_lanes.entries` | ❌ ignored | ✅ `_solved_lanes_section()` |
| `historical_targets` | ❌ ignored | ✅ `_historical_targets_section()` |
| `current_state.not_working` | ✅ already rendered | ✅ unchanged |
| `changelog[]` (all entries) | ✅ all 13 rendered | ✅ unchanged |
| working evidence verbatim | ✅ already passed through | ✅ regression test added |
| `as_of` (footer date) | ❌ not used (`generated_at[:10]`) | ✅ `last_updated = roadmap.get("as_of") or generated_at[:10]` |

---

## What changed

### `generate.py`

Two new private renderer functions (no public API change):

- `_solved_lanes_section(roadmap)` — reads `roadmap["solved_lanes"]`, renders
  note + each entry's `lane`/`repo`/`resolved_by`/`date`/`summary`. Returns
  `""` when the key is absent or `entries` is empty (safe omission).
- `_historical_targets_section(roadmap)` — reads `roadmap["historical_targets"]`,
  renders each entry's `claim`/`stated_in`/`outcome_as_of_*`. Returns `""` when
  the key is absent (safe omission).

`build_readme` updated:

- Calls both new helpers; includes each section conditionally between Coming
  Next and Changelog (separated by `---` dividers only when content is present).
- Footer date now uses `roadmap.get("as_of") or generated_at[:10]` so the
  "Last updated:" line reflects when the roadmap was curated, not when the
  nightly ran.

Public function signatures are **unchanged**: `build_readme`, `load_roadmap`,
`_format_item`, `_apply_context`, `_apply_context_to_items`,
`_count_repo_tests`, `_fetch_db_stats`, `_fetch_repo_stats` all retain their
existing signatures and behaviour.

### `tests/test_generate.py`

Six new tests added (35 → 41 total, all passing):

1. `test_solved_lanes_renders_when_present` — heading and entry content appear
2. `test_solved_lanes_omitted_when_absent` — no heading when key missing
3. `test_historical_targets_renders_when_present` — heading and claim appear
4. `test_historical_targets_omitted_when_absent` — no heading when key missing
5. `test_changelog_all_entries_rendered_in_order` — 3-entry list stays in order
6. `test_working_evidence_main_head_survives_render` — `Main HEAD \`4c5f2f3\``
   passes through verbatim (regression guard against future template changes)

---

## Sections intentionally not made generator-backed

| Section | Decision | Rationale |
|---|---|---|
| `REPORIUM_ROADMAP.md` | **Not touched** | It is an extended architecture doc with tables, phases, and prose that have no counterpart in `roadmap.json`. Making it generator-backed would require a major schema extension that is out of scope for a parity lane. |
| Badge block (`<!-- perditio-badges-start -->`) | **Not touched** | Already correct; constraint in lane brief. |
| Nightly `update.yml` workflow | **Not touched** | Constraint in lane brief. |

---

## Stop conditions honored

- No application repos modified.
- No PRs merged or deployed.
- `roadmap.json` and `README.md` not edited (the README will be regenerated
  correctly by the next nightly run once this branch lands on main).
- No public function signatures changed.
- All 41 tests green.

---

## Acceptance criteria

- [x] `## Solved Lanes — do not re-open` appears in rendered README when
      `solved_lanes.entries` is non-empty in `roadmap.json`.
- [x] `## Solved Lanes` is absent when key is missing.
- [x] `## Historical Targets` appears in rendered README when
      `historical_targets` is non-empty.
- [x] `## Historical Targets` is absent when key is missing.
- [x] All 13 changelog entries render in declared order.
- [x] `Main HEAD \`4c5f2f3\`` in a working entry's evidence survives rendering.
- [x] `python -m pytest tests/test_generate.py` — 41 passed.
- [x] Footer uses `roadmap.json:as_of` when present.
- [x] No public function signatures changed.
