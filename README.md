# Reporium Roadmap

> Track every meaningful AI development tool on GitHub. 10K repos by end of March 2026. 100K by end of April 2026.

---

## Live

- [**reporium v1.0.0**](https://reporium.com) — AI tool discovery frontend: full-text search, category filtering, static JSON serving, mobile responsive  
  last commit: `2026-03-18` · 1 stars · 0 open issues
  _Full-text search · Category filtering · Static JSON serving · Mobile responsive_
- [**reporium-api v1.0.0**](https://github.com/perditioinc/reporium-api) — FastAPI + PostgreSQL + pgvector: 702 repos queryable, Redis caching  
  last commit: `2026-03-15` · 1 stars · 0 open issues
  _FastAPI · PostgreSQL + pgvector · 702 repos queryable · Redis caching_
- [**reporium-ingestion v1.0.0**](https://github.com/perditioinc/reporium-ingestion) — AI enrichment pipeline: Ollama local AI, four-tier cache, nightly batch, 12 categories  
  last commit: `2026-03-16` · 1 stars · 0 open issues
  _Ollama local AI · Four-tier cache · Nightly batch · 12 categories_
- [**forksync v2.0.0**](https://github.com/perditioinc/forksync) — 68s for 805 repos: 50 concurrent calls, Cloud Run + Redis + VPC, smart scheduling, 91% faster than v1  
  last commit: `2026-03-17` · 1 stars · 0 open issues
  _50 concurrent calls · Cloud Run + Redis + VPC · Smart scheduling · 91% faster than v1_

---

## In Progress

- [**reporium-db**](https://github.com/perditioinc/reporium-db) — GraphQL batch fetch, schedule tiers, checkpoint/resume, partitioned JSON: target 10K repos  
  last commit: `2026-03-19` · 1 stars · 0 open issues
- [**reporium-dataset**](https://github.com/perditioinc/reporium-dataset) — Nightly auto-generated README, top repos table, freshness indicator, public dataset mirror  
  last commit: `2026-03-19` · 1 stars · 0 open issues
- [**portfolio**](https://github.com/perditioinc/portfolio) — Real metrics from live sources, auto-updates nightly, link to live products  
  last commit: `2026-03-19` · 1 stars · 0 open issues
- [**reporium-roadmap**](https://github.com/perditioinc/reporium-roadmap) — This file: live commit dates, feature tracking, version history  
  last commit: `2026-03-19` · 1 stars · 0 open issues
- [**reporium-metrics**](https://github.com/perditioinc/reporium-metrics) — Nightly collection, ASCII trend charts, milestone tracking  
  last commit: `2026-03-19` · 1 stars · 0 open issues

---

## Coming Next

- [**repo-intelligence**](https://github.com/perditioinc/repo-intelligence) — 0-100 repo scorer: README, activity, community, CI. Pip-installable.
- **reporium frontend v2** — Figma-designed UI: faster, cleaner, better filtering
- **reporium enterprise** — Self-hosted for internal repos

---

## Backlog

- **reporium observability** — Latency dashboards, error rate tracking, SLO definitions
- **public API v2** — Rate-limited public REST API with API keys

---

## Changelog

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


---

*Platform **v0.3.0** · Last updated: 2026-03-19 · See [CHANGELOG.md](CHANGELOG.md) for version history.*
