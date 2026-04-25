## v0.8.3-roadmap-sync-pr273 - 2026-04-25

AM revalidation pass on top of v0.8.2. One stale claim fixed.

**FAQ lane — PR #272 superseded by PR #273.** v0.8.2 said "FAQ product
decision (PR #272)" in three places (reporium evidence, fixing_now lane
list, Next Up). Overnight (2026-04-24 → 2026-04-25), the FAQ work was
re-scoped onto **PR #273** (`feat(faq): /faq + client spend-surface
mitigation (KAN-272, supersedes #272)`) which carries a client-side
spend-surface mitigation that PR #272 lacked. Both PRs are still **open**
as of 2026-04-25 AM (verified via `gh pr view 272/273`); the dispatch
sheet now lists PR #272 for **close-out before #273 merges**.

Changes in this commit (owned files only):
- `roadmap.json` — `current_state.working[reporium].evidence`: rewrites
  "FAQ page (PR #272 in flight)" to point at PR #273 with #272 marked
  superseded; `fixing_now[Ask UX].description` updated; `next_up.items`
  FAQ line updated; `as_of` advanced 2026-04-24 → 2026-04-25; new v0.8.3
  changelog entry prepended.
- `README.md` — corresponding rewrites of working entry, fixing_now line,
  Next Up bullet, and Historical Targets outcome date; new v0.8.3
  changelog section; footer "Last updated" advanced.
- `REPORIUM_ROADMAP.md` — service-map row 1 (reporium) and Open/In-Flight
  table row 4 updated to reference PR #273 with #272 marked superseded;
  `Last manually updated` and `Current State (as of …)` advanced;
  NullPool gotcha "Both PRs remain open as of …" date advanced.
- `CHANGELOG.md` — this entry.

JIRA fallback: `.audit/2026-04-25/reporium-roadmap-sync-jira.md` already
present from v0.8.2; the v0.8.3 delta is documented inside that file's
revision log (no new audit file needed; same lane, same owned scope).

No code change to `generate.py`; no application repos modified.
Branch-strategy unchanged (target `main`, branch
`claude/feature/KAN-ROADMAP-reporium-roadmap-sync`).

## v0.8.2-roadmap-sync-pr441 - 2026-04-24

Late-PM follow-up to v0.8.1. Two stale claims corrected against owned files only.

1. **NullPool-safe `/health`.** v0.8.0 said `PR #435 — open, pending merge`.
   PR #435's CI in fact went red because `NullPool` lacks `.size()`/
   `.checkedout()`/`.overflow()`. A self-contained green replacement was opened
   as **PR #441** (`fix(health): NullPool-safe pool telemetry on /health
   (#354 follow-up)`, head `3b52231`, all 4 required CI checks green: Tests,
   Dev Tests, ask-quality-gate, migration-smoke). PR #441 includes the
   original telemetry plus a defensive `_pool_stats` helper that probes each
   counter with `getattr` + try/except.
   - `roadmap.json` `current_state.working[reporium-api].evidence` rewritten
     to point at PR #441 with PR #435 marked superseded but still open.
   - `roadmap.json` `fixing_now` Ask UX lane list updated to reference #441
     and expanded to include PRs #434 and #440.
   - `README.md` working entry, fixing_now, and `REPORIUM_ROADMAP.md`
     gotchas section + Open/In-Flight table updated to match.
2. **reporium-ingestion main HEAD.** v0.8.0 evidence said `head 025a60b`.
   Verified main HEAD is `4c5f2f3` (#66, ci/graph-build diagnostics merge);
   `025a60b` is the unmerged follow-up branch
   `ci/graph-build-failure-ergonomics` and is *not* on main.
   - `roadmap.json` `current_state.working[reporium-ingestion].evidence`
     corrected: pins main HEAD `4c5f2f3` and tag v1.3.0 at `cd9fb16`;
     calls out `025a60b` explicitly as an unmerged follow-up branch.
   - `README.md` already had `4c5f2f3` (no change needed).

No code change to `generate.py`; owned files only (`roadmap.json`,
`README.md`, `REPORIUM_ROADMAP.md`, `CHANGELOG.md`, `tests/`,
`.audit/2026-04-25/`). Branch-strategy unchanged (target `main`, branch
`claude/feature/KAN-ROADMAP-reporium-roadmap-sync`). No application repos
modified.

## v0.8.1-roadmap-sync-correction - 2026-04-24

Same-day PM correction to v0.8.0-roadmap-sync (02:10 PDT).

The 02:10 sync said reporium-db's GraphQL 5xx companion fix (`f3a099e`) was on a
feature branch only and tracked under `next_up`. That was wrong by ~22 hours: PR
#11 (`fix(fetcher): GraphQL 5xx resilience — 6 retries, jitter, correct
checkpoint`) merged to main as commit `9c0dad3` at **2026-04-23T04:56Z**. The
local feature branch `claude/fix/graphql-502-resilience` (commit `f3a099e`) is
the source; `9c0dad3` is what landed on main.

Changes in this commit:
- `roadmap.json` working entry for reporium-db rewritten — now points at PR #11
  / `9c0dad3` and pins main HEAD `5816999` (build, 2026-04-24).
- `roadmap.json` `solved_lanes` entry renamed `DB sync GraphQL 403 retry-after
  cap` → **`DB sync GitHub 403 + GraphQL 5xx resilience`**; lists both PR #10
  (`53b7c44`) and PR #11 (`9c0dad3`) as resolved on main.
- `README.md` working entry, solved-lanes summary line, and Next Up updated
  to match. The `Land reporium-db f3a099e GraphQL 5xx resilience patch from
  feature branch onto main` item has been **removed from Next Up** because it is
  already on main.
- New v0.8.1 changelog entry added to both `roadmap.json` and `README.md`.

Owned files only. No application repos modified. Branch-strategy unchanged
(target `main`, branch `claude/feature/KAN-ROADMAP-reporium-roadmap-sync`).

## v0.8.0-roadmap-sync - 2026-04-24

Sync of `roadmap.json`, `README.md`, and `REPORIUM_ROADMAP.md` to validated
2026-04-24 suite reality. No code change to `generate.py`; source-of-truth
content only, plus eight new contract tests (`tests/test_generate.py`) that
pin the new state so it cannot silently regress.

Highlights:
- Corpus updated from claimed 1,406 → measured **1,856** repos (live `/library/full`).
- DB backend updated **Neon → Cloud SQL** (migrated 2026-04-15).
- Alembic head updated **004 → 039** (`039_query_log_query_id`).
- `reporium-mcp` added to working list (live on Cloud Run via HTTP bridge,
  18 tools, WIF deploy, used by 3 Workato recipes). Main HEAD `d5b6d11`.
- `reporium-events` moved from "local only" to **public on GitHub**. Main HEAD `81a51fd`.
- `reporium-api` openapi/tag version drift (openapi reports 1.1.0, tag v1.6.0)
  flagged in `not_working` for follow-up. Main HEAD `58ab8cd`.
- `reporium-ingestion` main HEAD pinned at `4c5f2f3`; tag v1.3.0 at `cd9fb16`.
  (Earlier roadmap drafts cited `025a60b`, which is not on main of the local clone.)
- NullPool-safe `/health` (PR #435, lane commit `3b52231`) softened from
  "shipped today" to **"open, pending merge"** — verified against reporium-api
  main HEAD.
- `reporium-db` evidence corrected: 403-retry-with-cap (PR #10, `53b7c44`) is
  on main; the GraphQL 5xx companion (`f3a099e`) is on a feature branch only
  and has not yet landed on main as of 2026-04-24.
- Knowledge-graph edge total marked **needs verification** (was 6,209 on the
  old 1,406-repo corpus; not re-measured this cycle).
- New `solved_lanes` array enumerates 8 already-shipped lanes (3 P2s closed
  today + Neon→Cloud SQL + reporium-events publication + reporium-mcp WIF +
  forksync Upstash + SEC-HOTFIX #264) so future runs do not re-open them.
- `reporium-api` evidence no longer carries unresolved `{db_total}` template
  placeholder (it would have resolved to reporium-db's 1,848 on next render
  instead of the API's 1,856).
- Original 10K-by-end-of-March / 100K-by-end-of-April targets preserved in a
  new `historical_targets` block — kept honest, not silently rewritten.

## v0.3.0 - 2026-03-17

- forksync v2 launched: 68s for 805 repos (was 13 min - 91% faster)
- 6 new repos built: reporium-db, reporium-dataset, portfolio, reporium-roadmap, reporium-metrics, repo-intelligence
- Cloud Run + Redis + VPC connector deployed for forksync

## v0.2.0 - 2026-03-01

- reporium-ingestion pipeline live
- 702 repos AI-enriched across 12 categories
- Ollama local AI for tag generation

## v0.1.0 - 2026-01-01

- reporium frontend and API launched
- 805 repos tracked
- Full-text search and category filtering live at reporium.com
