# reporium-roadmap-sync — late-PM follow-up (PR #441 + ingestion HEAD)

**Lane:** roadmap-sync (third pass on this branch — v0.8.2)
**Date:** 2026-04-24 (late PM PDT, lane window 2026-04-25)
**Branch:** `claude/feature/KAN-ROADMAP-reporium-roadmap-sync`
**Base / target:** `main`
**JIRA:** unavailable in shell at time of writing; this file is the
JIRA-first fallback per the lane's process rule.
**Owned files only:** `roadmap.json`, `README.md`, `REPORIUM_ROADMAP.md`,
`CHANGELOG.md`, `tests/test_generate.py`, `.audit/2026-04-25/`.

## Why this commit exists

The earlier sync commits on this branch are:

- `24da8c5` (2026-04-24 02:10 PDT) — v0.8.0 sync to validated suite reality.
- `37e1149` (2026-04-24 18:07 PDT) — v0.8.1 same-day correction (reporium-db
  PR #11 already on main).

Two more stale claims were identified in v0.8.0 by re-validating against
live GitHub PR state and per-repo `git log origin/main` on the late-PM pass:

### Drift 1 — NullPool /health was rewritten on PR #441

v0.8.0 said:

> NullPool-safe /health pool telemetry is in PR #435 — open, pending merge
> as of 2026-04-24.

That was empirically not the right summary by 2026-04-24 18:02 PDT.
PR #435's CI went red because the pool stats it added (`.size()`,
`.checkedout()`, `.overflow()`) are not callable on SQLAlchemy `NullPool`,
which is the engine pool class CI uses. A self-contained replacement was
opened as **PR #441** at 2026-04-25T01:02:53Z (head OID `3b52231`, base
`main`) titled `fix(health): NullPool-safe pool telemetry on /health (#354
follow-up)`. PR #441 includes the original telemetry plus a defensive
`_pool_stats` helper that probes each counter with `getattr` + try/except.

Verification (this lane, 2026-04-24 PM):

```
gh pr view 441 --json statusCheckRollup
  → ask-quality-gate: SUCCESS
  → test (Dev Tests):  SUCCESS
  → test (Tests):      SUCCESS
  → migration-smoke:   SUCCESS
  → notify-on-failure: SKIPPED   (only fires on failure)
```

PR #435 remains open (not closed); v0.8.2 records it as superseded by #441.

### Drift 2 — reporium-ingestion main HEAD was wrong

v0.8.0 said:

> Tag v1.3.0; head 025a60b.

`git log origin/main --oneline -3` on `reporium-ingestion` (this lane,
2026-04-24 PM) returns:

```
4c5f2f3 ci(graph-build): surface Cloud Run Job diagnostics on failure (#66)
4a58b6c chore(nightly): remove legacy GitHub Actions enrichment cron (#65)
e47281e fix(cli): parse comma-separated --repos for fix subcommand
```

Main HEAD is `4c5f2f3`, not `025a60b`. `025a60b` is the unmerged follow-up
branch `ci/graph-build-failure-ergonomics` per the release-certification
memo (`.audit/2026-04-24/release-certification-memo.md` §2.3).

Notably: `README.md` already had the correct `4c5f2f3` value — the drift
was only in `roadmap.json` evidence. v0.8.2 brings the JSON into agreement
with the README.

## What changed in this commit (owned files only)

1. `roadmap.json`
   - `current_state.working[reporium-api].evidence` rewritten: NullPool
     /health now points at PR #441 (`3b52231`) with PR #435 marked
     superseded but still open. Lists the 4 green CI checks by name.
   - `current_state.working[reporium-ingestion].evidence` corrected:
     `head 025a60b` → `Main HEAD '4c5f2f3'; tag v1.3.0 at 'cd9fb16'`.
     Calls out `025a60b` explicitly as an unmerged follow-up branch.
   - `fixing_now[0]` (Ask UX lane) updated: NullPool reference to #441,
     "supersedes #435"; expanded list to include PR #440 (data-quality
     X-Admin-Key) and PR #434 (`hn_mentions_count`).
   - `fixing_now[1]` (Roadmap sync) rewritten to describe the v0.8.2
     pass instead of the v0.8.0 pass.
   - New `v0.8.2-roadmap-sync-pr441` changelog entry prepended.

2. `README.md`
   - Working entry for reporium-api updated to match the JSON.
   - "Fixing Now" Ask UX lane bullet updated likewise.
   - New v0.8.2 changelog block added above v0.8.1.

3. `REPORIUM_ROADMAP.md`
   - "Open / In-Flight" lane 1 row: PR #435 → PR #441 (with caveat that
     #435 is still open and superseded).
   - "Recurring Patterns & Gotchas" NullPool block rewritten to describe
     the #441 replacement explicitly.

4. `CHANGELOG.md`
   - New v0.8.2 entry at top, followed by the verbatim v0.8.1 / v0.8.0
     entries (history honest, not silently rewritten).

5. `.audit/2026-04-25/reporium-roadmap-sync-jira.md` (this file).

No application repos touched. No PRs merged. No deploys. The two existing
commits on this branch (`24da8c5`, `37e1149`) are not being amended;
v0.8.2 is a third commit on top.

## Per-repo HEAD verification (this pass, 2026-04-24 late PM)

| Repo | Main HEAD | Source |
|---|---|---|
| reporium-api | `58ab8cd` | `git log origin/main --oneline -1` |
| reporium-ingestion | `4c5f2f3` | `git log origin/main --oneline -1` |
| reporium-mcp | `d5b6d11` | `git log origin/main --oneline -1` |
| reporium-events | `81a51fd` | `git log origin/main --oneline -1` |
| reporium-db | `5816999` | `git log origin/main --oneline -1` |
| forksync | `8055652` | `git log origin/main --oneline -1` |
| reporium | `8224e3a` | `git log origin/main --oneline -1` (nightly library refresh on top of `a2b03c1`) |
| reporium-audit | `9d5e023` | `git log origin/main --oneline -1` (nightly report on top of `d1a81d3`) |
| reporium-roadmap | `2d79e6e` (origin/main) | branch is 2 commits ahead with the v0.8.0 + v0.8.1 work; v0.8.2 makes it 3 |

## Open PR snapshot (this pass)

Source: `gh pr list --state open` on `reporium-api` (the only repo with
multiple open PRs in flight today).

| PR | State | Title |
|---|---|---|
| #441 | open, all 4 CI green | `fix(health): NullPool-safe pool telemetry on /health (#354 follow-up)` |
| #440 | open | `fix(data-quality): pass X-Admin-Key to /metrics/data-quality` |
| #439 | open | `test(ask): add forbidden_repos primitive to golden-set gate (#367)` |
| #438 | open | `fix(library): make stats.total_forks / languages corpus-wide (#344)` |
| #436 | open | `fix(deploy): strip stale traffic tags after promotion` |
| #435 | open, superseded by #441 | `fix(health): expose pool stats on /health for saturation alerting (#354)` |
| #434 | open | `fix(evaluation): surface hn_mentions_count (#369)` |

`reporium` PR #272 (FAQ page) — open. `reporium-ingestion` no open PRs;
`ci/graph-build-failure-ergonomics` (`025a60b`) is unmerged, no PR yet.

## Stop conditions honored

- No claims invented; each correction is grounded in `gh pr view` or
  `git log origin/main` output captured during this pass.
- No edits outside owned files.
- No merge, no deploy, no force-push.
- Existing commits not amended; this is a new commit on top of `37e1149`.
- History kept honest: prior v0.8.0 / v0.8.1 changelog entries retained
  verbatim alongside the new v0.8.2 entry.

## Unresolved unknowns carried forward

- Knowledge-graph edge total still not re-measured this cycle (carried
  from v0.8.0; flagged in `not_working`).
- reporium-db published `index.json` count of 1,848 still sourced from the
  2026-04-22 local clone snapshot.
- README contains hand-written sections (Solved Lanes, Historical
  Targets, the explicit per-repo HEADs in Working evidence) that
  `generate.py:build_readme` does not produce. The next nightly will
  overwrite these unless `generate.py` is taught about them — this is the
  same parity follow-up flagged in v0.8.1, still owed as a separate lane
  (suggested name: `KAN-ROADMAP-generate-py-parity`).
- Three release-certification / convergence draft files from sibling
  lanes (`release-certification-memo.md`, `release-certification-jira.md`,
  `roadmap-backlog-convergence-jira.md`) sit untracked under
  `.audit/2026-04-24/`. They are out of scope for this lane and are
  intentionally not committed here.

## Acceptance criteria

- [ ] `python -m pytest tests/test_generate.py` green (pre-existing 35
      tests + the v0.8.0 contract tests).
- [ ] `roadmap.json` and `README.md` reporium-api evidence both name
      PR #441 with the four green CI checks.
- [ ] `roadmap.json` reporium-ingestion evidence pins main HEAD
      `4c5f2f3`.
- [ ] `REPORIUM_ROADMAP.md` Open/In-Flight table row 1 names PR #441,
      not PR #435 alone.
- [ ] `CHANGELOG.md` has v0.8.2 entry at top, v0.8.1 and v0.8.0 entries
      retained verbatim.
- [ ] `.audit/2026-04-25/reporium-roadmap-sync-jira.md` exists (this
      file).
