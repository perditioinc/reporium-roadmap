## v0.8.0-roadmap-sync - 2026-04-24

Sync of `roadmap.json`, `README.md`, and `REPORIUM_ROADMAP.md` to actual suite
state on 2026-04-24. No code change to `generate.py`; source-of-truth content
only, plus six new contract tests (`tests/test_generate.py`) that pin the new
state so it cannot silently regress.

Highlights:
- Corpus updated from claimed 1,406 → measured **1,856** repos (live `/library/full`).
- DB backend updated **Neon → Cloud SQL** (migrated 2026-04-15).
- Alembic head updated **004 → 039**.
- `reporium-mcp` added to working list (live on Cloud Run via HTTP bridge,
  18 tools, used by 3 Workato recipes).
- `reporium-events` moved from "local only" to **public on GitHub**.
- `reporium-api` openapi/tag version drift (openapi reports 1.1.0, tag v1.6.0)
  flagged in `not_working` for follow-up.
- Knowledge-graph edge total marked **needs verification** (was 6,209 on the
  old 1,406-repo corpus; not re-measured this cycle).
- Original 10K-by-end-of-March / 100K-by-end-of-April targets preserved in a
  new `historical_targets` block — kept honest, not silently rewritten.

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
