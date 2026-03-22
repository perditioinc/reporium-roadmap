# Reporium Roadmap
<!-- perditio-badges-start -->
[![Tests](https://github.com/perditioinc/reporium-roadmap/actions/workflows/test.yml/badge.svg)](https://github.com/perditioinc/reporium-roadmap/actions/workflows/test.yml)
[![Nightly](https://github.com/perditioinc/reporium-roadmap/actions/workflows/update.yml/badge.svg)](https://github.com/perditioinc/reporium-roadmap/actions/workflows/update.yml)
![Last Commit](https://img.shields.io/github/last-commit/perditioinc/reporium-roadmap)
![python](https://img.shields.io/badge/python-3.11%2B-3776ab)
![suite](https://img.shields.io/badge/suite-Reporium-6e40c9)
<!-- perditio-badges-end -->

> Track every meaningful AI development tool on GitHub. 10K repos by end of March 2026. 100K by end of April 2026.

---

## Current State

### Working

- [**reporium.com**](https://reporium.com) — Live — 831 repos browseable, full-text search, mobile responsive
- [**forksync v2**](https://github.com/perditioinc/forksync) — Cloud Run nightly sync + SYNC_REPORT.md committed via GitHub API after each run
- [**reporium-db**](https://github.com/perditioinc/reporium-db) — Nightly sync active, 831 repos tracked, 29 languages, GraphQL batch fetch
- [**reporium-api**](https://reporium-api-573778300586.us-central1.run.app/docs) — Deployed to Cloud Run — 0 repos via REST API, Swagger UI public at /docs
- [**reporium-events**](https://github.com/perditioinc/reporium-events) — Pub/Sub topic live, event schemas defined, forksync + reporium-db publishing events
- [**reporium-audit**](https://github.com/perditioinc/reporium-audit) — Nightly 8am UTC audit of all platform components, AUDIT_REPORT.md auto-generated
- [**perditio-devkit**](https://github.com/perditioinc/perditio-devkit) — Shared tooling: badges, GitHub client, file utilities — used by all repos

### Not Working

- [**reporium-ingestion**](https://github.com/perditioinc/reporium-ingestion) — Pipeline not running in cloud — 0 categories enriched, 0 readme summaries
- **AI categories** — Only 'tooling' exists in reporium-db — real AI categorization requires ingestion pipeline

---

## Fixing Now

- **reporium-ingestion pipeline** — Fix cloud deployment — unblocks categories, summaries, reporium.com usefulness
- **10K repos milestone** — Expand GitHub fetcher to discover repos beyond perditioinc forks

---

## Next Up — end of March 2026

- 10K repos tracked in reporium-db
- Categories working (requires ingestion pipeline fix)
- Redis cache enabled on reporium-api

---

## Target: end of April 2026

- 100K repos tracked
- repo-intelligence library live on PyPI
- reporium frontend v2 (Figma-designed)

---

## Coming Next

- [**repo-intelligence**](https://github.com/perditioinc/repo-intelligence) — 0-100 repo scorer: README, activity, community, CI. Pip-installable.
- **github-ai-trends** — Daily GitHub trending scraper focused on AI repos. Scrapes github.com/trending per language (Python, TypeScript, Rust, Go, C++, Jupyter Notebook) for daily, weekly, and monthly time periods. Stores one timestamped snapshot per day. Feeds new repo candidates to reporium-db. Does not do AI enrichment — discovery only.
- **reporium frontend v2** — Figma-designed UI: faster, cleaner, better filtering
- **reporium enterprise** — Self-hosted for internal repos

---

## Changelog

### v0.4.0 - 2026-03-20
reporium-api deployed to Cloud Run (0 repos live), reporium-events Pub/Sub system, reporium-audit nightly health checks, perditio-devkit shared tooling, build counters on all nightly repos, Reporium suite badges across all repos — 0 tests passing

### v0.3.0 - 2026-03-17
reporium-db, reporium-dataset, reporium-metrics, portfolio, repo-intelligence all launched — 0 tests passing across all repos

### v0.2.0 - 2026-03-16
forksync v2 launched on Cloud Run (68s for 818 repos), reporium-ingestion pipeline built — not yet deployed to cloud

### v0.1.0 - 2026-03-14
reporium.com and reporium-api first deployed


---

*Platform **v0.4.0** · Last updated: 2026-03-22 · See [CHANGELOG.md](CHANGELOG.md) for version history.*
