# JIRA fallback: Roadmap and backlog convergence

JIRA is unavailable from this lane; this file stands in for the ticket per the
2026-04-24 dispatch process rule. A real KAN ticket should replace `KAN-ROADMAP`
once JIRA access is restored.

This is the **convergence** pass that follows the earlier roadmap-sync commit
(`3a57373 KAN-ROADMAP: sync roadmap to 2026-04-24 suite reality`). The sync
captured the new reality; this pass makes sure the artifacts converge with
validated suite state and do not silently re-open lanes that other lanes have
already closed today.

## Title
Converge `reporium-roadmap` with validated 2026-04-24 suite state — mark today's
closed lanes, correct overstated claims from the earlier sync commit, and pin
what must not be re-opened.

## Type / Priority
Chore · Medium

## Owner / Lane
Roadmap and backlog convergence lane (2026-04-24 multi-lane dispatch, ~6h into run)

## Branch
`claude/feature/KAN-ROADMAP-roadmap-backlog-convergence` → `main`

## Owned files
- `README.md`
- `REPORIUM_ROADMAP.md`
- `roadmap.json`
- `tests/test_generate.py`, `tests/conftest.py`
- `.audit/2026-04-24/roadmap-backlog-convergence-jira.md` (this file)
- `.audit/2026-04-24/roadmap-backlog-convergence.md` (summary of what changed)

## Problem
The earlier sync commit was broadly accurate but contains two concrete drifts
that would mis-inform downstream lanes if left as-is:

1. `roadmap.json` → `current_state.working[reporium-api].evidence` contains
   `{db_total}` which `generate.py` resolves against
   `reporium-db`/index.json (1,848 on 2026-04-22). The API's own corpus count
   (1,856 via `/library/full`) is a different number from a different source.
   Using `{db_total}` here would print `1,848` for the API line on the next
   nightly render, contradicting the API line in the committed README.
2. The same evidence field says NullPool-safe /health "shipped today (PR #435
   follow-up)". Main HEAD of reporium-api is `58ab8cd` (#433). PR #435 is
   still open; the NullPool fix exists only on a feature branch today. "Shipped"
   is wrong; the accurate status is "PR #435 open — pending merge".

Separately, there is no structured record in `roadmap.json` of which lanes
closed today. Without it, a future run scanning the roadmap will not know that
the three P2s (conftest teardown, legacy nightly cron, DB sync 502 resilience)
already merged and should not be re-proposed.

## Acceptance criteria
1. `roadmap.json` reporium-api evidence no longer uses `{db_total}`; the API
   line uses a stable count or a placeholder that resolves against the API,
   not against reporium-db.
2. The NullPool / PR #435 claim reflects open-PR status, not merged status.
3. `roadmap.json` gains a `solved_lanes` array with the three P2s merged today,
   naming PR numbers and commit SHAs so future lanes can verify before
   re-opening.
4. `README.md` regenerates cleanly from the updated `roadmap.json` via
   `generate.py` (no missing keys, no template errors); the committed
   `README.md` matches the render for consistency.
5. Tests still pass. Updated or new tests pin: `solved_lanes` is present and
   non-empty; the reporium-api evidence does not contain `{db_total}`.
6. A convergence summary is written to
   `.audit/2026-04-24/roadmap-backlog-convergence.md` describing what
   changed, what is now complete, what remains active, and what must not be
   re-opened.

## Validation evidence (re-checked this lane, 2026-04-24)
| Claim | Source | Verified |
|---|---|---|
| reporium-api `/library/full` totalRepos = 1,856 | `curl /library/full?page=1&page_size=1` | ✔ 2026-04-24 09:10 UTC |
| reporium-api `/health` = `{status:ok,db:ok}` | `curl /health` | ✔ 2026-04-24 09:10 UTC |
| reporium-db index.json `meta.total` = 1,848 | `reporium-db/LAST_RUN.md` | ✔ run 2026-04-22 |
| Alembic head `039_query_log_query_id` | `reporium-api/migrations/versions/` ls | ✔ |
| reporium-api `app/main.py` app version = `1.1.0` | grep | ✔ (tag / openapi drift real) |
| reporium-api main HEAD = `58ab8cd` (#433) | `git log --oneline -1` | ✔ |
| reporium-ingestion main HEAD = `025a60b` (graph-build diagnostics) | `git log --oneline -1` | ✔ |
| reporium-db main HEAD = `f3a099e` (GraphQL 5xx resilience) | `git log --oneline -1` | ✔ |
| reporium-mcp main HEAD = `d5b6d11` (deploy auth-enforcement probe) | `git log --oneline -1` | ✔ |
| reporium-events main HEAD = `81a51fd` (Firestore async txn fix #2) | `git log --oneline -1` | ✔ |
| P2 #1 conftest teardown merged as `8c9a872` (#429) | `git log` | ✔ |
| P2 #2 legacy nightly cron removed as `4a58b6c` (#65) | `git log` | ✔ |
| P2 #3 DB sync 502 resilience shipped as `f3a099e` | `git log` | ✔ |
| PR #435 (NullPool /health) merged | `git log --grep=#435` | ✘ NOT on main — still a feature branch |

## Out of scope
- No edits to other repos (process rule 6/7).
- No merge/deploy from this lane.
- No invented JIRA IDs in code; placeholder `KAN-ROADMAP` used until ticket
  exists.
- No retroactive rewrite of the earlier sync commit — convergence is layered
  on top as a follow-up commit so the history is auditable.
