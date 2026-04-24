# JIRA fallback: reporium-roadmap sync to current suite reality

JIRA is unavailable from this lane; this file stands in for the ticket per process rule.
A real KAN ticket should replace `KAN-ROADMAP` once JIRA access is restored.

## Title
Sync `reporium-roadmap` (README, REPORIUM_ROADMAP, roadmap.json) with current suite reality

## Type / Priority
Chore · Medium

## Owner / Lane
Roadmap-sync lane (2026-04-24 multi-lane dispatch)

## Branch
`claude/feature/KAN-ROADMAP-reporium-roadmap-sync` → `main`

## Owned files
- `README.md`
- `REPORIUM_ROADMAP.md`
- `roadmap.json`
- `CHANGELOG.md` (changelog note only)
- `tests/test_generate.py`, `tests/conftest.py`
- `.audit/2026-04-24/reporium-roadmap-sync-jira.md` (this file)

## Problem
The roadmap repo is the public single-source-of-truth for the suite's status.
`roadmap.json` was last marked `as_of: 2026-03-23`. `REPORIUM_ROADMAP.md` was
last manually updated `2026-03-24`. README badges/timestamps say `2026-04-09`.
None of those reflect the suite as it actually stands on 2026-04-24.

Concrete drift identified by audit (see "Findings" below):
- Repo count claim is ~450 stale.
- Database backend ("Neon") was migrated to Cloud SQL on 2026-04-15.
- Migration count claim is 35 versions stale (claimed `004`, current head is `039`).
- `reporium-events` is no longer "local only / not on GitHub".
- `reporium-mcp` is missing entirely from the service map and current state.
- Phase 2 / Phase 3 deadlines (end of March, April) have lapsed without status update.
- Targets ("10K by end of March 2026", "100K by end of April 2026") are unmet
  and need an honest restatement; silently rewriting them would erase history.

## Acceptance criteria
1. `roadmap.json` reflects the current suite (services, versions, last-known
   metrics, work in flight, targets) with `as_of: 2026-04-24`.
2. Stale targets are kept in the changelog as historical entries; new targets
   are stated honestly.
3. `REPORIUM_ROADMAP.md` service map adds `reporium-mcp`, marks `reporium-events`
   as on GitHub, and updates DB backend to Cloud SQL.
4. `README.md` regenerates cleanly from the new `roadmap.json` via `generate.py`
   (template substitution still works, no missing keys).
5. Tests still pass; new test pins the new structure (e.g. asserts that
   `reporium-mcp` appears in `current_state.working` and that the platform
   metrics include `cloud_sql`).
6. `CHANGELOG.md` has a new top entry describing the sync.
7. Any claim that cannot be verified from the live suite is marked
   `needs verification` rather than restated as fact.

## Findings (audit, 2026-04-24)

### Verified live (curl against prod)
| Claim source | Old value | New value (live) | Source |
|---|---|---|---|
| reporium.com | live, 1406 repos | live (HTTP 200) | `curl -sL https://reporium.com` |
| reporium-api `/health` | ok | `{"status":"ok","db":"ok"}` | `curl /health` |
| reporium-api `/library/full` totalRepos | 1,406 | **1,856** | `curl /library/full?page=1&page_size=1` |
| reporium-api `/graph/edges` total_repos | n/a | **1,895** total / **1,768** with embeddings | `curl /graph/edges?limit=1` |
| reporium-api openapi version | 1.6.0 (claimed) | reports `1.1.0` in openapi but git tag is `v1.6.0` (drift between `app/main.py` and tag) | `curl /openapi.json` + `git tag` |
| Knowledge graph edges | 6,209 (claimed) | **needs verification** — only `ALTERNATIVE_TO` returned in sampled `/graph/edges` (limit=1); openapi has 98 paths | live |

### Verified from local clones (main HEAD on 2026-04-24)
| Repo | Roadmap claim | Reality (main) |
|---|---|---|
| reporium | last commit 2026-04-09 | `8224e3a` (latest library data refresh 2026-04-24); product changes through `a2b03c1` (FAQ page, jellyfish hover, citation linking, security hotfix #264). |
| reporium-api | last commit 2026-04-08, tag v1.6.0 | main HEAD `58ab8cd` (#433, smart-route fix). NullPool-safe `/health` (PR #435, commit `3b52231`) is on the lane branch but **not yet on main**. Tag still v1.6.0; openapi reports `1.1.0` — drift. |
| reporium-ingestion | last commit 2026-04-08, tag v1.3.0 | main HEAD `4c5f2f3` (#66 graph-build CI diagnostics). Earlier roadmap drafts cited `025a60b`; that hash is **not on main** of the local clone. Tag v1.3.0 is at `cd9fb16`. |
| reporium-db | last commit 2026-04-06 | main HEAD `31b06bd` (build(12) nightly 2026-04-22). Latest substantive fix on main is PR #10 `53b7c44` (403 retry-after cap). The 5xx companion `f3a099e` is on `claude/fix/graphql-502-resilience` only — **not yet on main**. Tag v1.0.0. |
| reporium-audit | last commit 2026-04-08 | `4ddc6dd` (knowledge graph edge count regression check). |
| reporium-events | "local only, not on GitHub" | Published; main HEAD `81a51fd` (PR #2 Firestore async txn fix). |
| reporium-mcp | **absent from roadmap** | Live on Cloud Run via `cloudbuild.http.yaml`; HTTP bridge for Workato (KAN-120, KAN-163); 18 tools across 7 modules. Main HEAD `d5b6d11`. |
| forksync | last commit 2026-04-01 | Main HEAD `8055652` (Upstash Redis migration from Memorystore, PR #1). |

### Verified from auto-memory (project context, requires sanity-check before reuse)
- 2026-04-15: Neon → Cloud SQL migration complete (f1-micro, max_connections=25, pool_size=5+2). Source: `project_neon_quota_migration.md`.
- 2026-04-15: Sentry, 6 alert policies, 3 Workato recipes shipped (KAN-120 demo prep). Source: `project_kan120_session_apr15.md`.
- 2026-04-21–22: Ask sprint 1 closed; PRs #407/#409/#410/#411/#412/#413 merged; Cloud Run Job for nightly enrichment proven end-to-end. Source: `project_ask_sprint1_apr21.md`, `project_ask_sprint1_apr22.md`.
- 2026-04-24 (today): conftest teardown (api PR #429, main `8c9a872`) and legacy nightly cron (ingestion PR #65, main `4a58b6c`) shipped to main. Memory `project_reporium_p2_resolved_apr24.md` records DB sync 5xx resilience as shipped at `f3a099e` — **this lane was unable to confirm `f3a099e` on main**; it is on a feature branch. Memory note may be stale on this point.

### Cannot verify from this lane
- Exact knowledge-graph edge count (only sampled, not totalled)
- Current commit-stats backfill coverage (was 1,011 missing — needs DB query)
- "100K by end of April 2026" is mathematically infeasible (1,856 today)
- Whether the legacy "Phase 4 / cloud credits" items are still on the roadmap
  intentionally — flagged as **needs product decision**

## Out of scope
- No edits to other repos (process rule 6/7).
- No merge/deploy.
- No invented JIRA IDs in code; placeholder `KAN-ROADMAP` used until ticket exists.
