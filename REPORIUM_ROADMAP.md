# Reporium Roadmap & Architecture

> Planning and architecture companion document for the Reporium suite.
> This document preserves roadmap context and historical milestones.
> It is not the canonical live metrics source.

Last manually updated: 2026-03-24

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
