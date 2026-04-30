# Reporium Roadmap
<!-- perditio-badges-start -->
[![Tests](https://github.com/perditioinc/reporium-roadmap/actions/workflows/test.yml/badge.svg)](https://github.com/perditioinc/reporium-roadmap/actions/workflows/test.yml)
[![Nightly](https://github.com/perditioinc/reporium-roadmap/actions/workflows/update.yml/badge.svg)](https://github.com/perditioinc/reporium-roadmap/actions/workflows/update.yml)
![Last Commit](https://img.shields.io/github/last-commit/perditioinc/reporium-roadmap)
![python](https://img.shields.io/badge/python-3.11%2B-3776ab)
![suite](https://img.shields.io/badge/suite-Reporium-6e40c9)
<!-- perditio-badges-end -->

> Track every meaningful AI development tool on GitHub.

---

## Current State

### Working

- [**reporium.com v0.7.0**](https://reporium.com) — Live (HTTP 200). FAQ page now in PR #273 (`feat(faq): /faq + client spend-surface mitigation (KAN-272, supersedes #272)`); PR #272 (`feat(faq): add /faq page rendering every curated Ask suggestion`) was closed 2026-04-25T11:39:02Z as superseded by #273 (close-out completed before #273 merges, as planned). Inline citation linking, jellyfish hover tooltips, and security hotfix #264 (44 leaked private repos removed from library.json) all shipped earlier in the cycle. Banner stickiness fix shipped. Progressive loading (owned.json + library.json) still in place. Last release tag v0.7.0.  
  last commit: `2026-04-30`
- [**reporium-api v1.6.0**](https://reporium-api-573778300586.us-central1.run.app/docs) — Cloud Run, /health 200 ok (verified 2026-04-24). Live /library/full reports 1,856 repos; /graph/edges reports 1,895 total / 1,768 with embeddings. 39 alembic migrations on head (039_query_log_query_id). /intelligence/ask + smart routing + follow-up suggestion chips live. DB backend is Cloud SQL (migrated from Neon 2026-04-15). Main HEAD 58ab8cd (#433). NullPool-safe /health pool telemetry: PR #441 (`fix(health): NullPool-safe pool telemetry on /health (#354 follow-up)`, head `3b52231`) is open with all 4 required CI checks green (Tests, Dev Tests, ask-quality-gate, migration-smoke); PR #441 is a self-contained green replacement for the earlier PR #435 whose CI went red because `NullPool` lacks `.size()`/`.checkedout()`/`.overflow()`. PR #435 was closed 2026-04-25T11:38:47Z as superseded by #441. Last tag v1.6.0; openapi reports app version 1.1.0 — version drift between tag and FastAPI app — flagged for follow-up.  
  last commit: `2026-04-28`
- [**reporium-mcp**](https://github.com/perditioinc/reporium-mcp) — MCP server giving Claude/Workato direct access to the live library. 18 tools across 7 modules (search, taxonomy, intelligence, graph, quality, repos, …). HTTP bridge deployed to Cloud Run via cloudbuild.http.yaml (KAN-163). Migrated to Workload Identity Federation; deploy auth probe replaced ID-token smoke test. Used by 3 Workato recipes.  
  last commit: `2026-04-27`
- [**reporium-ingestion v1.3.0**](https://github.com/perditioinc/reporium-ingestion) — Cloud Run Job for nightly enrichment proven end-to-end (181 repos / 0 errors on first scheduled fire). Legacy GitHub Actions enrichment cron removed (PR #65). Graph-build CI surfaces Cloud Run Job diagnostics on failure (PR #66). Main HEAD `4c5f2f3`; tag v1.3.0 at `cd9fb16`. An unmerged follow-up branch `ci/graph-build-failure-ergonomics` (`025a60b`) further improves graph-build CI ergonomics — not on main as of 2026-04-24.  
  last commit: `2026-04-30`
- [**forksync**](https://github.com/perditioinc/forksync) — Cloud Run nightly sync. Cache migrated from Cloud Memorystore to Upstash Redis REST API (PR #1). SYNC_REPORT.md still committed after each run.  
  last commit: `2026-04-10`
- [**reporium-db v1.0.0**](https://github.com/perditioinc/reporium-db) — Nightly sync. 1858 repos in published index.json across 40 languages. GraphQL 5xx resilience + correct checkpoint cursor landed on main via PR #11 (merge commit `9c0dad3`, merged 2026-04-23T04:56Z). 403 retry with 300s Retry-After cap (PR #10, `53b7c44`) live since 2026-04. Main HEAD `5816999` (build, 2026-04-24).  
  last commit: `2026-04-30`
- [**reporium-events v1.0.0**](https://github.com/perditioinc/reporium-events) — Now public on GitHub (was local-only as of 2026-03). GCP Pub/Sub topic 'reporium-events' live. 8 event schemas (sync.completed, db.synced, ingestion.completed, repo.added, repo.updated, health.check, build.failed, api.deployed). Async Firestore transactional fix shipped (PR #2).  
  last commit: `2026-04-10`
- [**reporium-audit**](https://github.com/perditioinc/reporium-audit) — Nightly 8am UTC audit of all platform components, AUDIT_REPORT.md auto-generated. Knowledge graph edge count regression check added (4ddc6dd).  
  last commit: `2026-04-29`
- [**perditio-devkit**](https://github.com/perditioinc/perditio-devkit) — Shared tooling: badges, GitHub client, file utilities, reusable test failure workflow. Used by all suite repos.  
  last commit: `2026-03-23`

### Not Working

- [**openapi version drift**](https://github.com/perditioinc/reporium-api) — Live /openapi.json reports app version 1.1.0 while git tag is v1.6.0. Symptom of FastAPI `version=` constant being out of date. Cosmetic but breaks any external consumer that reads openapi for version pinning.
- [**knowledge-graph edge total — not verified on 2026-04-24**](https://github.com/perditioinc/reporium-api) — Older roadmap claimed 6,209 edges on a 1,406-repo corpus. Corpus is now 1,856 and ALTERNATIVE_TO is the only edge type observed in a sampled /graph/edges call. A current total has not been measured this cycle. needs verification.

---

## Fixing Now

- **Ask UX trust + safety hardening** — Lane-coordinated work across 8+ parallel lanes (2026-04-24, revalidated 2026-04-25 AM): NullPool-safe /health (PR #441 — green, all CI pass; supersedes PR #435), stale Cloud Run candidate-tag cleanup (PR #436), library stats fix (PR #438), forbidden_repos primitive (PR #439), data-quality X-Admin-Key fix (PR #440), `hn_mentions_count` evaluation field (PR #434), FAQ product decision (PR #273 — `feat(faq): /faq + client spend-surface mitigation (KAN-272, supersedes #272)`; PR #272 closed 2026-04-25T11:39:02Z as superseded — close-out completed before #273 merges).
- **Roadmap sync (this PR)** — Update reporium-roadmap to reflect validated 2026-04-24 PM suite state. Builds on the v0.8.0 (02:10 PDT) sync and v0.8.1 (PM correction). NullPool /health rewritten to point at PR #441 (green replacement for #435 whose CI went red on `NullPool` lacking `.size()`/etc.); reporium-ingestion main HEAD corrected from `025a60b` → `4c5f2f3` (`025a60b` is the unmerged `ci/graph-build-failure-ergonomics` follow-up branch, not on main); fixing_now lane list expanded to include PRs #434 and #440. Owned files only.

---

## Next Up — Q2 2026

- Resolve openapi/tag version drift in reporium-api
- Re-measure knowledge-graph edge totals after 2026-04 enrichment work
- Land FAQ product decision (PR #273 — supersedes PR #272)
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

## Changelog

### v0.8.4-roadmap-status-plus6h-refresh - 2026-04-25
+6h Roadmap/Status Lane refresh. PR #272 (`feat(faq): add /faq page rendering every curated Ask suggestion`) closed 2026-04-25T11:39:02Z as superseded by #273; PR #435 (NullPool /health, `feat(health): pool stats`) closed 2026-04-25T11:38:47Z as superseded by #441. Both close-outs match the supersession disposition the v0.8.2/v0.8.3 syncs already documented — this patch only updates the status word `open`/`remains open`/`still open` to `closed <ISO>` in the three places where it appeared (reporium evidence, reporium-api evidence, fixing_now Ask UX description), plus the corresponding spots in README.md and REPORIUM_ROADMAP.md. No application repos modified. No upstream PRs merged in the +6h window. Owned files only: roadmap.json, README.md, REPORIUM_ROADMAP.md, CHANGELOG.md, .audit/2026-04-25/.

### v0.8.3-roadmap-sync-pr273 - 2026-04-25
AM revalidation pass on top of v0.8.2. One stale claim fixed: PR #272 (`feat(faq): add /faq page rendering every curated Ask suggestion`) was superseded overnight by PR #273 (`feat(faq): /faq + client spend-surface mitigation (KAN-272, supersedes #272)`). Both PRs are still OPEN as of 2026-04-25 AM (verified via `gh pr view 272/273`); PR #273 carries the spend-surface mitigation that PR #272 lacked, and the dispatch sheet now lists #272 for close-out before #273 merges. Updated reporium evidence, fixing_now description, and next_up FAQ line to point at #273 with #272 marked superseded. `as_of` advanced 2026-04-24 → 2026-04-25 to match the revalidation date. No application repos modified. Owned files only: roadmap.json, README.md, REPORIUM_ROADMAP.md, CHANGELOG.md, tests, .audit/2026-04-25/.

### v0.8.2-roadmap-sync-pr441 - 2026-04-24
Late-PM follow-up to v0.8.1. Two stale claims corrected against owned files only. (1) NullPool-safe /health: v0.8.0 said `PR #435 — open, pending merge`. PR #435's CI in fact went red because `NullPool` lacks `.size()`/`.checkedout()`/`.overflow()`; a self-contained green replacement was opened as PR #441 (`fix(health): NullPool-safe pool telemetry on /health (#354 follow-up)`, head `3b52231`, all 4 required CI checks green: Tests, Dev Tests, ask-quality-gate, migration-smoke). reporium-api evidence and fixing_now updated to point at #441 with #435 marked superseded but still open. (2) reporium-ingestion main HEAD: v0.8.0 evidence said `head 025a60b`. Verified main HEAD is `4c5f2f3` (#66, ci/graph-build diagnostics merge). `025a60b` is the unmerged follow-up branch `ci/graph-build-failure-ergonomics` and is *not* on main. fixing_now lane list also expanded to include PR #440 (data-quality X-Admin-Key) and PR #434 (hn_mentions_count). No code change to generate.py; owned files only (roadmap.json, README.md, REPORIUM_ROADMAP.md, CHANGELOG.md, tests, .audit/2026-04-25/).

### v0.8.1-roadmap-sync-correction - 2026-04-24
Correction to v0.8.0-roadmap-sync (same-day, PM follow-up). The 02:10 PDT sync claimed reporium-db's GraphQL 5xx companion fix (`f3a099e`) was on a feature branch only — that was wrong by ~22 hours. PR #11 (`fix(fetcher): GraphQL 5xx resilience — 6 retries, jitter, correct checkpoint`) had already merged to main as commit `9c0dad3` on 2026-04-23T04:56Z. reporium-db evidence updated accordingly; solved_lanes entry renamed `DB sync GraphQL 403 retry-after cap` → `DB sync GitHub 403 + GraphQL 5xx resilience` and now lists both PRs as resolved on main. Main HEAD pinned to `5816999` (build, 2026-04-24). No application repos modified. Owned files only: roadmap.json, README.md, CHANGELOG.md, REPORIUM_ROADMAP.md, tests.

### v0.8.0-roadmap-sync - 2026-04-24
Roadmap sync to validated 2026-04-24 suite reality. Corpus updated 1,406 → 1,856 (live API /library/full). DB backend Neon → Cloud SQL (migrated 2026-04-15, KAN-120). reporium-mcp added to working list (HTTP bridge on Cloud Run, 18 tools, WIF deploy, used by 3 Workato recipes). reporium-events moved from 'local only' to public on GitHub. Alembic head 004 → 039 (039_query_log_query_id). openapi/tag version drift in reporium-api (openapi reports 1.1.0, tag v1.6.0) flagged in not_working. Knowledge-graph edge total marked needs-verification (no current measurement). Per-repo HEAD commits pinned: reporium-api 58ab8cd, reporium-ingestion 4c5f2f3 (v1.3.0 at cd9fb16), reporium-mcp d5b6d11, reporium-events 81a51fd. NullPool-safe /health softened to 'PR #435 open, pending merge as of 2026-04-24'. reporium-db evidence corrected: 403-retry-with-cap (PR #10) is on main; the GraphQL 5xx companion (`f3a099e`) is on a feature branch only. New `solved_lanes` array enumerates 8 already-shipped lanes (3 P2s closed today + Neon→Cloud SQL + reporium-events publication + reporium-mcp WIF + forksync Upstash + SEC-HOTFIX #264) so future runs do not re-open them. Original 10K/100K corpus targets acknowledged as missed; new targets pending product input. Lane work for 2026-04-24 dispatch summarized in fixing_now.

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

*Platform **v0.7.0** · Last updated: 2026-04-30 · See [CHANGELOG.md](CHANGELOG.md) for version history.*
