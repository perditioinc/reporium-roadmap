# Reporium Roadmap & Architecture

> Planning and architecture companion document for the Reporium suite.
> This document preserves roadmap context and historical milestones.
> It is not the canonical live metrics source.

Last manually updated: 2026-04-09

---

## How To Read This Document

- Use this file for roadmap and architecture context.
- Use current outputs from `reporium-db`, `reporium-api`, and `reporium-metrics` for live counts and health.
- Treat 826-repo and 1,406-repo references as dated milestones unless a line explicitly says it is current runtime state.

---

## Historical Platform Snapshots

| Snapshot | Meaning |
|---|---|
| 826 repos | March 2026 foundation milestone |
| 1,406 repos | March 2026 expansion/planning snapshot |

These are historical markers, not guaranteed current live totals.

---

## Service Map

| Service | Tech | Deployment Notes |
|---|---|---|
| reporium | Next.js | Public frontend |
| reporium-api | FastAPI | Cloud Run deployment exists; use live audit/status output for current counts |
| reporium-ingestion | Python | Pipeline and backfill tooling exist; live operating status should be verified from current runs |
| reporium-db | Python | Nightly sync; canonical source for current tracked repo totals |
| reporium-events | Python | Schemas and publisher library exist; consumer rollout remains partial |
| forksync | Python | Active sync service |
| reporium-audit | Python | Nightly audit automation |
| reporium-security | Python | Main-only repo today |
| reporium-scoring | Python | Current scoring repo name; formerly `repo-intelligence` |
| reporium-metrics | Python | Metrics snapshots and generated summaries |
| reporium-dataset | Python | Dataset publication and fallback logic |
| reporium-roadmap | Markdown/Python | This repo; roadmap generator and docs |
| perditio-devkit | Python | Shared internal tooling |
| reporium-system-design | Docs | Architecture-only repo |

---

## Branch Strategy

The suite does not use a single branch pattern everywhere.

### Current Rule

- If a repo has a maintained `dev` branch, use `dev` as the integration target.
- If a repo does not have `dev`, branch from `main` and PR back to `main`.
- Avoid stale `master` references.

### Common `dev`-First Repos

- reporium
- reporium-api
- reporium-db
- reporium-ingestion
- reporium-audit
- reporium-metrics
- reporium-roadmap
- reporium-events

### Current `main`-Only Repos

- reporium-security
- reporium-scoring
- reporium-system-design
- reporium-dataset

This is the actual mixed branch strategy today.

---

## Naming Guidance

- Use `reporium-scoring` as the current repo name.
- Use `repo-intelligence` only when explicitly describing a former identity or historical milestone.

---

## Active Workstreams

- taxonomy expansion and category quality
- ingestion and backfill follow-through
- benchmark and performance visibility
- documentation consistency across roadmap, metrics, audit, and generated status outputs
- **knowledge graph data trust** — repo_dependencies rewiring, repo_edges schema, temporal history, audit regression checks

---

## Planned Features — Knowledge Graph Track

### In Progress (PR 3 / Knowledge Graph Data Trust)

| Item | Description | Status | PRs |
|---|---|---|---|
| Tag canonicalization layer | Fuzzy-match AI-generated `integration_tags` to canonical vocabulary (~200 tags) before building COMPATIBLE_WITH edges | in-progress | reporium-ingestion #42, reporium-api #324 |
| Multi-signal activity score | Replace single-formula score with log2-based components: commits velocity (max 60), star log-scale (max 15), forks log-scale (max 15), recency bonus (10). Store breakdown in `activity_score_breakdown` JSONB | in-progress | reporium-ingestion #42 |
| Velocity views | `v_edge_count_by_run` and `v_repo_activity_trend` for operational monitoring and regression detection | in-progress | reporium-api #324 (migration 035) |
| Knowledge graph nightly cron | Standalone cron at 08:30 UTC (90 min after enrichment) with crash resume via `RESUME_CRASHED_RUN` | in-progress | reporium-ingestion #42 |

### Near-term (PR 1 / KAN-101–103)

| Item | Description | Repo |
|---|---|---|
| DEPENDS_ON fix | Rewire dependency writer from dropped `repos.dependencies` column to `repo_dependencies` table | reporium-ingestion, reporium-api |
| `repo_edges` schema | Proper migration (033) with `confidence`, `metadata`, `ingest_run_id`, UNIQUE constraint | reporium-api |
| `repo_edges_history` | Append-only archive written before each rebuild; enables temporal edge diffs | reporium-api |
| Extend `ingest_runs` | Add `checkpoint_data`, `prev_edge_counts`, `git_sha`, `triggered_by` | reporium-api |
| Nightly graph build | GitHub Actions workflow chained after nightly enrichment | reporium-ingestion |
| Edge-count audit | Automated regression check: alert if DEPENDS_ON = 0 or any type drops > 20% | reporium-audit |

### Medium-term

| Item | Description |
|---|---|
| Semantic proximity map | UMAP endpoint projecting 384-dim embeddings to 2D; canvas visualisation in the frontend with zoom + cluster labels |
| Temporal layer | Time-slider UI replaying `repo_edges_history` to show how the graph evolved; backend query: `WHERE valid_from <= $ts AND valid_until > $ts` |
| Append-only embeddings | Version `repo_embeddings` rows instead of overwriting; enables embedding drift detection over time |

### Long-term (Graph Data Trust Track)

| Item | Description |
|---|---|
| Atomic graph rebuild | Staging table swap: build edges into `repo_edges_staging`, then rename atomically — zero-downtime rebuilds |
| Edge confidence calibration | Tune confidence thresholds from clickstream feedback (which edges users follow) |
| Cross-repo dependency graph | Extend DEPENDS_ON to package registries (PyPI, npm) for repos not tracked in Reporium |
| MCP temporal surface | Expose `repo_edges_history` through MCP `get_knowledge_graph` so AI agents can reason about graph evolution |

---

## Historical Milestones

### March 2026 Foundation

- foundation milestone reached on an 826-repo corpus
- early ingestion, enrichment, embeddings, and knowledge graph work completed here

### March 2026 Expansion Snapshot

- planning and roadmap docs later referenced a 1,406-repo snapshot
- use that only as a dated planning marker

### Historical Rename

- `repo-intelligence` was renamed to `reporium-scoring`

---

## Architecture Notes

- direct API, dataset, and metrics outputs should remain the live truth sources
- roadmap docs should summarize and contextualize, not replace generated operational data
- event-driven automation should only be documented as live when both producer and consumer paths are implemented
