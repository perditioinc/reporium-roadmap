# Reporium Roadmap

> Track every meaningful AI development tool on GitHub. 10K repos by end of March 2026. 100K by end of April 2026.

---

## Current State

### Working

- [**reporium.com**](https://reporium.com) — Live — 818 repos browseable, full-text search, mobile responsive  
  last commit: `2026-03-18` · 1 stars
- [**forksync v2**](https://github.com/perditioinc/forksync) — 68s for 818 repos on Cloud Run, nightly cron active at 6am UTC  
  last commit: `2026-03-19` · 1 stars
- [**reporium-db**](https://github.com/perditioinc/reporium-db) — Nightly sync active, 818 repos tracked, 29 languages, GraphQL batch fetch  
  last commit: `2026-03-19` · 1 stars
- [**reporium-api**](https://github.com/perditioinc/reporium-api) — Running locally at localhost:8000, 702 repos in DB, 571 have ai_dev_skills  
  last commit: `2026-03-15` · 1 stars

### Not Working

- [**reporium-ingestion**](https://github.com/perditioinc/reporium-ingestion) — Pipeline not running in cloud — 0 categories enriched, 0 readme summaries
- **reporium-api cloud deployment** — Local only — no public endpoint, not deployed to GCP
- **forksync SYNC_REPORT.md** — v2 on Cloud Run does not write SYNC_REPORT.md back to GitHub (workflow fix deployed, pending next nightly run)
- **AI categories** — Only 'tooling' exists in reporium-db — real AI categorization requires ingestion pipeline

---

## Fixing Now

- **forksync SYNC_REPORT.md** — Nightly workflow now captures Cloud Run output and commits SYNC_REPORT.md — unblocks metrics and portfolio
- **reporium-ingestion pipeline** — Fix cloud deployment — unblocks categories, summaries, reporium.com usefulness
- **reporium-api cloud deployment** — Deploy to GCP — unblocks public read endpoint

---

## Next Up — end of March 2026

- 10K repos tracked in reporium-db
- Categories working (requires ingestion pipeline fix)
- reporium-api deployed to cloud with public read endpoint

---

## Target: end of April 2026

- 100K repos tracked
- repo-intelligence library live on PyPI
- reporium frontend v2 (Figma-designed)

---

## Coming Next

- [**repo-intelligence**](https://github.com/perditioinc/repo-intelligence) — 0-100 repo scorer: README, activity, community, CI. Pip-installable.
- **reporium frontend v2** — Figma-designed UI: faster, cleaner, better filtering
- **reporium enterprise** — Self-hosted for internal repos

---

## Changelog

### v0.3.0 - 2026-03-18
6 new repos built, forksync v2 live, reporium-db nightly sync active, 147 tests passing

### v0.2.0 - 2026-03-01
reporium-ingestion pipeline built, 12 AI categories defined

### v0.1.0 - 2026-01-01
reporium.com and reporium-api first deployed


---

*Platform **v0.3.0** · Last updated: 2026-03-19 · See [CHANGELOG.md](CHANGELOG.md) for version history.*
