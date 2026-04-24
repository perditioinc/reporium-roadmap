# Reporium Roadmap
<!-- perditio-badges-start -->
[![Tests](https://github.com/perditioinc/reporium-roadmap/actions/workflows/test.yml/badge.svg)](https://github.com/perditioinc/reporium-roadmap/actions/workflows/test.yml)
[![Nightly](https://github.com/perditioinc/reporium-roadmap/actions/workflows/update.yml/badge.svg)](https://github.com/perditioinc/reporium-roadmap/actions/workflows/update.yml)
![Last Commit](https://img.shields.io/github/last-commit/perditioinc/reporium-roadmap)
![python](https://img.shields.io/badge/python-3.11%2B-3776ab)
![suite](https://img.shields.io/badge/suite-Reporium-6e40c9)
<!-- perditio-badges-end -->

> Track every meaningful AI development tool on GitHub.

> **Note:** this README is auto-generated from [`roadmap.json`](roadmap.json) by the nightly workflow.
> If you want to change a status, edit `roadmap.json` (the source of truth), not this file.

---

## Current State

### Working

- [**reporium.com v0.7.0**](https://reporium.com) — Live (HTTP 200). Latest commit 2026-04-23 — FAQ page (PR #272 in flight), inline citation linking, jellyfish hover tooltips, security hotfix #264 took down 44 leaked private repos from library.json. Banner stickiness fix shipped. Progressive loading (owned.json + library.json) still in place. Last release tag v0.7.0.
- [**reporium-api v1.6.0**](https://reporium-api-573778300586.us-central1.run.app/docs) — Cloud Run, /health 200 ok. Live /library/full reports 1,856 repos; /graph/edges reports 1,895 total / 1,768 with embeddings. 39 alembic migrations on head. /intelligence/ask + smart routing + follow-up suggestion chips live. NullPool-safe /health pool telemetry shipped today (PR #435 follow-up). DB backend is Cloud SQL (migrated from Neon 2026-04-15). Last tag v1.6.0; openapi reports app version 1.1.0 — version drift between tag and FastAPI app — flagged for follow-up.
- [**reporium-mcp**](https://github.com/perditioinc/reporium-mcp) — MCP server giving Claude/Workato direct access to the live library. 18 tools across 7 modules (search, taxonomy, intelligence, graph, quality, repos, …). HTTP bridge deployed to Cloud Run via cloudbuild.http.yaml (KAN-163). Migrated to Workload Identity Federation; deploy auth probe replaced ID-token smoke test. Used by 3 Workato recipes.
- [**reporium-ingestion v1.3.0**](https://github.com/perditioinc/reporium-ingestion) — Cloud Run Job for nightly enrichment proven end-to-end (181 repos / 0 errors on first scheduled fire). Legacy GitHub Actions enrichment cron removed (PR #65). Graph-build CI surfaces Cloud Run Job diagnostics on failure (PRs #66 and follow-up). Tag v1.3.0; head 025a60b.
- [**forksync**](https://github.com/perditioinc/forksync) — Cloud Run nightly sync. Cache migrated from Cloud Memorystore to Upstash Redis REST API (PR #1). SYNC_REPORT.md still committed after each run.
- [**reporium-db v1.0.0**](https://github.com/perditioinc/reporium-db) — Nightly sync. 1,848 repos in published index.json across 24+ languages. Stronger GraphQL 5xx resilience landed today (f3a099e). 403 retry with 300s Retry-After cap (PR #10) live since 2026-04.
- [**reporium-events v1.0.0**](https://github.com/perditioinc/reporium-events) — Now public on GitHub (was local-only as of 2026-03). GCP Pub/Sub topic 'reporium-events' live. 8 event schemas (sync.completed, db.synced, ingestion.completed, repo.added, repo.updated, health.check, build.failed, api.deployed). Async Firestore transactional fix shipped (PR #2).
- [**reporium-audit**](https://github.com/perditioinc/reporium-audit) — Nightly 8am UTC audit of all platform components, AUDIT_REPORT.md auto-generated. Knowledge graph edge count regression check added (4ddc6dd).
- [**perditio-devkit**](https://github.com/perditioinc/perditio-devkit) — Shared tooling: badges, GitHub client, file utilities, reusable test failure workflow. Used by all suite repos.

### Not Working

- [**openapi version drift**](https://github.com/perditioinc/reporium-api) — Live /openapi.json reports app version 1.1.0 while git tag is v1.6.0. Symptom of FastAPI `version=` constant being out of date. Cosmetic but breaks any external consumer that reads openapi for version pinning.
- [**knowledge-graph edge total — not verified on 2026-04-24**](https://github.com/perditioinc/reporium-api) — Older roadmap claimed 6,209 edges on a 1,406-repo corpus. Corpus is now 1,856 and ALTERNATIVE_TO is the only edge type observed in a sampled /graph/edges call. A current total has not been measured this cycle. needs verification.

---

## Fixing Now

- **Ask UX trust + safety hardening** — Lane-coordinated work across 8+ parallel lanes (2026-04-24): NullPool-safe /health (PR #435), stale Cloud Run candidate-tag cleanup (PR #436), library stats fix (PR #438), forbidden_repos primitive (PR #439), FAQ product decision (PR #272), Data Quality Check workflow verification.
- **Roadmap sync (this PR)** — Update reporium-roadmap to reflect actual 2026-04-24 suite state. Honest restatement of corpus targets that were missed.

---

## Next Up — Q2 2026

- Resolve openapi/tag version drift in reporium-api
- Re-measure knowledge-graph edge totals after 2026-04 enrichment work
- Land FAQ product decision (PR #272)
- Audit suite hardening + Workato recipe validation (lanes 9–10 from today's dispatch)
- Ask/FAQ UX safety design spec (lane 11)

---

## Target: 2026 H2

- Honest restatement of corpus growth targets — original 10K-by-end-of-March / 100K-by-end-of-April were not met (current ~1,856). New targets need product input.
- repo-intelligence library on PyPI (still planned)
- reporium frontend v2 (Figma-designed) — still planned

---

## Coming Next

- [**repo-intelligence**](https://github.com/perditioinc/repo-intelligence) — 0-100 repo scorer: README, activity, community, CI. Pip-installable. Status: planned (no recent CI runs as of 2026-04-09 audit).
- **github-ai-trends** — Daily GitHub trending scraper for AI repos. Feeds new repo candidates to reporium-db. Status: planned.
- **reporium frontend v2** — Figma-designed UI: faster, cleaner, better filtering. Status: planned.

---

## Historical Targets

These are kept here so the original ambition is not silently rewritten:

- **Stated in v0.7.0 README (2026-03-23):** "10K repos by end of March 2026; 100K by end of April 2026."
- **Outcome as of 2026-04-24:** Not met. Live API reports 1,856 repos. Replacement targets are pending product input.

---

## Changelog

### v0.8.0-roadmap-sync - 2026-04-24
Roadmap sync to reality: corpus updated from 1,406 → 1,856 (live API). DB backend updated from Neon → Cloud SQL (migrated 2026-04-15). reporium-mcp added to working list (HTTP bridge on Cloud Run, 18 tools, used by 3 Workato recipes). reporium-events moved from 'local only' to public on GitHub. Alembic head updated 004 → 039. openapi/tag version drift in reporium-api (openapi reports 1.1.0, tag v1.6.0) flagged in not_working. Knowledge-graph edge total marked needs-verification (no current measurement this cycle). Original 10K/100K corpus targets acknowledged as missed; new targets pending product input. Lane work for 2026-04-24 dispatch summarized in fixing_now.

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

*Platform **v0.7.0** · Last updated: 2026-04-24 · See [CHANGELOG.md](CHANGELOG.md) for version history.*
