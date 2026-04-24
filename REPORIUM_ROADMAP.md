# Reporium Roadmap & Architecture

> **Single source of truth** for the Reporium platform suite.
> Designed to be auto-updated via the `reporium-events` system.
> Last manually updated: **2026-04-24**

---

## Current State (as of 2026-04-24)

### Platform Metrics

| Metric | Value | Source |
|---|---|---|
| Total repos (live API `/library/full`) | **1,856** | curl prod 2026-04-24 |
| Total repos (live API `/graph/edges`) | **1,895** | curl prod 2026-04-24 |
| Repos with embeddings | 1,768 (all-MiniLM-L6-v2, 384-dim) | curl prod 2026-04-24 |
| Knowledge graph edge total | **needs verification** (older claim 6,209 was on 1,406-repo corpus) | — |
| reporium-db published index.json | 1,848 repos | local clone 2026-04-22 |
| Alembic head | `039_query_log_query_id` | `reporium-api/migrations/versions/` |
| DB backend | **Cloud SQL** PostgreSQL + pgvector (migrated from Neon 2026-04-15) | project memory `project_neon_quota_migration.md` |
| DB tier | f1-micro (`max_connections=25`, app `pool_size=5` + `max_overflow=2`) | same |
| Monitoring | Sentry + 6 GCP alert policies | `project_kan120_session_apr15.md` |
| External integrations | Workato (3 recipes), MCP (Claude Code + HTTP bridge) | `WORKATO_RECIPE_*_COMPLETE.md`, `reporium-mcp/` |

### Service Map

| Service | Tech | Deployed | URL | Status |
|---|---|---|---|---|
| reporium | Next.js | Vercel | reporium.com | live, v0.7.0, FAQ in flight (PR #272) |
| reporium-api | FastAPI | GCP Cloud Run | reporium-api-573778300586.us-central1.run.app | live, tag v1.6.0 (openapi reports 1.1.0 — **drift, follow-up**) |
| reporium-mcp | Python | GCP Cloud Run (HTTP bridge) + stdio MCP | — | live, 18 tools, Workload Identity Federation |
| reporium-ingestion | Python | GCP Cloud Run **Job** (nightly) | — | live, v1.3.0; legacy Actions cron removed |
| reporium-db | Python | GitHub Actions (nightly) | — | live, v1.0.0 |
| reporium-events | Python | GCP Pub/Sub + Firestore | — | **public on GitHub** as of 2026-04, v1.0.0 |
| forksync | Python | GCP Cloud Run + Upstash Redis | — | live |
| reporium-audit | Python | GitHub Actions (nightly 8am UTC) | — | live, v1.0.0 |
| reporium-security | Python | pip-installable | — | unchanged from prior roadmap; needs verification |
| reporium-scoring | Python | pip-installable | — | unchanged from prior roadmap; needs verification |
| reporium-metrics | Python | GitHub Actions (nightly) | — | live (per 2026-04-09 audit pass) |
| reporium-dataset | Python | GitHub Actions (auto-updated) | — | live |
| reporium-roadmap | Markdown | GitHub Pages + nightly job | — | this repo |
| perditio-devkit | Python | pip-installable | — | live |
| reporium-system-design | Docs | — | — | docs only |

### Git Flow (current dispatch contract)

```
main                              → production (protected, PR required)
claude/feature/KAN-<id>-<lane>    → owned by a single dispatch lane (PR → main)
fix/*                             → bug fixes  (PR → main)
hotfix/*                          → emergency fixes  (PR → main, tagged SEC-HOTFIX where applicable)
```

The earlier `dev` integration branch is no longer the default PR target for new
lanes; lanes PR straight to `main` per the 2026-04-23 JIRA-first workflow contract.
Older PRs that targeted `dev` are still in flight.

### Open / In-Flight (sample, not exhaustive)

| Lane | Repo | PR/branch | Status |
|---|---|---|---|
| 1 | reporium-api | PR #435 (NullPool /health) | open on lane branch (`3b52231`); not yet on main |
| 2 | reporium-api | PR #436 (stale Cloud Run candidate-tag cleanup) | review |
| 3 | reporium-ingestion | Nightly Graph Build investigation | diagnostics added (PR #66, main HEAD `4c5f2f3`) |
| 4 | reporium | PR #272 (FAQ page) | product/cost decision |
| 5 | reporium-api | PR #434 (hn_mentions_count) | review |
| 6 | reporium-api | PR #438 (library stats fix) | review, merge-order coordinated |
| 7 | reporium-api | PR #439 (forbidden_repos primitive) | review |
| 8 | reporium-api | Data Quality Check workflow verification | plumbing fixed; data regression tracked |

---

## Phase 1: Foundation (COMPLETED — March 23, 2026)

- [x] Build enrichment pipeline (Phases 0–6)
- [x] Expand corpus from 826 → 1,406 repos
- [x] Research and fork 500+ AI repos across 40+ categories
- [x] Fix dashboard regressions (`is_private`, category names, cache invalidation)
- [x] Fix coverage badges, builder display, language count
- [x] Establish Git Flow and SDLC practices
- [x] Set up task management and persistent memory
- [x] Research AI taxonomy (28 skill areas, 58 categories, ~200 tags)
- [x] Explore reporium-events Pub/Sub system
- [x] PM Skills + Industries backfill (390 repos)
- [x] SQL-migrate all 1,127 old-taxonomy-name rows to canonical names
- [x] Fix in-memory cache invalidation on ingestion
- [x] Add `is_private` column to DB + ingestion pipeline

---

## Phase 2: Data Quality (CLOSED — March 24 → April 16, 2026)

Scope from the original roadmap, with current status:

### Taxonomy Expansion (Issue #17)
- [x] Implement 28 skill areas in enrichment prompt
- [x] Re-enrich repos with new taxonomy
- [x] Update frontend coverage badges
- [x] Curate tags
- [x] Add unit tests for new taxonomy

### Data Backfills
- [x] PM Skills + Industries backfill (390 repos)
- [x] Fork timeline backfill (1,390 repos — script ran)
- [ ] Commit data backfill (1,011 repos) — **needs verification**: claim was that nightly CI would populate it; status not re-measured this cycle.

### API & Deployment
- [x] CORS restricted to `reporium.com`
- [x] CI/CD: push to `main` → auto-deploy Cloud Run
- [x] Deploy builder category + status tag filter fixes
- [x] Migrate from Neon → Cloud SQL (2026-04-15)
- [x] Sentry + 6 GCP alert policies (KAN-120, 2026-04-15)

### Events System
- [x] Push `reporium-events` to GitHub (`perditioinc/reporium-events`)
- [ ] Wire `ingestion.completed` event into enrichment pipeline — **partial**, needs verification
- [ ] Wire `repo.added` event into fork + ingest workflow — **partial**, needs verification
- [ ] Wire `api.deployed` event into deploy workflow — needs verification
- [ ] Create real subscriber in reporium-api (replace stub at `platform.py:82`) — needs verification
- [x] Create GCP Pub/Sub topic + Firestore collection
- [ ] Auto-update this roadmap via events — still on roadmap; nightly job now regenerates README from `roadmap.json` instead

---

## Phase 3: Intelligence Layer (IN PROGRESS — April 2026)

### Knowledge Graph Visualization
- [x] 3D knowledge graph in API + frontend (KAN-119 snapshot feature; edge type colors per relationship type)
- [ ] Re-measure knowledge graph edge totals after 2026-04 enrichment work
- [ ] Mobile-responsive with touch gestures — needs verification

### Query Enhancement (KAN-162 / KAN-366 / Ask sprint)
- [x] `/intelligence/ask` smart routing + follow-up suggestion chips (PR #422, #423, #431)
- [x] Off-topic regex check deferred until after retrieval (KAN-366, PR #425)
- [x] Conftest teardown made non-fatal — kills flaky main CI (PR #429)
- [ ] Re-run smoke tests with expanded taxonomy + Phase 2 backfills
- [ ] Track query metrics — partially live via `/metrics/data-quality`; admin-key-gated

### Repo Expansion
- Original "2,000 by end of April" target — current 1,856; not yet met but close.

---

## Phase 4: Platform & Scale (May 2026)

### Infrastructure
- [x] Sentry / error monitoring
- [x] Document deployment runbooks (`.audit/2026-04-22/cutover-runbook.md`)
- [ ] Set up staging environment for `dev` branch — superseded by direct-to-main lane workflow
- [ ] Lighthouse performance baselines — needs verification
- [ ] Mac Mini setup for local LLM enrichment — deferred (still under 10K repos)

### GitHub Pages Dashboard
- [x] Public roadmap visualization (this repo)
- [ ] Knowledge graph interactive explorer — frontend has 3D view; standalone explorer still planned

### Cloud Credits
- Items still on backlog; status unchanged.

---

## Honest restatement of corpus targets

The original v0.7.0 roadmap said: **"10K repos by end of March 2026; 100K by end of April 2026."**
As of 2026-04-24 the live API reports **1,856 repos**. Those targets were not met
and are kept here in `historical_targets` rather than silently rewritten.
Replacement targets are pending product input.

---

## Event-Driven Updates

Auto-update plan (unchanged in spirit, partially implemented):

| Event | Publisher | Updates |
|---|---|---|
| `ingestion.completed` | reporium-ingestion | Total repos, enriched count, cost |
| `db.synced` | reporium-db | Commit data freshness, sync status |
| `sync.completed` | forksync | Fork count, sync health |
| `api.deployed` | reporium-api | API version, deployment status |
| `repo.added` | any | Total repo count |
| `health.check` | reporium-audit | Service health status |

The current nightly workflow re-renders `README.md` from `roadmap.json` using
live GitHub stats; the long-term plan is for `reporium-events` to mutate
`roadmap.json` directly.

---

## Architecture Decisions (additions since 2026-03-24)

| # | Decision | Rationale |
|---|---|---|
| 1 | Neon over Supabase | Disconnection issues with Supabase; better pgvector support on Neon |
| 2 | sentence-transformers locally | Zero cost at current scale |
| 3 | pgvector not Neo4j | Sufficient at current scale, avoids new infra overhead |
| 4 | RAG in reporium-ingestion | Keep intelligence close to the data |
| 5 | Mac Mini / Ollama deferred | Not needed until 10K+ repos |
| 6 | Claude API for enrichment | Quality at 900 repos; revisit at 10K+ |
| 7 | Targeted sweeps > broad scraping | Higher signal, lower noise |
| 8 | GCP Pub/Sub for events | Native to `perditio-platform` GCP project |
| 9 | Git Flow branching → JIRA-first lane workflow | Multiple agents working in parallel; JIRA-first contract established 2026-04-23 |
| 10 | Google Stitch + Antigravity | Design-to-code workflow, free tier |
| 11 | **Cloud SQL over Neon** (2026-04-15) | Neon free-tier compute quota exhaustion; predictable billing on Cloud SQL f1-micro |
| 12 | **Cloud Run Job for nightly enrichment** | Replace GitHub Actions cron; long-running, scoped IAM, observable via Cloud Run diagnostics |
| 13 | **Workload Identity Federation for Cloud Run deploys** | Replace `GCP_SA_KEY` secret (KAN-124, reporium-mcp PR #12) |
| 14 | **MCP HTTP bridge for Workato** | Workato can't speak stdio MCP directly; HTTP bridge runs in Cloud Run alongside the stdio server |

---

## Known Security / Quality Issues (2026-04-24)

| Severity | Location | Issue |
|---|---|---|
| ⚠️ Cosmetic | reporium-api `app/main.py` | FastAPI `version="1.1.0"` while git tag is `v1.6.0` — openapi/tag drift |
| ⚠️ Low | knowledge-graph edge total | Not measured this cycle; needs re-verification after taxonomy work |
| ⚠️ Low | commit data backfill (1,011 repos) | Coverage not re-verified this cycle |
| ✅ Resolved | leaked private repos in library.json | SEC-HOTFIX #264 (2026-04) — 44 leaked entries removed |
| ✅ Resolved | Cloud SQL password in logs | Password rotation runbook prepared (`.audit/2026-04-22/password-rotation-runbook.md`) |

All secrets are properly `.gitignore`d. Security headers, rate limiting, and
private-repo filtering remain active.

---

## Recurring Patterns & Gotchas

**After every bulk fork/import:**
Always follow up with `python -m ingestion fix --repos <names>` (note: comma-separated list per `e47281e`).
Bulk imports via `/ingest/repos` only write basic GitHub metadata — no tags, categories, builders, or readme summaries.

**Cache invalidation:**
`library_full.py` has a module-level `_cache` (5-min TTL). Call `invalidate_library_cache()` after ingestion.

**Category taxonomy:**
All 1,127 old-taxonomy rows have been SQL-migrated to canonical names.

**Cloud Run deploy race (documented 2026-04-15):**
Promotions need a stale-traffic-tag cleanup step; tracked by reporium-api PR #436.

**NullPool in /health (2026-04-24):**
`/health` pool telemetry must guard against `NullPool` (which lacks `.size()` etc.).
Fix is on lane branch as `3b52231` (PR #435) — open, pending merge to main as of 2026-04-24.
