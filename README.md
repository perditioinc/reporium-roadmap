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

- [**reporium.com v0.7.0**](https://reporium.com) — Live — 1406 repos. AskBar fully functional (natural language Q&A over repo library via /intelligence/ask). Progressive loading: owned.json (690KB, 16 repos) renders in ~0.5s, full library.json (5.3MB) merges in background. Repo cards fixed: system tags, builder badges, category aliases, timeline guard. Filter bar clean. MetricsSidebar fixed. AI Dev Coverage all green. CI green, GitHub Pages deployed. 197 tests passing.  
  last commit: `2026-04-03`
- [**reporium-api v1.6.0**](https://reporium-api-573778300586.us-central1.run.app/docs) — Cloud Run revision 00027-2v5. 1406 repos, 6209 knowledge graph edges. /intelligence/ask public endpoint (10/min + 100/day rate limit). Prompt injection + SQL injection fixed. CORS restricted to reporium.com origins. CI/CD auto-deploy on push to main. DB at migration 004 (head): is_private + stargazers_count columns. GH_TOKEN wired for nightly commit stats fetch. 32 unit tests passing.  
  last commit: `2026-04-02`
- [**reporium-ingestion v1.3.0**](https://github.com/perditioinc/reporium-ingestion) — 1406/1406 repos enriched. 14K tags, 2K pmSkills, 918 industries, 825 builders, 4920 categories. fetch_commit_stats.py wired into nightly_enrichment.yml CI. backfill_fork_dates.py ran — all 1390 forks populated.  
  last commit: `2026-03-30`
- [**forksync v2**](https://github.com/perditioinc/forksync) — Cloud Run nightly sync, SYNC_REPORT.md committed after each run.  
  last commit: `2026-04-01`
- [**reporium-db**](https://github.com/perditioinc/reporium-db) — Nightly sync active, 1406 repos tracked.  
  last commit: `2026-04-03`
- [**reporium-events**](https://github.com/perditioinc/reporium-events) — GCP Pub/Sub topic 'reporium-events' live. Event schemas: sync.completed, db.synced, ingestion.completed, repo.added, repo.updated, health.check, build.failed, api.deployed. Publisher client with atomic build_number counter in Firestore. Validated payload schemas.  
  last commit: `2026-03-23`
- [**reporium-audit**](https://github.com/perditioinc/reporium-audit) — Nightly 8am UTC audit of all platform components, AUDIT_REPORT.md auto-generated.  
  last commit: `2026-04-02`
- [**perditio-devkit**](https://github.com/perditioinc/perditio-devkit) — Shared tooling: badges, GitHub client, file utilities — used by all repos.  
  last commit: `2026-03-23`

### Not Working

- [**commit data for 1011 repos**](https://github.com/perditioinc/reporium-ingestion) — fetch_commit_stats.py now wired into nightly CI (7am UTC). Will populate on next nightly run. Not a blocking issue — cards still render, commit section just shows empty.

---

## Fixing Now

- **commit stats backfill** — fetch_commit_stats.py wired into nightly CI — will populate commit data for 1011 repos on next 7am UTC run.
- **reporium taxonomy expansion** — 28 skill areas (Issue #17). Re-enrich all 1406 repos, update frontend to 28 coverage badges, curate tags. Feature branch: feature/taxonomy-expansion. Cowork lane.

---

## Next Up — end of March 2026

- 10K repos tracked in reporium-db
- Taxonomy expansion: 28 skill areas, 58 categories, ~200 curated tags
- Wire ingestion.completed + repo.added events into enrichment pipeline
- API response time monitoring
- Knowledge graph visualization (D3.js/Three.js, 6209 edges)

---

## Target: end of April 2026

- 100K repos tracked
- repo-intelligence library live on PyPI
- reporium frontend v2 (Figma-designed)

---

## Coming Next

- [**repo-intelligence**](https://github.com/perditioinc/repo-intelligence) — 0-100 repo scorer: README, activity, community, CI. Pip-installable.
- **github-ai-trends** — Daily GitHub trending scraper for AI repos. Feeds new repo candidates to reporium-db.
- **reporium frontend v2** — Figma-designed UI: faster, cleaner, better filtering

---

## Changelog

### v0.7.0 - 2026-03-23
AskBar: natural language Q&A over repo library via public /intelligence/ask endpoint (rate limited). Progressive loading: owned.json (690KB) renders in ~0.5s, library.json (5.3MB) merges in background — 87% first-paint payload reduction. CI/CD auto-deploy on push to main for reporium-api. DB migrations 003+004 applied (is_private, stargazers_count). CORS restricted. GH_TOKEN wired for commit stats. PR #16 merged (tag cloud status filter). Issues #27, #30 closed. reporium-api v1.6.0, reporium v0.7.0.

### v0.6.1 - 2026-03-23
MetricsSidebar LIBRARY BY CATEGORY fixed: normalizedCategories passed so stale Audio/Deployment entries no longer appear. jest worktree exclusion added. reporium v0.6.1 tagged.

### v0.6.0 - 2026-03-23
Repo card fixes: system tags removed, category aliases, builder badge, timeline guard. Filter bar stale category normalization. AI Dev Coverage badges all green. Builders section restored. Prompt injection prevention + SQL injection fix in reporium-api. 32 unit tests. SDLC: Git Flow established, dev branch on all repos, CONTRIBUTING.md, semver releases.

### v0.5.0 - 2026-03-22
reporium-api security: private repo exposure fixed (is_private column, WHERE is_private=false). Redis Memorystore cache enabled via VPC connector. CI workflows across suite.

### v0.4.0 - 2026-03-20
reporium-api deployed to Cloud Run, reporium-events Pub/Sub system, reporium-audit nightly health checks, perditio-devkit shared tooling.

### v0.3.0 - 2026-03-17
reporium-db, reporium-dataset, reporium-metrics, portfolio, repo-intelligence all launched.

### v0.2.0 - 2026-03-16
forksync v2 launched on Cloud Run (68s for 818 repos).

### v0.1.0 - 2026-03-14
reporium.com and reporium-api first deployed.


---

*Platform **v0.7.0** · Last updated: 2026-04-03 · See [CHANGELOG.md](CHANGELOG.md) for version history.*
