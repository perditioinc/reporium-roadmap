# Reporium Roadmap
<!-- perditio-badges-start -->
[![Tests](https://github.com/perditioinc/reporium-roadmap/actions/workflows/test.yml/badge.svg)](https://github.com/perditioinc/reporium-roadmap/actions/workflows/test.yml)
[![Nightly](https://github.com/perditioinc/reporium-roadmap/actions/workflows/update.yml/badge.svg)](https://github.com/perditioinc/reporium-roadmap/actions/workflows/update.yml)
![Last Commit](https://img.shields.io/github/last-commit/perditioinc/reporium-roadmap)
![python](https://img.shields.io/badge/python-3.11%2B-3776ab)
![suite](https://img.shields.io/badge/suite-Reporium-6e40c9)
<!-- perditio-badges-end -->

> Track meaningful AI development tooling on GitHub while keeping execution, documentation, and platform status explicit.

---

## Current State Guidance

This README is a planning document, not a live metrics feed. For current repo totals and API-backed corpus size, use current outputs from:

- `reporium-db` generated dataset and README
- `reporium-api` audit/status output
- `reporium-metrics` generated metrics artifacts

### Working

- [**reporium.com**](https://reporium.com) - live and browseable
- [**forksync v2**](https://github.com/perditioinc/forksync) - nightly sync active
- [**reporium-db**](https://github.com/perditioinc/reporium-db) - nightly sync active and current source for live corpus totals
- [**reporium-api**](https://reporium-api-573778300586.us-central1.run.app/docs) - deployed to Cloud Run; current REST-backed repo totals should be taken from live audit/status output, not frozen roadmap text
- [**reporium-events**](https://github.com/perditioinc/reporium-events) - schemas and publisher client exist; downstream consumer integration remains partial
- [**reporium-audit**](https://github.com/perditioinc/reporium-audit) - nightly audit active; `AUDIT_REPORT.md` is runtime-generated and not treated as committed live truth
- [**perditio-devkit**](https://github.com/perditioinc/perditio-devkit) - shared tooling in active use

### Needs Continued Work

- [**reporium-ingestion**](https://github.com/perditioinc/reporium-ingestion) - historical milestone docs exist, but current cloud-operating posture and live enrichment totals should be verified from current runs
- AI category quality and taxonomy expansion - still an active workstream

---

## Branch Strategy

Current suite branch strategy is mixed in practice:

- Repos with a maintained `dev` branch should take feature and fix PRs into `dev` first, then promote `dev` to `main`.
- Repos without a maintained `dev` branch should branch from `main` and PR back to `main`.
- Do not use stale `master` references; active suite repos use `main` and, where present, `dev`.

### Repos Commonly Using `dev` First

- `reporium`
- `reporium-api`
- `reporium-db`
- `reporium-ingestion`
- `reporium-audit`
- `reporium-metrics`
- `reporium-roadmap`
- `reporium-events`

### Repos Currently Operating on `main` Only

- `reporium-security`
- `reporium-scoring`
- `reporium-system-design`
- `reporium-dataset`

This should be treated as current suite practice, not an aspirational future-only policy.

---

## Fixing Now

- commit-data and enrichment follow-through work across the ingestion pipeline
- taxonomy expansion and category quality
- keeping roadmap, metrics, and audit documentation aligned with current suite reality

---

## Near-Term Focus

- continue scaling discovery and ingestion
- improve category and enrichment quality
- wire event-driven automation where the producer/consumer path is actually implemented
- keep docs and execution state aligned across the suite

---

## Historical Milestones

### March 2026 Milestone: 826-Repo Foundation

- the original ingestion/enrichment milestone processed 826 repos
- this is a historical platform milestone, not the current live total

### March 2026 Expansion Snapshot: 1,406 Repos

- some March 2026 planning documents referenced a 1,406-repo expansion snapshot
- treat that as a dated planning snapshot, not the current canonical total

### Naming History

- `reporium-scoring` is the current repo name
- `repo-intelligence` is a former name that should only appear when explicitly labeled as historical

---

## Changelog Highlights

### v0.4.0 - 2026-03-20

Historical milestone: `reporium-api` deployed to Cloud Run, `reporium-events` introduced, `reporium-audit` nightly checks added, and shared tooling expanded.

### v0.3.0 - 2026-03-17

Historical milestone: `reporium-db`, `reporium-dataset`, `reporium-metrics`, `portfolio`, and `reporium-scoring` (then named `repo-intelligence`) launched.

### v0.2.0 - 2026-03-16

Historical milestone: `forksync v2` launched on Cloud Run.

### v0.1.0 - 2026-03-14

Historical milestone: `reporium.com` and `reporium-api` first deployed.

---

*Last updated: 2026-03-24. Use generated outputs from the operational repos for live counts and health.*
