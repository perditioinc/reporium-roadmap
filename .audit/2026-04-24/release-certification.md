# Reporium Release Certification — 2026-04-24 (post-wave)

**Coordinator lane.** Evidence-only. No product-code edits. No merges.
No deploys.

**Evidence timestamp:** 2026-04-24 ~02:10 PDT (wall) /
 ~09:10 UTC, six hours after the wave-1 dispatch.

**Repo anchors (at time of audit):**

- `reporium-api` `main` HEAD: `58ab8cd` (`fix(intelligence): newest/oldest smart route references non-existent column (#433)`).
- `reporium-ingestion` `dev` HEAD: last green Tests run 2026-04-23 04:57 UTC.
- `reporium-audit`, `perditio-workato-integration`, `reporium-roadmap`:
  `main` is ahead of every local `claude/feature/KAN-*` branch — lanes
  9 / 10 / 12 produced **zero commits**.

---

## Executive verdict

**Five PRs are safe to review-and-merge now; one PR is red; three
lanes never started; two failures require ops action outside code.**

| Status | Count | IDs |
|---|---|---|
| Safe, ready for human review | 5 | PR #434, #436, #438, #439, #440 |
| Safe, decision deferred to base-branch policy | 1 | PR #272 |
| Still needs code work | 1 | PR #435 |
| Blocked on external (ops) validation | 2 | nightly-graph-build (L3), data-quality workflow (L8) |
| Not started | 3 | L9 audit hardening, L10 Workato recipes, L12 roadmap sync |
| Done (doc-only, no code) | 2 | L3 RCA, L11 Ask/FAQ UX spec |

PR #435 is the **single hard blocker**: CI is red with
`AttributeError: 'NullPool' object has no attribute 'size'` across 10+
tests. The in-memory notes (and five separate claude-mem observations)
claim the fix was made NullPool-safe, but `origin/fix/health-pool-stats-354`
HEAD `e9b6493` still has the unguarded call at `app/main.py:360`
(`pool.size()`) with no `hasattr` / `isinstance(pool, NullPool)` fallback.
**The fix was never pushed.**

---

## Part A — Lane classification

### Canonical per-lane status

Mergeability, CI, and mergeable-at-audit columns are current evidence
from `gh pr view` / `gh run list` — not prior lane notes.

| # | Lane | Artifact | CI status | Mergeable | Verdict |
|---|---|---|---|---|---|
| 1 | `/health` NullPool (PR #435) | branch + failing CI | ❌ Tests/Dev Tests FAIL (`NullPool.size` AttributeError in 10+ tests) | yes, MERGEABLE (but would land red to main) | **Still needs code work** |
| 2 | PR #436 deploy tag cleanup | `pr-436-review.md`: APPROVE AND MERGE | ✅ all required checks green | yes | **Safe and ready for human review** |
| 3 | Nightly graph-build RCA | `nightly-graph-build-root-cause.md`: RCA complete | last scheduled run 2026-04-23 red; cause = stale `reporium-db-url` secret (DB password rotated 2026-04-22) | n/a (investigation) | **Blocked on external validation** (GCP secret rotation) |
| 4 | PR #272 FAQ decision | `pr-272-faq-decision.md`: MERGE AS-IS, mitigation deferred | n/a from this side; PR targets `main` but `reporium/CLAUDE.md` says feature branches → `dev`. Dispatch-sheet "Conflict 4" — inert for this decision lane. | yes | **Safe; base-branch policy call pending** |
| 5 | PR #434 `hn_mentions_count` | `pr-434-review.md`: GO (approve) | ✅ all green | yes | **Safe and ready for human review** |
| 6 | PR #438 library.stats | `pr-438-review.md`: GO (approve) | ✅ all green | yes | **Safe — merge after #436 so the shared `deploy.yml` commit `5235333` drops out of the #438 diff** |
| 7 | PR #439 forbidden_repos | `pr-439-review.md`: GO with caveat | ✅ all green | yes | **Safe and ready for human review** |
| 8 | Data-quality verification | `data-quality-check-verification.md` — superseded by PR #440 (`fix(data-quality): pass X-Admin-Key to /metrics/data-quality`) | ✅ PR #440 all green | yes | **Safe and ready for human review.** After merge, ops must manual-dispatch `data-quality.yml` to confirm 5-day failure streak ends. |
| 9 | `reporium-audit` hardening | draft JIRA present; local branch `claude/feature/KAN-AUDIT-reporium-audit-hardening` has **0 commits ahead of main**; no PR | none | n/a | **Not started / superseded for today** |
| 10 | Workato recipes | draft JIRA present; local branch has **0 commits ahead of main**; no PR | none | n/a | **Not started** |
| 11 | Ask/FAQ UX safety design spec | `reporium/.audit/2026-04-24/reporium-ask-faq-design-memo.md` (spec-only) | n/a | n/a | **Done — doc-only deliverable landed in `reporium/.audit/`** |
| 12 | `reporium-roadmap` reality sync | draft JIRA present; local branch has **0 commits ahead of main**; no PR | none | n/a | **Not started — correctly deferred until L1–L10 have settled** |

### Evidence notes worth pinning

- **PR #440 is new today.** It was not in the original 12-lane
  dispatch but landed as the concrete plumbing fix for L8. Treat it as
  the L8 artifact.
- **L9 / L10 / L12 idle-but-branched.** Branches exist locally, zero
  commits, zero PRs, nothing pushed. Safe to either pick up in a
  follow-up wave or retire.
- **PR #436 ↔ PR #438 merge-order is real.** `gh pr diff 438` still
  shows `deploy.yml` commit `5235333` as its first patch — identical
  to PR #436's HEAD. Merge #436 first; rebase #438; duplicate commit
  drops out. This is the only multi-hop serial dependency in the wave.

---

## Part B — No-regression matrix

Legend: ✅ proven safe · ⚠ partial / watchpoint · ❌ regression risk
not covered · ⏳ proof pending external action.

| # | Risk area | Touched by | Current proof | Gap / watchpoint | Verdict |
|---|---|---|---|---|---|
| 1 | **Deploy safety** (prevent stale `allUsers`-invokable candidate tags re-exposing pre-promotion revisions) | PR #436 (L2) | Green CI on `.github/workflows/deploy.yml`. Review verified the `filter('percent=0').extract(tag)` selector cannot touch the live serving revision. `continue-on-error: true` so a flaky `gcloud` call cannot break a successful deploy. Live service at audit time has one traffic entry with candidate tag on current revision → selector is a no-op, which is the correct steady state. | The cleanup step never ran yet in prod (PR unmerged). First real exercise is the next production deploy. | ✅ (once merged) |
| 2 | **`/health` endpoint correctness** (must not crash under NullPool in CI or under connection-pool edge cases) | PR #435 (L1) | None. `origin/fix/health-pool-stats-354` HEAD `e9b6493` still calls `pool.size()` unguarded at `app/main.py:360`. CI run `24874659096` returns `AttributeError: 'NullPool' object has no attribute 'size'` on 10+ tests (`test_health`, `test_cors`, `test_rate_limiting`, `test_repos::test_health`, `test_security::test_health_does_not_leak_secrets`). `main` HEAD `58ab8cd` does not have the pool-stats block, so **prod `/health` is currently safe**; merging #435 as-is would ship the regression. | Code-level gap: PR #435 must either `hasattr(pool, "size")` / `isinstance(pool, NullPool)`-guard or skip the stats block when the engine runs with `poolclass=NullPool`. | ❌ (PR red; do not merge) |
| 3 | **Graph freshness** (Nightly Graph Build keeps the knowledge graph from going stale) | L3 RCA (investigation) | RCA identifies root cause: Cloud Run Job `reporium-graph-build` cannot auth to Cloud SQL because secret `reporium-db-url:latest` holds the pre-rotation password; DB rotated 2026-04-22. `reporium-api` uses IAM auth so is unaffected. Last failing run 2026-04-23 10:00 UTC; last successful 2026-04-22 09:57 UTC. Next scheduled run 2026-04-24 10:00 UTC will also fail unless the secret is rotated. | No repo fix exists or is needed — this is an **external ops action** (add a new version to `reporium-db-url` with the post-rotation password). Lane delivered the RCA; secret rotation is out-of-scope for code. | ⏳ (pending ops secret rotation) |
| 4 | **Ask correctness** (no regression in retrieval quality, no new shortcut that lets "alternatives to X" return X) | PR #439 (L7) — test-only primitive. PR #272 (L4) — new Ask-caller surface. | PR #439: `forbidden_repos` primitive only wires into `tests/test_ask_golden_numeric.py` + `golden_set_ask.yaml`; it does not touch the production Ask path. PR #272: `/faq` uses only existing `/intelligence/ask` endpoint with the existing `NEXT_PUBLIC_APP_API_TOKEN` and pins each question to a deterministic smart-route (≈0 LLM tokens). Ask Quality Gate green on every PR in scope (#434, #435, #436, #438, #439, #440). | PR #439's *first use* of the primitive does not cover issue #365 regression-guard the way the PR description implies (mechanical, not fatal — captured in review). | ✅ |
| 5 | **Data-quality automation** (scheduled `/metrics/data-quality` probe that gates on classified ≥ 90 %, categories ≥ 10, tags ≥ 50) | PR #440 (emergent L8 artifact) | 5 consecutive scheduled failures (2026-04-19 → 2026-04-23). PR #432 fixed the psycopg2→HTTPS rewrite but did not carry `X-Admin-Key`; live probe returned `403 Admin key required for metrics endpoints`. PR #440 passes `ADMIN_API_KEY` via `X-Admin-Key`; all required checks green. | After merge: ops must `gh workflow run data-quality.yml --ref main` to confirm the streak ends. A green dispatch distinguishes a plumbing-fix success from a real data-quality regression. | ⚠ (green after merge **and** manual dispatch) |
| 6 | **Public spend surface** (curious users hitting `/faq` cannot wave-DoS the Ask budget) | PR #272 (L4) | Review quantified: worst case 16 smart-route calls per visit, no shared rate counter, no answer cache, all paths under the 10/min / 100/day per-IP budget already enforced on `/intelligence/ask`. Mitigation (shared rate counter + 1 h answer cache) drafted as a follow-up JIRA — **not shipped in #272**. | Risk scales with traffic, not code. If L4 merges before the mitigation PR, a Hacker News or LinkedIn spike on `/faq` can contend with Ask traffic on the same DB pool (which is already at ceiling per `project_ask_sprint1_apr22.md`). | ⚠ (watchpoint; ship mitigation before any public launch) |

### Areas with no proof in this wave

Nothing in today's 12 lanes exercised:

- **Enrichment correctness** (16-category taxonomy, 90 % classified
  floor). Data-quality probe (row 5) is the closest proxy; until PR
  #440 lands and a manual dispatch goes green, we do not have a fresh
  reading.
- **Embeddings / pgvector freshness.** Not in scope for any lane
  today.
- **Off-topic / injection regex bypass.** KAN-366 already landed
  (`d69da25` on main). No new proof this wave.

These are not regressions — just areas where *this wave* does not
produce evidence. They are tracked in `project_reporium_audit.md`
and `project_reporium_security_pentest.md` and do not block the
merge set recommended below.

---

## Part C — Current suite state

### Release-ready items (safe to ship in this order)

1. **PR #436** — `fix(deploy): strip stale traffic tags after
   promotion`. All green. Review approved. Ship this first: PR #438
   carries its commit as a dependency.
2. **PR #438** — `fix(library): make stats.total_forks / languages
   corpus-wide (#344)`. All green. After #436 lands, rebase #438; the
   duplicate `deploy.yml` commit drops out. Then merge.
3. **PR #440** — `fix(data-quality): pass X-Admin-Key to
   /metrics/data-quality`. All green. After merge, ops manual-dispatch
   `data-quality.yml` to confirm plumbing is green end-to-end.
4. **PR #434** — `fix(evaluation): surface hn_mentions_count (#369)`.
   All green. Additive field, independent of everything else.
5. **PR #439** — `test(ask): add forbidden_repos primitive to
   golden-set gate (#367)`. Test-only; safe at any point in the order.

### Safe but gated on a policy decision

6. **PR #272** — `/faq` page. Review recommends merge-as-is with the
   shared-rate-counter + 1 h-answer-cache mitigation deferred to a
   follow-up PR. **Before merging**, resolve "Conflict 4": dispatch
   sheet says `reporium` feature branches go to `main`;
   `reporium/CLAUDE.md` says `dev`. Since #272 currently targets
   `main`, the human merger must either re-point the PR at `dev` or
   explicitly accept the deviation for this PR.

### Not ready to merge

- **PR #435** (`/health` NullPool). **Do not merge.** Branch still has
  unguarded `pool.size()` at `app/main.py:360`; CI is red with
  `AttributeError: 'NullPool' object has no attribute 'size'` across
  10+ tests. The author of PR #435 must push the NullPool guard to
  `origin/fix/health-pool-stats-354` and re-run CI. Recommended guard
  (not applied from this lane): `isinstance(pool, NullPool)` early
  return with `{"pool": {"enabled": false}}`, or `hasattr(pool,
  "size")` per-field guards.

### Blocked on external action

- **Nightly Graph Build (L3).** No code fix needed. Ops must add a
  new version to GCP Secret Manager secret `reporium-db-url` with the
  current Cloud SQL password. Once rotated, the next scheduled run at
  10:00 UTC will verify. Until then, the knowledge graph goes stale
  one more day at a time.
- **Data-quality workflow (L8 / PR #440).** Nothing external blocks
  the PR; after human merge, ops triggers one manual dispatch to
  confirm the 5-day failure streak breaks.

### Not started / deferred

- **L9** `reporium-audit` hardening — local branch exists, 0 commits,
  no PR. Pick up in a later wave or retire.
- **L10** Workato recipe validation — local branch exists, 0 commits,
  no PR. Same posture as L9.
- **L12** `reporium-roadmap` reality sync — local branch exists, 0
  commits, no PR. Correctly deferred per dispatch: must wait for
  L1–L10 to settle.

---

## Exact next actions (human-owned)

In order. Each action is authoritative once completed; no further
approval round needed.

1. **Author of PR #435** pushes the NullPool guard to
   `origin/fix/health-pool-stats-354` and waits for green CI. Until
   this is done, do not merge. (Memory claimed the fix was done five
   times; verify from `git log origin/fix/health-pool-stats-354 --
   app/main.py` before trusting memory on this again.)

2. **Authorized merger** merges in this order:

   a. `reporium-api` #436 → `main`.

   b. Rebase PR #438 on updated `main`, confirm the duplicate
   `deploy.yml` commit is gone, merge #436's sibling `reporium-api`
   #438 → `main`.

   c. `reporium-api` #440 → `main`, then
   `gh workflow run data-quality.yml --ref main -R perditioinc/reporium-api`
   and confirm the run goes green (or fails on real data thresholds,
   not plumbing).

   d. `reporium-api` #434 → `main`.

   e. `reporium-api` #439 → `main`.

   f. `reporium` #272 → (decide `main` vs. `dev` per Conflict 4),
   then merge.

3. **GCP ops** adds a new version to Secret Manager secret
   `reporium-db-url` in project `perditio-platform` using the current
   Cloud SQL password (rotated 2026-04-22). Confirm with a manual
   `gcloud run jobs execute reporium-graph-build --region us-central1`
   and watch for exit code 0. See
   `reporium-ingestion/.audit/2026-04-24/nightly-graph-build-root-cause.md`
   for the exact commands.

4. **Wave-3 dispatcher** decides whether to pick up L9 (audit
   hardening), L10 (Workato recipes), and L12 (roadmap sync) in a
   follow-up wave, or retire the drafts. If retired, delete the local
   `claude/feature/KAN-*` branches on those three repos since nothing
   is pushed.

---

## Remaining risks

- **PR #435 regression-trap.** If a human merges #435 because memory
  or the lane-1 draft says "NullPool-safe," CI on `main` goes red and
  the `/health` endpoint starts 500-ing in any test suite that runs
  with `poolclass=NullPool`. Guard: the author must push and the
  merger must watch CI on the PR itself, not trust the lane draft.
- **Stale DB secret.** Every day without rotation = one more day of
  graph drift, which feeds directly into Ask retrieval quality. Not a
  code problem but the longest-lived open risk in this suite.
- **`/faq` spend surface without mitigation.** If PR #272 merges
  *and* traffic spikes *before* the follow-up mitigation PR lands,
  the Ask budget and DB pool share the hit. Keep the mitigation PR in
  the same 1–2 day window as the #272 merge if any public
  announcement is planned.
- **Branch-policy drift in `reporium`.** `CLAUDE.md` says `dev`,
  today's dispatch says `main`, PR #272 was cut against `main`.
  Whichever way the call goes, land it as a one-line update to
  `CLAUDE.md` or the next dispatch sheet — not a rolling inconsistency.
- **Accumulated claim-vs-evidence drift in memory.** Five separate
  claude-mem observations claim the PR #435 NullPool fix was shipped;
  origin says otherwise. Before acting on memory-claimed status again,
  verify with `git log origin/<branch>` and `gh run view`.

---

## Inputs consulted

- Dispatch: `.audit/2026-04-24/DISPATCH-SHEET.md`
- Per-lane JIRA drafts: `.audit/2026-04-24/lane-{1..12}-*.md`
- Reviews in `reporium-api/.audit/2026-04-24/`: `pr-434-review.md`,
  `pr-436-review.md`, `pr-438-review.md`, `pr-439-review.md`,
  `data-quality-check-verification.md`.
- Decision doc in `reporium/.audit/2026-04-24/`:
  `pr-272-faq-decision.md`, `reporium-ask-faq-design-memo.md`.
- RCA in `reporium-ingestion/.audit/2026-04-24/`:
  `nightly-graph-build-root-cause.md`.
- `gh pr list` / `gh pr view` / `gh run view` for the seven PRs
  (#272, #434, #435, #436, #438, #439, #440) and for `Nightly Graph
  Build` + `Data Quality Check` workflows.
- `git log origin/fix/health-pool-stats-354 -- app/main.py`
  (confirmed unguarded `pool.size()` at line 360).
