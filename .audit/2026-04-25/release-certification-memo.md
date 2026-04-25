# Reporium Release Certification — 2026-04-25

**Lane**: 13 (release certification + merge queue).
**Authoritative dispatch**: `.audit/2026-04-25/DISPATCH-SHEET.md` (workspace-level).
**Supersedes**: `.audit/2026-04-24/release-certification-v3.md` and the 2026-04-24 morning-handoff.
**Validation basis**: live `gh pr list` + `gh pr view <n> --json statusCheckRollup` + `git log origin/<branch>` for every PR, plus `gh run list` for scheduled workflows. Run 2026-04-25 morning, **revalidated mid-morning 2026-04-25** (see §0).
**Author rule reminder**: this lane does **not** merge, deploy, push to product branches, or rotate secrets. It writes the ledger and the order; the human acts.

---

## 0. Revalidation delta — 2026-04-25 mid-morning

Live state was re-checked against this memo. Deltas relative to the original morning ledger:

1. **`reporium#273` opened at 05:47 UTC and supersedes `#272`.** PR `#273` carries `#272`'s commit verbatim plus an ~80-LOC client-side spend-surface mitigation in `src/components/FAQPanel.tsx` (shared `reporium_ask_timestamps` wallet — same 10/min·100/day cap as AskBar — and a 1 h answer cache keyed by question text). It is `MERGEABLE / CLEAN`, with `lint-and-build`, `security`, `Vercel`, and `Vercel Preview Comments` all `SUCCESS`. PR body explicitly directs: "close #272 in favor of this branch, OR cherry-pick `7ab8e64` onto `claude/feature/faq-page` and merge that." Recommended: **close #272 as superseded, merge #273**.
2. **Spend-surface mitigation is no longer deferred.** The "hold the public `/faq` announcement until the spend-surface mitigation lands" gate from the original ledger is **satisfied by #273** (client wallet + cache shipped in the same PR). The "server-side proxy" item (token-in-bundle full fix) remains tracked as `KAN-LATER-2`; it is not a launch blocker.
3. **Lane jira drafts now exist** for L1, L2, L3, L4, L5, L7, L8, L9, L10. The §8 organizational gap noted in the morning ledger has largely closed during the day. Updated lane status reflected in §8 below.
4. **Workato local branch state**: PR #1 HEAD remains `7604755` on remote (`Perditio-Labs/perditio-workato-integration`). Local `claude/feature/KAN-DRAFT-workato-reporium-validation` carries `81c98c7` + `a5c6468` ahead. Action unchanged: author must push.
5. **No new red CI** since the morning ledger. `#435` still UNSTABLE; all other `reporium-api` PRs still CLEAN. Scheduled workflows on `main` (`Nightly Graph Build` + `data-quality.yml`) still red — same operations causes.
6. **Base-branch policy item for `reporium`** (CLAUDE.md says `dev`, dispatch says `main`) is still unresolved, but #273 also targets `main`, so the operational decision is the same as for #272: pick the policy and merge.

The remainder of this memo has been edited in place to reflect these deltas. The §6 morning-handoff actions are the operative checklist.

### 0.1 Late-morning revalidation — 2026-04-25 ~09:19 UTC (02:19 PDT)

Third pass against live state. Deltas relative to §0:

1. **All open PR states unchanged.** `reporium-api` (#434/#436/#438/#439/#440/#441 CLEAN, #435 UNSTABLE), `reporium` (#272 + #273 both CLEAN), `reporium-ingestion#67` CLEAN, `reporium-audit` #11/#12 CLEAN, `reporium-roadmap` #7/#8/#9 CLEAN. `reporium-api#441` checks: `ask-quality-gate`, `test`×2, `migration-smoke` all SUCCESS as of 2026-04-25 01:07 UTC. `reporium#273` checks: `lint-and-build`, `security`, `Vercel`, `Vercel Preview Comments` all SUCCESS as of 2026-04-25 06:01 UTC.
2. **Nightly Graph Build streak now at 5 reds in 6 nights.** Newest run `2026-04-25T09:14:09Z` → `failure` (same `reporium-db-url` secret-rotation cause). Streak: 04-25 fail, 04-24 fail, 04-23 fail, 04-22 ok, 04-21 ok, 04-20 fail. No code action; the §6 Action 2 ops checklist still applies and is now one day more overdue.
3. **`data-quality.yml` last run `2026-04-24T10:14:20Z` → `failure`.** No new dispatch since; will re-fire on schedule or after #440 merges + manual dispatch in §6 Action 1 step 5.
4. **Workato `#1` HEAD still `7604755`** on `Perditio-Labs/perditio-workato-integration`. Local `81c98c7` + `a5c6468` validation commits still unpushed. Action unchanged: author must push.
5. **No new red CI** on any PR since §0.

The memo body, merge order (§3), do-not-merge list (§4), no-regression checklist (§5), and morning handoff (§6) all remain operative as written.

### 0.2 Pre-dawn revalidation — 2026-04-25 ~09:53 UTC (02:53 PDT)

Fourth pass against live state. Deltas relative to §0.1:

1. **NEW PR `reporium-roadmap#10`** opened today (head `claude/feature/KAN-ROADMAP-reporium-roadmap-sync` → `main`, HEAD `72a779e`). Title: `KAN-ROADMAP: roadmap sync v0.8.0 → v0.8.3 (FAQ lane PR #273 supersedes #272)`. **MERGEABLE / CLEAN**; all `Tests` (`test`×2) SUCCESS at 09:34 UTC. Body explicitly notes that PR #7's release-cert memo references to #272 are **stale** — i.e. **#10 supersedes #7's content surface**. Action: see §6 Action 4 update; close #7 in favor of #10 (or rebase #7 onto v0.8.3 — but the simpler move is to land #10 and close #7).
2. **`reporium#273` is currently `mergeStateStatus=UNSTABLE` — but transient, not red.** Cause: the branch was force-pushed at 09:53 UTC (HEAD `6d595a1`), so `lint-and-build` is `IN_PROGRESS` and the Vercel preview is `PENDING`; `security` already returned SUCCESS on the new HEAD. This is a re-validation race, not a regression. Hold the merge until the rollup re-greens, then proceed per §6 Action 3. **#273's status is "currently re-checking" — neither merge nor close until CI converges.**
3. **`reporium-api#436` was force-pushed at 09:23 UTC** (new HEAD `755fb17`). All five checks (`ask-quality-gate`, `test`×2, `migration-smoke`) returned SUCCESS at 09:27 UTC. Still merge-ready; the §3 critical path order holds.
4. **`data-quality.yml` re-fired and failed again** at `2026-04-25T09:40:51Z` — extends the streak to **5/5 reds on `main`**. Cause unchanged (awaits PR #440 merge). No new action.
5. **Nightly Graph Build streak unchanged** since §0.1 (still `04-25 fail / 04-24 fail / 04-23 fail / 04-22 ok / 04-21 ok / 04-20 fail` — 3-night running streak). §6 Action 2 ops checklist still applies.
6. **Workato `#1` HEAD still `7604755`** — no push since §0.1.
7. **`reporium-ingestion#67` re-validated CLEAN** (new HEAD `c2de352` at 09:23 UTC, `test` SUCCESS at 09:24 UTC).
8. **All other PR states unchanged** since §0.1.

The merge order in §3 is **operative** but with one hold: `reporium#273` waits on CI re-green before §6 Action 3 fires. The do-not-merge list (§4) and no-regression checklist (§5) are unchanged.

---

## 1. Headline

The 2026-04-24 wave landed mostly clean. The single red item that worried us yesterday — `reporium-api#435` (`/health` NullPool) — was correctly **resupplied as `#441`**, which is now the green replacement (`MERGEABLE/CLEAN`, all 5 checks SUCCESS). #435 itself is still red and must be **closed as superseded, not merged**.

The FAQ surface in `reporium` is now also a **superseded → replacement** pair: `#272` is the original, `#273` is the green replacement that bundles the client-side spend-surface mitigation (shared AskBar wallet + 1 h answer cache). Merge #273; close #272.

Two scheduled workflows on `reporium-api` and `reporium-ingestion` `main` remain red. They are *not* code blockers — both are operations work (secret rotation + a PR-#440 dependency).

There are now eleven open PRs across six repositories. Five are queue-ready in `reporium-api`, one is the `#435` close-out, two are a `#272`→`#273` close-out + green merge in `reporium`, **four are doc PRs in `reporium-roadmap` (the new `#10` is today's v0.8.3 sync and supersedes `#7`'s content surface)**, two `reporium-audit` PRs (#11, #12) are open with no CI configured (review-by-reading), and `perditio-workato-integration#1` is still incomplete (a local commit on the L10 author's machine has not been pushed). `reporium-ingestion#67` is the lone non-`reporium-api` `dev`-targeted PR.

---

## 2. Factual ledger (live evidence)

Source: `gh pr view <n> --json mergeable,mergeStateStatus,statusCheckRollup` against each repo, 2026-04-25 morning.

### 2.1 Merge-ready (CI green, mergeStateStatus=CLEAN, no blocker)

| PR | Repo | Title | Base | Head | Files |
|---|---|---|---|---|---|
| **#441** | reporium-api | fix(health): NullPool-safe pool telemetry on /health (#354 follow-up) | main | claude/feature/KAN-354-health-pool-nullpool | app/main.py, tests/test_health.py |
| **#436** | reporium-api | fix(deploy): strip stale traffic tags after promotion | main | fix/deploy-strip-stale-traffic-tags | .github/workflows/deploy.yml |
| **#438** | reporium-api | fix(library): make stats.total_forks / languages corpus-wide (#344) | main | fix/library-stats-corpus-wide-344 | app/routers/library.py, tests/test_library.py, .github/workflows/deploy.yml |
| **#440** | reporium-api | fix(data-quality): pass X-Admin-Key to /metrics/data-quality | main | claude/feature/KAN-XXX-data-quality-verification | .github/workflows/data-quality.yml, scripts/quality_gates.py |
| **#434** | reporium-api | fix(evaluation): surface hn_mentions_count (#369) | main | fix/evaluation-hn-mentions | app/routers/repos.py, tests/test_pros_cons.py |
| **#439** | reporium-api | test(ask): add forbidden_repos primitive to golden-set gate (#367) | main | fix/ask-gate-forbidden-repos-367 | tests/golden_set_ask.yaml, tests/test_ask_golden_numeric.py |
| **#273** | reporium | feat(faq): /faq + client spend-surface mitigation (KAN-272, supersedes #272) | main | claude/feature/KAN-272-faq-spend-surface | src/app/faq/page.tsx, src/components/FAQPanel.tsx, src/components/StickyNavBar.tsx, .audit/2026-04-{24,25}/* |
| **#67** | reporium-ingestion | feat(backfill): no-tag fork tag-recovery via upstream README + topics | dev | claude/feature/KAN-TBD-taxonomy-backfill-completion | (CI: test SUCCESS) |
| **#10** | reporium-roadmap | KAN-ROADMAP: roadmap sync v0.8.0 → v0.8.3 (FAQ lane PR #273 supersedes #272) | main | claude/feature/KAN-ROADMAP-reporium-roadmap-sync | roadmap.json, README.md, REPORIUM_ROADMAP.md, CHANGELOG.md, tests/test_generate.py, .audit/2026-04-25/reporium-roadmap-sync-jira.md |

Of the **nine merge-ready entries**: `mergeable=MERGEABLE` for all; `mergeStateStatus=CLEAN` for eight as of 09:34 UTC. **#273 is currently `UNSTABLE` (transient)** because its branch was force-pushed at 09:53 UTC and `lint-and-build` + Vercel preview are still running on the new HEAD; `security` already returned SUCCESS — see §0.2 ¶2. The `reporium-api` five carry: `ask-quality-gate=SUCCESS`, `test=SUCCESS`, `migration-smoke=SUCCESS`. `reporium-roadmap#10` carries `Tests/test`×2 SUCCESS at 09:34 UTC. `reporium#272` is also CLEAN but is **superseded** — see §2.4; do not merge it.

### 2.2 Needs human review before merge (mergeable but governance/policy gates apply)

| PR | Repo | Why "needs review" |
|---|---|---|
| **#273** | reporium | CLEAN. Two governance items: (a) base-branch policy is unresolved (`reporium/CLAUDE.md` says `dev`, dispatch+remote say `main`; PR is targeted at `main`); (b) the long-term server-side proxy fix is tracked as `KAN-LATER-2`, not in scope here. The client-side mitigation (shared 10/min·100/day wallet + 1 h answer cache) is in this PR, so the public `/faq` announcement is *no longer gated* by mitigation. Decision needed: pick the base branch and merge. |
| **#7** | reporium-roadmap | `docs(release-cert): 2026-04-24 post-wave certification snapshot`. **Now further superseded by #10** (today's v0.8.3 roadmap sync explicitly flags #7's #272 references as stale). Recommended action: close #7 in favor of #10 (the v0.8.3 sync is the active roadmap-status surface; #7's release-cert memo is overtaken by *this* memo, the v4 cert). |
| **#8** | reporium-roadmap | `KAN-ROADMAP: Ask/FAQ roadmap decision package`. Bundles L5 (#272) + L11 (Ask UX safety) outcomes. Reviewable as-is. |
| **#9** | reporium-roadmap | `KAN-DRAFT: production safety checklist`. Reviewable as-is; mirrors `production-safety-checklist.md`. |
| **#11** | reporium-audit | `docs: audit weekly operator pack`. **No CI configured on repo** — review by reading. |
| **#12** | reporium-audit | `feat(audit): harden coverage against live failure modes` (Lane 9). **No CI** — review against L4 nightly-graph-build RCA + L11 §7. |
| **#1** | perditio-workato-integration | `KAN-DRAFT: activate Workato recipe 07`. **Incomplete** — local commit `81c98c7` ("validate recipes 03 + 07") on the L10 author's machine is not pushed; PR HEAD is still `7604755`. Ask author to push before reviewing as full L10 deliverable. |

### 2.3 Blocked / red

| PR | Repo | Block |
|---|---|---|
| **#435** | reporium-api | **Do not merge.** `mergeStateStatus=UNSTABLE`; `test=FAILURE` (twice). The branch HEAD `e9b6493` does not contain the NullPool fix. The fix lives on the sibling branch `claude/feature/KAN-354-health-pool-nullpool@3b52231`, which is now PR #441. Action: close #435 as superseded by #441 (no merge). |

### 2.4 Superseded

| PR | Repo | Superseded by | Reason |
|---|---|---|---|
| **#435** | reporium-api | **#441** | #441's diff is a strict superset of #435 (adds NullPool guard); #441 is CLEAN, #435 is UNSTABLE. Memory observations 4431/4438 confirm fix integration into #441's branch. |
| **#272** | reporium | **#273** | #273's diff is #272 verbatim plus an ~80-LOC client-side spend-surface mitigation (`FAQPanel.tsx` shared wallet + 1 h cache) and audit docs. Both are CLEAN, but #273 is the merge candidate per its own PR body. Close #272; merge #273. |
| **#7** | reporium-roadmap | **#10** | #7 was already flagged as v1 stale-vs-v3; the new v0.8.3 sync in #10 explicitly enumerates #7's #272 references as stale. The active release-cert surface is *this memo* (v4); #7's earlier memo no longer reflects merge-ready state. Close #7, land #10. |
| 2026-04-24 dispatch sheets v1–v4 | workspace | `.audit/2026-04-25/DISPATCH-SHEET.md` | Carry-forward complete; new dispatch is authoritative. |
| 2026-04-24 release-certification-v3.md | workspace | this memo (v4 cert) | Delta: #435 path resolved via #441 (Option B from yesterday's handoff); #272 path resolved via #273; #7 path resolved via #10. |

### 2.5 Scheduled workflows on `main` (not PRs, but on the cert surface)

| Workflow | Repo | Last 5 runs | Status |
|---|---|---|---|
| Nightly Graph Build | reporium-ingestion | 04-25 fail, 04-24 fail, 04-23 fail, 04-22 ok, 04-21 ok (+ 04-20 fail) | **Red 5/6 — current 3-night running streak — awaits GCP secret rotation** (`reporium-db-url:latest`). RCA at `reporium-ingestion/.audit/2026-04-24/nightly-graph-build-root-cause.md`. No code fix; ops action. |
| data-quality.yml | reporium-api | 04-25 fail, 04-24 fail, 04-23 fail, 04-22 fail, 04-21 fail | **Red 5/5 on `main`** — newest fail at 09:40 UTC. **Awaits PR #440 merge** (data-quality plumbing fix). After #440 merges, dispatch and re-validate. |

Both red workflow streaks are *known* and tracked. Neither is a code blocker; both are operations follow-ups.

---

## 3. Ordered merge queue (with dependency reasoning)

**Convention**: each step waits for green CI on its merge before the next starts. After every merge, `git fetch origin && git pull origin main` on the next branch.

### Critical path — `reporium-api` (single-repo serialization)

```
Step 1 — close #435 as superseded by #441           (Lane 14 close-out; no merge)
Step 2 — merge #441 to main                          (NullPool /health fix)
         then verify /health pool block on prod under real pool
Step 3 — merge #436 to main                          (deploy: strip stale candidate-* traffic tags)
Step 4 — rebase #438 on updated main, re-verify CI,
         merge #438 to main                          (library.stats corpus-wide)
         NB: #438's branch already contains #436's commit 5235333 — after #436 squash-merges,
         #438 must be rebased on the new main; otherwise the duplicate workflow change will conflict.
Step 5 — merge #440 to main                          (data-quality X-Admin-Key)
         then `gh workflow run data-quality.yml --ref main -R perditioinc/reporium-api`
         confirm green dispatch (or red on real thresholds, not on plumbing)
Step 6 — merge #434 to main                          (hn_mentions_count on /repos/{id}/evaluation)
Step 7 — merge #439 to main                          (forbidden_repos test primitive — golden-set)
```

**Why this order**:
- #441 first because `/health` saturation alerting and the NullPool guard are the safest single change to ship before the plumbing changes that follow (deploy.yml, data-quality.yml).
- #436 before #438 to satisfy CONFLICT-A in DISPATCH-SHEET §4 (same `.github/workflows/deploy.yml`); #438 is built on top of #436's branch and must be rebased after #436 squash-merges.
- #440 after the deploy + library changes so the data-quality plumbing is exercised on the freshest `main`.
- #434 / #439 last because they are response-shape additions and a test-only addition — lowest blast radius, batched at the tail.

### Off-critical-path

```
Step 8a — close reporium#272 as superseded by #273                   (Lane 5 close-out; no merge)
Step 8b — wait for #273 CI to re-green (post 09:53 UTC force-push),
          then decide #273 base-branch policy and merge              (FAQ + mitigation)
Step 9a — close roadmap#7 as superseded by #10                       (close-out; no merge)
Step 9b — merge roadmap#10 (v0.8.3 sync)                             (CLEAN; Tests SUCCESS)
Step 10 — merge roadmap#8 (Ask/FAQ decision package)                 (review-by-reading)
Step 11 — merge roadmap#9 (production safety checklist)
Step 12 — review-by-reading reporium-audit#11 + #12, merge in order  (no CI)
Step 13 — ask Workato author to push 81c98c7 + a5c6468, then review #1
Step 14 — merge reporium-ingestion#67 to dev at owner discretion     (off-lane, green)
```

### Dependency graph (compact)

- `#441 → #436 → #438` (deploy.yml ordering — must serialize)
- `#440 → data-quality.yml dispatch` (workflow recovery)
- `secret rotation (ops) → Nightly Graph Build recovery` (no PR — ops action)
- `Lane 14 (close #435) ← #441 merged` (close after #441 lands)
- `reporium#272 close ← #273 merged` (close after #273 lands)
- `reporium#273 ← CI re-green after 09:53 UTC force-push` (transient block, then base-branch policy)
- `roadmap#7 close ← roadmap#10 merged` (#10 supersedes #7's content surface)

---

## 4. Do-not-merge list (explicit)

Each item below is supported by live evidence. Do not merge any of these in their current state.

1. **`reporium-api#435`** — `mergeStateStatus=UNSTABLE`; `test` job FAILURE x2. Fix lives on a sibling branch (now PR #441). Action: **close as superseded**, do not push the fix onto #435's branch.
2. **`reporium#272`** — superseded by `#273`. CLEAN, but **must not merge** — its merge would land #272 without the spend-surface mitigation that #273 carries on top. Action: **close as superseded by #273**.
3. **`reporium#273`** — CLEAN, but holds until base-branch policy is resolved between `CLAUDE.md` (`dev`) and dispatch (`main`). Mergeability ≠ merge-readiness.
4. **`reporium-roadmap#7`** — stale v1 cert mirror. Do not merge as-is; either close or refresh to v3 first.
5. **`perditio-workato-integration#1`** — incomplete relative to L10 deliverable; missing pushed commits `81c98c7` + `a5c6468`. Do not merge until author pushes the validation commits (remote is `Perditio-Labs/perditio-workato-integration`, not `perditioinc`).
6. **Anything to `reporium-api/main` after #438 merges without rebasing #440 / #434 / #439** — those branch off pre-#436 main and will conflict on `deploy.yml` if not refreshed in step order.
7. **`reporium-audit#11` and `#12`** — no CI configured; not a hard block, but treat as "merge only after the L4 RCA + L11 §7 cross-reference review is recorded" (per Lane 9 stop conditions).

---

## 5. No-regression checklist

Run after every merge in the queue, and *all of these* after Step 7. If any item fails, halt the queue and escalate to the on-call engineer.

### 5.1 Deploy safety (after #436 lands)

- [ ] `gh run list --workflow="Deploy to Cloud Run" -R perditioinc/reporium-api --limit 1` → SUCCESS on the first post-merge dispatch.
- [ ] `gcloud run services describe reporium-api --region=us-central1 --format=json | jq '.status.traffic'` → no `tag: candidate-*` entries surviving promotion.
- [ ] First post-promotion request: `curl -fsS https://<prod-api>/health | jq '.version'` returns the new build sha.
- [ ] No unexpected revision pinning: `gcloud run revisions list --service=reporium-api --region=us-central1` → newest revision serves 100%.
- [ ] **Hotfix bypass guard** (related to S1315 in memory): confirm no candidate-tagged revision still receives traffic after promotion.

### 5.2 `/health` (after #441 lands)

- [ ] Prod (real pool): `curl -fsS https://<prod-api>/health | jq '.pool'` → object containing `enabled`, sane numeric `size`, `checked_out`, `overflow` (no NullPool path under prod).
- [ ] CI (NullPool): the test that previously failed (`tests/test_health.py::test_pool_stats_nullpool_safe`) passes on `main`.
- [ ] No 500s on `/health` for 30 min after deploy: `gh run list --workflow="post-deploy-smoke"` (or equivalent) → green.
- [ ] Memory observation 4452 (NullPool lacks pool telemetry methods) is *covered* by the helper — confirm by reading `app/main.py:health` post-merge.

### 5.3 Graph freshness (independent of code merges; tracks ops action)

- [ ] After GCP ops rotates `reporium-db-url`, manually dispatch: `gcloud run jobs execute reporium-graph-build --region=us-central1 --project=perditio-platform --wait` → exit 0.
- [ ] Next scheduled run (2026-04-26 10:00 UTC) → SUCCESS in `gh run list --workflow="Nightly Graph Build" -R perditioinc/reporium-ingestion --limit 1`.
- [ ] Graph node count vs baseline: hit `/intelligence/graph/stats` (or equivalent) → ≥ pre-staleness baseline (1,641 nodes per `project_reporium_apr15_demo_gates.md`).
- [ ] Sentinel repos: spot-check 3 fast-moving repos for `last_enriched_at` within 24 h.

### 5.4 Data-quality (after #440 lands)

- [ ] `gh workflow run data-quality.yml --ref main -R perditioinc/reporium-api` → next run SUCCESS *or* a real threshold failure (not a 401/403/missing-header plumbing failure).
- [ ] `scripts/quality_gates.py` no longer emits "401 Unauthorized" against `/metrics/data-quality`.
- [ ] X-Admin-Key path is exercised in the workflow log; secret reference resolves.
- [ ] Confirm migration smoke (`migration-smoke` job) still passes — schema gates unchanged.

### 5.5 Ask correctness (after #439 + #434 land)

- [ ] `tests/test_ask_golden_numeric.py::test_forbidden_repos` passes on `main` (`gh run list --workflow=test`).
- [ ] Golden set `tests/golden_set_ask.yaml` not regressed: spot-check 5 prompts against `/intelligence/ask` and confirm no forbidden-repo leak.
- [ ] `/repos/{id}/evaluation` returns `hn_mentions_count` (integer or `null`) for: a HN-popular repo, a HN-unknown repo, a brand-new repo. (#434 acceptance.)
- [ ] No regression in stars-based ranking introduced by Sprint 1 (#412 already merged).

### 5.6 Public spend surface (after #273 lands)

- [ ] `/faq` page renders every curated Ask suggestion as a card; expanding a card calls `/intelligence/ask` exactly once (cache miss) or zero times (cache hit). No prefetch on page load.
- [ ] DB pool saturation: `pool_size=5+2` ceiling is not exceeded for ≥ 1 h after merge during normal traffic. (`project_neon_quota_migration.md` baseline.)
- [ ] Shared wallet check: with `localStorage.reporium_ask_timestamps` pre-populated to 10 entries in the last minute, expanding a fresh FAQ card shows the friendly per-minute message and **fires zero** `/intelligence/ask` calls. (Confirms `FAQPanel.tsx` `readBudget()` shares state with AskBar.)
- [ ] Cache: reload `/faq`, re-open the same card → no new network call (cache hit on `reporium_faq_answer_cache`, 1 h TTL).
- [ ] Existing AskBar surface (`/ask`) still respects the same wallet — no regression.
- [ ] Vercel preview deploy passes the same checks as prod build (Vercel Preview Comments check on #273 is currently SUCCESS).
- [ ] Server-side proxy fix (`KAN-LATER-2`) is filed and tracked but **not** a launch blocker for `/faq`.

### 5.7 Process hygiene (superseded PRs + placeholder branches)

- [ ] `reporium-api#435` closed with the close comment linking to #441 and citing the supersession evidence (Lane 14 close-out; no force-push to that branch).
- [ ] `reporium#272` closed with the close comment linking to #273 (Lane 5 close-out; no force-push to `claude/feature/faq-page`).
- [ ] No `KAN-DRAFT-*` placeholder branch ever merged into a default branch — replace with real `KAN-<id>` once minted in JIRA. Today the placeholders in flight: `KAN-DRAFT-workato-activation`, `KAN-DRAFT-2026-04-25-release-certification` (this lane), `KAN-DRAFT-production-safety-checklist`, `KAN-DRAFT-release-certification` (older roadmap branch — close once #7 is resolved), `KAN-XXX-data-quality-verification` (PR #440 branch — rename or accept that the merge commit will record the placeholder).
- [ ] `reporium-roadmap#7` is closed or refreshed; stale v1 must not co-exist with v3 on `main`.
- [ ] No memory-driven "it's already merged" claims accepted without `gh pr view` + `git log` evidence (yesterday's lesson — see `project_reporium_p2_resolved_apr24.md` and `morning-handoff-2026-04-25.md` warning).
- [ ] Branch cleanup: after each PR squash-merges, delete the head branch (`gh pr view <n> --json headRefName -q .headRefName | xargs -I{} git push origin --delete {}`).

---

## 6. Morning handoff — exact next actions for the human

The first three actions are the only ones that move the on-call surface. Do those before any satellite review.

### Action 1 — `reporium-api` queue, in order (≈ 30 min CI)

```bash
# 1. close #435 as superseded by #441 (no merge)
gh pr close 435 -R perditioinc/reporium-api \
  --comment "Superseded by #441 (NullPool-safe /health). Branch HEAD e9b6493 does not contain the fix; #441 carries 3b52231 on top of 56c0e1b. mergeStateStatus comparison: #435 UNSTABLE / #441 CLEAN. Closing per release-cert lane 13 (2026-04-25)."
# (do NOT push 3b52231 onto fix/health-pool-stats-354 — that branch belongs to the original author)

# 2. merge #441
gh pr merge 441 -R perditioinc/reporium-api --squash --delete-branch
# wait for deploy workflow to land before continuing

# 3. merge #436
gh pr merge 436 -R perditioinc/reporium-api --squash --delete-branch
# wait for deploy.yml to dispatch and run green

# 4. rebase #438 on the freshly-updated main, then merge
cd reporium-api
git fetch origin
git checkout fix/library-stats-corpus-wide-344
git rebase origin/main
# resolve any deploy.yml drift (the #436 commit is now squashed on main)
git push --force-with-lease origin fix/library-stats-corpus-wide-344
gh pr merge 438 -R perditioinc/reporium-api --squash --delete-branch

# 5. merge #440, then dispatch data-quality.yml manually to confirm plumbing
gh pr merge 440 -R perditioinc/reporium-api --squash --delete-branch
gh workflow run data-quality.yml --ref main -R perditioinc/reporium-api
gh run list --workflow="data-quality.yml" -R perditioinc/reporium-api --limit 1

# 6. merge #434
gh pr merge 434 -R perditioinc/reporium-api --squash --delete-branch

# 7. merge #439
gh pr merge 439 -R perditioinc/reporium-api --squash --delete-branch
```

### Action 2 — Page GCP ops to rotate `reporium-db-url`

The Nightly Graph Build has been failing daily since 2026-04-23. Hand off this exact checklist (RCA in `reporium-ingestion/.audit/2026-04-24/nightly-graph-build-root-cause.md`):

```bash
# verify current secret version
gcloud secrets versions list reporium-db-url --project=perditio-platform

# add new version with the post-2026-04-22 Cloud SQL password
echo -n "<new password>" | gcloud secrets versions add reporium-db-url \
  --data-file=- --project=perditio-platform

# manually run the job to confirm the fix
gcloud run jobs execute reporium-graph-build \
  --region=us-central1 --project=perditio-platform --wait

# confirm next scheduled run goes green
# next: 2026-04-26 10:00 UTC
```

### Action 3 — Close #272, then resolve `reporium` base-branch policy *before* merging #273

```bash
# 1. close #272 as superseded by #273 (no merge)
gh pr close 272 -R perditioinc/reporium \
  --comment "Superseded by #273. #273 carries this PR's commit verbatim plus an ~80-LOC client-side spend-surface mitigation in FAQPanel.tsx (shared AskBar wallet 10/min·100/day + 1h answer cache). Closing per release-cert lane 13 (2026-04-25)."
```

Then pick a base-branch policy and merge #273:

- **Path A** (keep #273 on `main`): update `reporium/CLAUDE.md` to declare `main` as the integration branch. Then `gh pr merge 273 -R perditioinc/reporium --squash --delete-branch`.
- **Path B** (re-target #273 to `dev`): change PR base to `dev`, update DISPATCH-SHEET §1 to record `reporium` integrates on `dev`. Then merge.

Either path is fine. **Do not merge #273 without picking one.** The client-side mitigation is in #273, so the public `/faq` announcement is no longer gated by mitigation work — but the long-term server-side proxy fix is still tracked as `KAN-LATER-2` and should be filed before any major external launch.

### Action 4 — Satellite reviews (afternoon)

In this order, after the `reporium-api` queue is drained:

1. **`reporium-roadmap#7` — close as superseded by `#10`** (the v0.8.3 sync; PR #10's body explicitly enumerates #7's #272 references as stale).
   ```bash
   gh pr close 7 -R perditioinc/reporium-roadmap \
     --comment "Superseded by #10 (v0.8.3 roadmap sync). #10's body enumerates this PR's #272 references as stale per AM revalidation. The active release-cert surface is .audit/2026-04-25/release-certification-memo.md (v4) on the cert branch, not #7's 2026-04-24 memo. Closing per release-cert lane 13 (2026-04-25)."
   ```
2. `reporium-roadmap#10` — green and CLEAN (`Tests/test`×2 SUCCESS at 09:34 UTC). Merge after #7 closes.
3. `reporium-roadmap#8` — review-by-reading. Reviewer should note the #272 → #273 supersession; #8's architectural §1–§5 still hold. Merge.
4. `reporium-roadmap#9` — review-by-reading, merge.
5. `reporium-audit#11` then `#12` — review against L4 RCA + L11 §7. Merge in order.
6. Ask Workato author to push commits `81c98c7` + `a5c6468` from `claude/feature/KAN-DRAFT-workato-reporium-validation` (or fast-forward `claude/feature/KAN-DRAFT-workato-activation`) to `Perditio-Labs/perditio-workato-integration`. Then review `#1`.
7. `reporium-ingestion#67` — green and mergeable to `dev`; merge at owner's discretion.

### Action 5 — Post-wave verification

```bash
# /health on prod (post-#441)
curl -fsS https://<prod-api>/health | jq '.pool'

# data-quality plumbing (post-#440)
gh workflow run data-quality.yml --ref main -R perditioinc/reporium-api
gh run list --workflow="data-quality.yml" -R perditioinc/reporium-api --limit 1

# graph freshness (post-secret-rotation)
gh run list --workflow="Nightly Graph Build" -R perditioinc/reporium-ingestion --limit 1
```

If any verification fails, halt — do not start the next merge. Escalate per `reporium-ingestion/.audit/2026-04-24/graph-build-operator-checklist.md` and the L9 audit playbook.

---

## 7. Things that absolutely must not happen

- **Do not** merge `reporium-api#435`. CI is red; the fix is on a sibling branch (now #441). Memory observations claiming #435 is fixed are wrong — yesterday's lesson burned an entire re-derivation cycle on this. Verify with `git log origin/fix/health-pool-stats-354 -- app/main.py` before trusting any "it's fixed" claim.
- **Do not** merge `reporium#272`. It is superseded by #273; merging #272 would land the FAQ surface without the spend-surface mitigation that #273 now carries.
- **Do not** merge `reporium#273` without resolving the `CLAUDE.md` vs dispatch base-branch inconsistency. That kind of rolling drift bites the next coding lane.
- **Do not** push to another author's PR branch (e.g., `fix/health-pool-stats-354`, `claude/feature/faq-page`). The cherry-pick path was abandoned in both cases; closing the superseded PR is the right move.
- **Do not** merge `reporium-roadmap#7` (v1) when v3 is the active certification — and now superseded again by `#10`'s v0.8.3 sync. Close #7; land #10.
- **Do not** merge `reporium#273` while it shows `mergeStateStatus=UNSTABLE`. The §0.2 ¶2 cause is a transient post-force-push CI race, not a regression — wait for `lint-and-build` + Vercel preview to converge to SUCCESS, then proceed per §6 Action 3.
- **Do not** merge `KAN-DRAFT-*` placeholder branches into default branches without a real KAN id in JIRA, *unless* the team has explicitly accepted the placeholder in the merge commit history (#440's branch is the only one this currently affects in flight).
- **Do not** treat memory as authoritative for PR state. Always: `gh pr view` first, memory second. (Project-rule reinforcement from `project_reporium_p2_resolved_apr24.md`.)

---

## 8. Lane-by-lane status (today's dispatch)

Updated mid-morning 2026-04-25 from filesystem state across repo `.audit/2026-04-25/` directories.

| Lane | Topic | Output (live) | Status |
|---|---|---|---|
| L1 | review #441 | `reporium-api/.audit/2026-04-25/health-pool-nullpool-followup-jira.md` | DELIVERED |
| L2 | review #436 | `reporium-api/.audit/2026-04-25/strip-stale-candidate-tags-jira.md` + `strip-stale-candidate-tags-pr436-review.md` | DELIVERED |
| L3 | review #440 | `reporium-api/.audit/2026-04-25/data-quality-admin-key-jira.md` | DELIVERED |
| L4 | nightly graph RCA | `reporium-ingestion/.audit/2026-04-25/graph-build-root-cause-jira.md` + `graph-build-operator-checklist.md` | DELIVERED (refresh of 2026-04-24 RCA) |
| L5 | #272 decision | `reporium/.audit/2026-04-25/faq-spend-surface-jira.md` + PR #273 itself | DELIVERED — produced replacement PR #273 |
| L6 | review #434 | (none located in `reporium-api/.audit/2026-04-25/`) | NOT FOUND — PR is CLEAN; review-by-reading suffices |
| L7 | review #438 | `reporium-api/.audit/2026-04-25/library-stats-corpus-wide-pr438-review.md` | DELIVERED |
| L8 | review #439 | `reporium-api/.audit/2026-04-25/ask-gate-forbidden-repos-jira.md` | DELIVERED |
| L9 | audit hardening | `reporium-audit/.audit/2026-04-24/reporium-audit-hardening-{jira,report}.md` (carryover) + PR #12 | DELIVERED (carryover) |
| L10 | Workato validation | `perditio-workato-integration/.audit/2026-04-24/workato-reporium-validation*.md` (carryover) | INCOMPLETE — local commits `81c98c7` + `a5c6468` not pushed to remote |
| L11 | Ask UX safety design | `reporium/.audit/2026-04-24/{pr-272-faq-decision,faq-spend-surface-jira}.md` (carryover) | DELIVERED (carryover) |
| L12 | roadmap reality sync | `reporium-roadmap/.audit/2026-04-24/*` carryover **+ NEW PR #10 today** (`reporium-roadmap-sync-jira.md` + branch `claude/feature/KAN-ROADMAP-reporium-roadmap-sync` v0.8.0→v0.8.3 cumulative). Existing #7/#8/#9 still open. | DELIVERED (today's PR #10 supersedes #7 content) |
| L13 | this memo | this file (`release-certification-memo.md` v4) + `release-certification-jira.md` | DELIVERED — refreshed §0.2 (pre-dawn revalidation, 02:53 PDT) |
| L14 | close #435 as superseded | (none located; close-out command in §6 Action 1) | NOT YET EXECUTED — close command in §6 Action 1 |

**Reading**: as of pre-dawn 02:53 PDT, all 12 review/decision lanes have produced reviewable outputs (L12 added today's PR #10). L6 and L14 remain organizational gaps; neither is a certification gap (PR #434 is CLEAN, and the #435 close-out is a single `gh pr close` invocation in §6 Action 1).

---

## 9. Open questions that are not blockers but should land within the week

1. **Real KAN ids** for the active drafts (`KAN-DRAFT-workato-activation`, `KAN-DRAFT-production-safety-checklist`, `KAN-DRAFT-release-certification`, `KAN-DRAFT-2026-04-25-release-certification`, `KAN-XXX-data-quality-verification`, `KAN-ROADMAP-reporium-roadmap-sync`). Mint in JIRA, rename branches before any further work — placeholder KANs in merge history are the kind of debt that compounds.
2. **`reporium-audit` CI**. Repo has no checks configured; reviews are read-only. Enabling at minimum a lint job would catch the kind of drift that L9's hardening targets.
3. **`reporium#272` base-branch policy** — must be resolved (see §6 Action 3) and the loser-branch retired in `CLAUDE.md` to prevent re-occurrence next sprint.
4. **84-commit dev→main** in `reporium-roadmap` (per `project_reporium_blockers_apr9.md` carry-over). Today's four roadmap PRs (#7/#8/#9/#10) compound this; stage a rolling reconciliation PR after the cert wave lands. Closing #7 in favor of #10 is one drop of relief.
5. **DB pool saturation** under sprint-1 traffic — Cloud SQL tier bump or query profiling needed. Out of scope for this lane but cited because it's the implicit ceiling for #272's mitigation.
6. **`generate.py` parity gap** in `reporium-roadmap` (called out in PR #10's body): README hand-written sections (Solved Lanes, Historical Targets, per-repo HEADs, v0.8.x changelog blocks) are not produced by `generate.py:build_readme`. The next nightly auto-build run on `main` will overwrite them after #10 lands. Already scheduled as a follow-up agent (memory observation 4508). Track to closure.

---

*End of memo. Author: lane-13 release-certification (2026-04-25 pre-dawn 02:53 PDT, `claude/feature/KAN-DRAFT-2026-04-25-release-certification` on reporium-roadmap@main). v4 cert.*
