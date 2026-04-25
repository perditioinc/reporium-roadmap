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
- [**reporium-api v1.6.0**](https://reporium-api-573778300586.us-central1.run.app/docs) — Cloud Run, /health 200 ok (verified 2026-04-24). Live /library/full reports 1,856 repos; /graph/edges reports 1,895 total / 1,768 with embeddings. 39 alembic migrations on head (039_query_log_query_id). /intelligence/ask + smart routing + follow-up suggestion chips live. DB backend is Cloud SQL (migrated from Neon 2026-04-15). Main HEAD `58ab8cd` (#433). NullPool-safe /health pool telemetry is in PR #435 — open, pending merge as of 2026-04-24. Last tag v1.6.0; openapi reports app version 1.1.0 — version drift between tag and FastAPI app — flagged for follow-up.
- [**reporium-mcp**](https://github.com/perditioinc/reporium-mcp) — MCP server giving Claude/Workato direct access to the live library. 18 tools across 7 modules (search, taxonomy, intelligence, graph, quality, repos, …). HTTP bridge deployed to Cloud Run via cloudbuild.http.yaml (KAN-163). Migrated to Workload Identity Federation; deploy auth probe replaced ID-token smoke test. Main HEAD `d5b6d11`. Used by 3 Workato recipes.
- [**reporium-ingestion v1.3.0**](https://github.com/perditioinc/reporium-ingestion) — Cloud Run Job for nightly enrichment proven end-to-end (181 repos / 0 errors on first scheduled fire). Legacy GitHub Actions enrichment cron removed (PR #65). Graph-build CI surfaces Cloud Run Job diagnostics on failure (PR #66). Main HEAD `4c5f2f3`; tag v1.3.0 at `cd9fb16`.
- [**forksync**](https://github.com/perditioinc/forksync) — Cloud Run nightly sync. Cache migrated from Cloud Memorystore to Upstash Redis REST API (PR #1). SYNC_REPORT.md still committed after each run.
- [**reporium-db v1.0.0**](https://github.com/perditioinc/reporium-db) — Nightly sync. 1,848 repos in published index.json across 24+ languages (local clone 2026-04-22). 403 retry with 300s Retry-After cap (PR #10, `53b7c44`) live since 2026-04. GraphQL 5xx resilience + correct checkpoint cursor landed on main via PR #11 (merge `9c0dad3`, merged 2026-04-23T04:56Z). Main HEAD `5816999` (build, 2026-04-24).
- [**reporium-events v1.0.0**](https://github.com/perditioinc/reporium-events) — Now public on GitHub (was local-only as of 2026-03). GCP Pub/Sub topic 'reporium-events' live. 8 event schemas (sync.completed, db.synced, ingestion.completed, repo.added, repo.updated, health.check, build.failed, api.deployed). Async Firestore transactional fix shipped (PR #2). Main HEAD `81a51fd`.
- [**reporium-audit**](https://github.com/perditioinc/reporium-audit) — Nightly 8am UTC audit of all platform components, AUDIT_REPORT.md auto-generated. Knowledge graph edge count regression check added (4ddc6dd).
- [**perditio-devkit**](https://github.com/perditioinc/perditio-devkit) — Shared tooling: badges, GitHub client, file utilities, reusable test failure workflow. Used by all suite repos.

### Not Working

- [**openapi version drift**](https://github.com/perditioinc/reporium-api) — Live /openapi.json reports app version 1.1.0 while git tag is v1.6.0. Symptom of FastAPI `version=` constant being out of date. Cosmetic but breaks any external consumer that reads openapi for version pinning.
- [**knowledge-graph edge total — not verified on 2026-04-24**](https://github.com/perditioinc/reporium-api) — Older roadmap claimed 6,209 edges on a 1,406-repo corpus. Corpus is now 1,856 and ALTERNATIVE_TO is the only edge type observed in a sampled /graph/edges call. A current total has not been measured this cycle. needs verification.

---

## Fixing Now

- **Ask UX trust + safety hardening** — Lane-coordinated work across 8+ parallel lanes (2026-04-24): NullPool-safe /health (PR #435), stale Cloud Run candidate-tag cleanup (PR #436), library stats fix (PR #438), forbidden_repos primitive (PR #439), FAQ product decision (PR #272), Data Quality Check workflow verification.
- **Roadmap sync (this PR)** — Update reporium-roadmap to reflect validated 2026-04-24 suite state. Honest restatement of corpus targets that were missed. Adds `solved_lanes` so future runs don't re-open closed work.

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

## Solved Lanes — do not re-open

Future runs MUST NOT re-propose these without first checking the referenced PR/commit.
Source of truth is `roadmap.json → solved_lanes` plus `project_reporium_p2_resolved_apr24.md` in auto-memory.

- **conftest teardown flake** (reporium-api) — PR #429 / main commit `8c9a872` (2026-04-24).
- **Legacy GitHub Actions nightly enrichment cron** (reporium-ingestion) — PR #65 / main commit `4a58b6c` (2026-04-24).
- **DB sync GitHub 403 + GraphQL 5xx resilience** (reporium-db) — PR #10 (`53b7c44`, 2026-04) and PR #11 (merge `9c0dad3`, merged 2026-04-23T04:56Z). Both on main; main HEAD `5816999`.
- **Neon → Cloud SQL DB migration** (reporium-api) — KAN-120 demo-prep session (2026-04-15).
- **reporium-events public publication** — GitHub publication + PR #2 Firestore async txn fix (2026-04). Main HEAD `81a51fd`.
- **reporium-mcp HTTP bridge + Workload Identity Federation** — PRs #12/#13/#14, main HEAD `d5b6d11` (2026-04).
- **forksync cache migration** (Memorystore → Upstash) — PR #1 (2026-04).
- **SEC-HOTFIX #264** (reporium) — 44 leaked private-repo entries removed from public library.json (2026-04).

---

## Historical Targets

These are kept here so the original ambition is not silently rewritten:

- **Stated in v0.7.0 README (2026-03-23):** "10K repos by end of March 2026; 100K by end of April 2026."
- **Outcome as of 2026-04-24:** Not met. Live API reports 1,856 repos. Replacement targets are pending product input.

---

## Changelog

### v0.8.1-roadmap-sync-correction - 2026-04-24
Correction to v0.8.0-roadmap-sync (same-day, PM follow-up). The 02:10 PDT sync claimed reporium-db's GraphQL 5xx companion fix (`f3a099e`) was on a feature branch only — that was wrong by ~22 hours. PR #11 (`fix(fetcher): GraphQL 5xx resilience — 6 retries, jitter, correct checkpoint`) had already merged to main as commit `9c0dad3` on 2026-04-23T04:56Z. reporium-db evidence updated; solved_lanes entry renamed and now lists both PR #10 and PR #11 as resolved on main. Main HEAD pinned to `5816999` (build, 2026-04-24). The `Land reporium-db f3a099e ...` item has been removed from Next Up because it is already on main.

### v0.8.0-roadmap-sync - 2026-04-24
Roadmap sync to validated 2026-04-24 suite reality. Corpus updated 1,406 → 1,856 (live API /library/full). DB backend Neon → Cloud SQL (migrated 2026-04-15, KAN-120). reporium-mcp added to working list (HTTP bridge on Cloud Run, 18 tools, WIF deploy, used by 3 Workato recipes). reporium-events moved from 'local only' to public on GitHub. Alembic head 004 → 039 (039_query_log_query_id). openapi/tag version drift in reporium-api (openapi reports 1.1.0, tag v1.6.0) flagged in not_working. Knowledge-graph edge total marked needs-verification (no current measurement). Per-repo HEAD commits pinned: reporium-api `58ab8cd`, reporium-ingestion `4c5f2f3` (v1.3.0 at `cd9fb16`), reporium-mcp `d5b6d11`, reporium-events `81a51fd`. NullPool-safe /health softened to 'PR #435 open, pending merge'. reporium-db evidence corrected: 403-retry-with-cap (PR #10) is on main; the GraphQL 5xx companion (`f3a099e`) is on a feature branch only. New `solved_lanes` array enumerates 8 already-shipped lanes so future runs do not re-open them. Original 10K/100K corpus targets acknowledged as missed; new targets pending product input.

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
