# Reporium Roadmap & Architecture

> **Single source of truth** for the Reporium platform suite.
> Designed to be auto-updated via the `reporium-events` system.
> Last manually updated: 2026-03-24

---

## Current State (as of 2026-03-24)

### Platform Metrics

| Metric | Value |
|---|---|
| Total repos tracked | 1,406 (started at 826) |
| Enriched | 1,406 / 1,406 (100%) |
| Embeddings | 1,406 (all-MiniLM-L6-v2, 384-dim) |
| Knowledge graph edges | 6,209 (ALTERNATIVE_TO, COMPATIBLE_WITH, DEPENDS_ON) |
| GitHub forks on perditioinc | ~1,444 |
| Total enrichment cost | ~$4.50 (Claude API) |
| Query endpoint cost | ~$0.01 / query |

### Service Map

| Service | Tech | Deployed | URL |
|---|---|---|---|
| reporium | Next.js | Vercel | reporium.com |
| reporium-api | FastAPI | GCP Cloud Run | reporium-api-573778300586.us-central1.run.app |
| reporium-ingestion | Python | Local / Manual | — |
| reporium-db | Python | GitHub Actions (nightly) | — |
| reporium-events | Python | Local only (NOT on GitHub) | — |
| forksync | Python | GitHub Actions | — |
| reporium-audit | Python | GitHub Actions (nightly 8am UTC) | — |
| reporium-security | Python | pip-installable | — |
| reporium-scoring | Python | pip-installable | — |
| reporium-metrics | Python | GitHub Actions (nightly) | — |
| reporium-dataset | Python | GitHub Actions (auto-updated) | — |
| reporium-roadmap | Markdown | GitHub Pages | — |
| perditio-devkit | Python | pip-installable | — |
| reporium-system-design | Docs | — | Architecture docs only |

### Git Flow

```
main        → production (protected, PR required)
dev         → integration (default branch for PRs)
feature/*   → new features  (PR → dev)
fix/*       → bug fixes      (PR → dev)
release/*   → release candidates (PR → main)
hotfix/*    → emergency fixes  (PR → main + dev)
```

### Open Issues & PRs

| # | Type | Title | Branch | Status |
|---|---|---|---|---|
| #15 | Issue | Tag cloud status tags | — | Open |
| #16 | PR | fix/tag-cloud-status-tags-15 | `fix/tag-cloud-status-tags-15` | Open → dev |
| #17 | Issue | Taxonomy expansion (28 skill areas) | — | Open |

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

## Phase 2: Data Quality (IN PROGRESS — March 24–31, 2026)

### Taxonomy Expansion (Issue #17)

- [ ] Implement 28 skill areas in enrichment prompt
- [ ] Re-enrich all 1,406 repos with new taxonomy
- [ ] Update frontend to display 28 coverage badges
- [ ] Curate tags: remove ~440 noise tags, keep ~200
- [ ] Add unit tests for new taxonomy

> Branch: `feature/taxonomy-expansion`

### Data Backfills

- [x] PM Skills + Industries backfill (390 repos)
- [ ] Commit data backfill (1,011 repos — needs `GH_TOKEN` secret on reporium-db)
- [ ] Fork timeline backfill (1,390 repos — script ready, needs prod run)

### API & Deployment

- [ ] Redeploy reporium-api v1.5.0 (security fixes; blocked on `GCP_SA_KEY` secret)
- [ ] CORS fix (`allow_origins` wildcard → restrict to `reporium.com`)
- [ ] Set up CI/CD: push to `main` → auto-deploy Cloud Run
- [ ] Deploy builder category + status tag filter fixes (PR #16)

### Events System

- [ ] Push `reporium-events` to GitHub (`perditioinc/reporium-events`)
- [ ] Wire `ingestion.completed` event into enrichment pipeline
- [ ] Wire `repo.added` event into fork + ingest workflow
- [ ] Wire `api.deployed` event into deploy workflow
- [ ] Create real subscriber in reporium-api (replace stub at `platform.py:82`)
- [ ] Create GCP Pub/Sub topic + Firestore collection via IaC
- [ ] Auto-update this roadmap via events (metrics section)

---

## Phase 3: Intelligence Layer (April 2026)

### Knowledge Graph Visualization

- [ ] Design spider-web graph component in Google Stitch
- [ ] Build D3.js / Three.js force-directed graph from graph edges
- [ ] Replace tag cloud with interactive knowledge graph
- [ ] Mobile-responsive with touch gestures
- [ ] Parallax scrolling integration

### Query Enhancement

- [ ] Re-run smoke tests with expanded taxonomy
- [ ] Improve signal scores in weak categories (MCP, RAG, doc processing)
- [ ] Add query caching for common patterns
- [ ] Track query metrics (latency, token usage, result quality)

### Repo Expansion

- [ ] Fork + ingest remaining Perditio-specific repos (WhatsApp, tourism, fintech)
- [ ] Fork + ingest PTR VR training repos
- [ ] Fork + ingest Fluency scaling / precompression repos
- [ ] Fork + ingest compression + video OCR repos
- [ ] **Target: 2,000 repos by end of April**

---

## Phase 4: Platform & Scale (May 2026)

### Infrastructure

- [ ] Set up staging environment for `dev` branch
- [ ] Add Lighthouse performance baselines
- [ ] Set up error monitoring (Sentry)
- [ ] Document deployment runbooks
- [ ] Mac Mini setup for local LLM enrichment (when approaching 10K repos)

### GitHub Pages Dashboard

- [ ] Public roadmap visualization
- [ ] DB metrics (repo count, category coverage, signal scores)
- [ ] Research portfolio (all company / industry analysis)
- [ ] Knowledge graph interactive explorer
- [ ] Auto-updated via `reporium-events`

### Cloud Credits

- [ ] Apply to Microsoft Azure for Startups ($5K instant)
- [ ] Apply to AWS Activate Founders ($1K)
- [ ] Reapply for Google for Startups AI credits ($350K)
- [ ] Apply to NVIDIA Inception ($100K GPU)
- [ ] Apply to Cloudflare for Startups ($250K)

---

## Event-Driven Updates

This document is designed to be auto-updated by `reporium-events`. When the following events fire, the metrics section should be refreshed:

| Event | Publisher | Updates |
|---|---|---|
| `ingestion.completed` | reporium-ingestion | Total repos, enriched count, cost |
| `db.synced` | reporium-db | Commit data freshness, sync status |
| `sync.completed` | forksync | Fork count, sync health |
| `api.deployed` | reporium-api | API version, deployment status |
| `repo.added` | any | Total repo count |
| `health.check` | reporium-audit | Service health status |

**Automation TODO:** Create a GitHub Action that subscribes to the `reporium-events` Pub/Sub topic (project: `perditio-platform`, topic: `reporium-events`), reads the latest metrics from Neon DB, and commits an updated `REPORIUM_ROADMAP.md` to this repo.

---

## Signal Scores (latest — 1,203-repo corpus)

| Category | Score | Status |
|---|---|---|
| Observability & Monitoring | 0.697 | Strong |
| LLM Evals & Benchmarking | 0.696 | Strong |
| Local AI Agents | 0.642 | Strong |
| Fine-tuning LLMs | 0.608 | Medium |
| AI Security / Prompt Injection | 0.587 | Medium (+0.033 improved) |
| RAG / Vector Search | 0.537 | Weak |
| Doc Processing | 0.533 | Weak |
| MCP / Tool-use | 0.386 | Weakest — priority target |

> **Note:** Re-run smoke tests after taxonomy expansion + Phase 2 backfills to get updated scores.

---

## Architecture Decisions

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
| 9 | Git Flow branching | Multiple agents working in parallel need clear merge targets |
| 10 | Google Stitch + Antigravity | Design-to-code workflow, free tier |

---

## Known Security Issues

| Severity | Location | Issue |
|---|---|---|
| ⚠️ Low | `intelligence.py:162` | f-string for UUIDs in SQL `IN` clause (internal IDs, low risk) |
| ⚠️ Medium | `library_full.py` CORS | `allow_origins=["*"]` — should restrict to `reporium.com` |
| ⚠️ Low | `platform.py` `/events/ingest` | No auth on stub endpoint, accepts arbitrary dict |

All secrets (`.env`, API keys) are properly `.gitignore`d. Security headers, rate limiting, and private-repo filtering are all active.

---

## Recurring Patterns & Gotchas

**After every bulk fork/import:**
Always follow up with `python -m ingestion fix --repos <names>` or a full `python -m ingestion run --mode full`. Bulk imports via `/ingest/repos` only write basic GitHub metadata — no tags, categories, builders, or readme summaries.

**Cache invalidation:**
`library_full.py` has a module-level `_cache` (5-min TTL) separate from Redis. Call `invalidate_library_cache()` after ingestion to flush both.

**Category taxonomy:**
All 1,127 old-taxonomy rows (Tooling, Agents, Research, etc.) have been SQL-migrated to canonical names. Do not use old names in new code.
