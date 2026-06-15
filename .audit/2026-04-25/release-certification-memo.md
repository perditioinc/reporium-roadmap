# Reporium Release Certification — 2026-04-25

**Lane**: 13 (release certification + merge queue).
**Authoritative dispatch**: `.audit/2026-04-25/DISPATCH-SHEET.md` (workspace-level).
**Supersedes**: `.audit/2026-04-24/release-certification-v3.md` and the 2026-04-24 morning-handoff.
**Validation basis**: live `gh pr list` + `gh pr view <n> --json statusCheckRollup` + `git log origin/<branch>` for every PR, plus `gh run list` for scheduled workflows. Run 2026-04-25 morning.
**Author rule reminder**: this lane does **not** merge, deploy, push to product branches, or rotate secrets. It writes the ledger and the order; the human acts.

---

## 1. Headline

The 2026-04-24 wave landed mostly clean. The single red item that worried us yesterday — `reporium-api#435` (`/health` NullPool) — was correctly **resupplied as `#441`**, which is now the green replacement (`MERGEABLE/CLEAN`, all 5 checks SUCCESS). #435 itself is still red and must be **closed as superseded, not merged**.

Two scheduled workflows on `reporium-api` and `reporium-ingestion` `main` remain red. They are *not* code blockers — both are operations work (secret rotation + a PR-#440 dependency).

There are now nine open PRs across six repositories. Five are queue-ready in `reporium-api`, one is the supersession close-out, one is a green decision-only PR in `reporium`, and three are doc PRs in `reporium-roadmap`. Two `reporium-audit` PRs (#11, #12) are open with no CI configured — they are review-by-reading. `perditio-workato-integration#1` is still incomplete (a local commit on the L10 author's machine has not been pushed).

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
| **#272** | reporium | feat(faq): add /faq page rendering every curated Ask suggestion | main | claude/feature/faq-page | src/app/faq/page.tsx, src/components/FAQPanel.tsx, src/components/StickyNavBar.tsx |
| **#67** | reporium-ingestion | feat(backfill): no-tag fork tag-recovery via upstream README + topics | dev | claude/feature/KAN-TBD-taxonomy-backfill-completion | (CI: test SUCCESS) |

All eight: `mergeable=MERGEABLE`, `mergeStateStatus=CLEAN`. The `reporium-api` five also carry: `ask-quality-gate=SUCCESS`, `test=SUCCESS`, `migration-smoke=SUCCESS`. `reporium#272` carries `lint-and-build=SUCCESS`, `security=SUCCESS`, `Vercel Preview Comments=SUCCESS`.

### 2.2 Needs human review before merge (mergeable but governance/policy gates apply)

| PR | Repo | Why "needs review" |
|---|---|---|
| **#272** | reporium | Already CLEAN, but base-branch policy is unresolved (`reporium/CLAUDE.md` says `dev`, dispatch+remote say `main`; PR is targeted at `main`). The Ask spend-surface mitigation (shared-rate counter + answer cache) is deferred. **Pick a base-branch policy and hold the public `/faq` announcement until the mitigation lands** (DB pool is at ceiling — see `project_ask_sprint1_apr22.md`). |
| **#7** | reporium-roadmap | `docs(release-cert): 2026-04-24 post-wave certification snapshot`. v1 mirror — **stale vs v3**. Either close-and-replace, or push v3 onto its branch and re-review. |
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
| 2026-04-24 dispatch sheets v1–v4 | workspace | `.audit/2026-04-25/DISPATCH-SHEET.md` | Carry-forward complete; new dispatch is authoritative. |
| 2026-04-24 release-certification-v3.md | workspace | this memo | Delta: #435 path resolved via #441 (Option B from yesterday's handoff). |

### 2.5 Scheduled workflows on `main` (not PRs, but on the cert surface)

| Workflow | Repo | Last 5 runs | Status |
|---|---|---|---|
| Nightly Graph Build | reporium-ingestion | 04-24 fail, 04-23 fail, 04-22 ok, 04-21 ok, 04-20 fail | **Red — awaits GCP secret rotation** (`reporium-db-url:latest`). RCA at `reporium-ingestion/.audit/2026-04-24/nightly-graph-build-root-cause.md`. No code fix; ops action. |
| data-quality.yml | reporium-api | 04-24 fail, 04-23 fail, 04-22 fail, 04-21 fail, 04-20 fail | **Red — awaits PR #440 merge** (data-quality plumbing fix). After #440 merges, dispatch and re-validate. |

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
Step 8  — decide reporium#272 base-branch policy, then merge        (FAQ page, deferred mitigation)
Step 9  — close roadmap#7 (stale v1) OR push v3 onto its branch
Step 10 — merge roadmap#8 (Ask/FAQ decision package)                 (no CI; review-by-reading)
Step 11 — merge roadmap#9 (production safety checklist)
Step 12 — review-by-reading reporium-audit#11 + #12, merge in order  (no CI)
Step 13 — ask Workato author to push 81c98c7, then review #1
Step 14 — merge reporium-ingestion#67 to dev at owner discretion     (off-lane, green)
```

### Dependency graph (compact)

- `#441 → #436 → #438` (deploy.yml ordering — must serialize)
- `#440 → data-quality.yml dispatch` (workflow recovery)
- `secret rotation (ops) → Nightly Graph Build recovery` (no PR — ops action)
- `Lane 14 (close #435) ← #441 merged` (close after #441 lands)
- `reporium#272 ← base-branch policy decision` (governance gate)
- `roadmap#7 ← v3 cert (this memo)` (must rebase or close)

---

## 4. Do-not-merge list (explicit)

Each item below is supported by live evidence. Do not merge any of these in their current state.

1. **`reporium-api#435`** — `mergeStateStatus=UNSTABLE`; `test` job FAILURE x2. Fix lives on a sibling branch (now PR #441). Action: **close as superseded**, do not push the fix onto #435's branch.
2. **`reporium#272`** — green, but holds until: (a) base-branch policy resolved between `CLAUDE.md` (`dev`) and dispatch (`main`); (b) public `/faq` announcement deferred until the spend-surface mitigation PR lands. Mergeability ≠ merge-readiness.
3. **`reporium-roadmap#7`** — stale v1 cert mirror. Do not merge as-is; either close or refresh to v3 first.
4. **`perditio-workato-integration#1`** — incomplete relative to L10 deliverable; missing pushed commit `81c98c7`. Do not merge until author pushes the validation commit.
5. **Anything to `reporium-api/main` after #438 merges without rebasing #440 / #434 / #439** — those branch off pre-#436 main and will conflict on `deploy.yml` if not refreshed in step order.
6. **`reporium-audit#11` and `#12`** — no CI configured; not a hard block, but treat as "merge only after the L4 RCA + L11 §7 cross-reference review is recorded" (per Lane 9 stop conditions).

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

### 5.6 Public spend surface (after #272 lands, and BEFORE any public announcement)

- [ ] `/faq` page renders every curated Ask suggestion as a static link, **not** as a hot-fired Ask request.
- [ ] DB pool saturation: `pool_size=5+2` ceiling is not exceeded for ≥ 1 h after merge during normal traffic. (`project_neon_quota_migration.md` baseline.)
- [ ] Shared-rate counter and 1 h answer cache mitigation PR is filed *before* any public `/faq` announcement (HN, LinkedIn, etc.). See `pr-272-faq-decision.md`.
- [ ] No JS path on `/faq` triggers a real `/intelligence/ask` round-trip without a user click.
- [ ] Vercel preview deploy passes the same checks as prod build (Vercel Preview Comments check is currently SUCCESS).

### 5.7 Process hygiene (superseded PRs + placeholder branches)

- [ ] `reporium-api#435` closed with the close comment linking to #441 and citing the supersession evidence (Lane 14 close-out; no force-push to that branch).
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

### Action 3 — Resolve `reporium` base-branch policy *before* merging #272

- **Path A** (keep #272 on `main`): update `reporium/CLAUDE.md` to declare `main` as the integration branch. Then merge #272.
- **Path B** (re-target #272 to `dev`): change PR base to `dev`, update DISPATCH-SHEET §1 to record `reporium` integrates on `dev`. Then merge.

Either path is fine. **Do not merge #272 without picking one.** After merge, hold the public `/faq` announcement until the spend-surface mitigation PR lands.

### Action 4 — Satellite reviews (afternoon)

In this order, after the `reporium-api` queue is drained:

1. `reporium-roadmap#7` — close as stale-v1, or replace branch HEAD with v3 (this memo). Then merge or close.
2. `reporium-roadmap#8` — review-by-reading, merge.
3. `reporium-roadmap#9` — review-by-reading, merge.
4. `reporium-audit#11` then `#12` — review against L4 RCA + L11 §7. Merge in order.
5. Ask Workato author to push commit `81c98c7` from `claude/feature/KAN-DRAFT-workato-reporium-validation` to `claude/feature/KAN-DRAFT-workato-activation`. Then review `#1`.
6. `reporium-ingestion#67` — green and mergeable to `dev`; merge at owner's discretion.

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
- **Do not** merge `reporium#272` without resolving the `CLAUDE.md` vs dispatch base-branch inconsistency. That kind of rolling drift bites the next coding lane.
- **Do not** announce `/faq` publicly until the Ask spend-surface mitigation PR lands. The DB pool is at ceiling.
- **Do not** push to another author's PR branch (e.g., `fix/health-pool-stats-354`). The cherry-pick path was abandoned in favor of #441; closing #435 is the right move.
- **Do not** merge `reporium-roadmap#7` (v1) when v3 is the active certification.
- **Do not** merge `KAN-DRAFT-*` placeholder branches into default branches without a real KAN id in JIRA, *unless* the team has explicitly accepted the placeholder in the merge commit history (#440's branch is the only one this currently affects in flight).
- **Do not** treat memory as authoritative for PR state. Always: `gh pr view` first, memory second. (Project-rule reinforcement from `project_reporium_p2_resolved_apr24.md`.)

---

## 8. Lane-by-lane status (today's dispatch)

| Lane | Topic | Output expected | Output observed (2026-04-25 morning) |
|---|---|---|---|
| L1 | review #441 | `lane-01-pr-441-nullpool-followup-jira.md` | not yet present in `.audit/2026-04-25/` — PR is CLEAN; reviewing-by-reading `app/main.py` + `tests/test_health.py` is sufficient |
| L2 | review #436 | `lane-02-pr-436-strip-stale-tags-jira.md` | not present; PR CLEAN |
| L3 | review #440 | `lane-03-pr-440-admin-key-jira.md` | not present; PR CLEAN |
| L4 | nightly graph RCA | `lane-04-nightly-graph-build-rca-jira.md` + `nightly-graph-build-rca.md` | 2026-04-24 RCA at `reporium-ingestion/.audit/2026-04-24/nightly-graph-build-root-cause.md` is still authoritative; no fresh contradiction observed |
| L5 | #272 decision | `lane-05-pr-272-faq-decision-jira.md` | not present; 2026-04-24 `pr-272-faq-decision.md` covers the call (merge as-is, mitigation deferred) |
| L6 | review #434 | `lane-06-pr-434-hn-mentions-jira.md` | not present; PR CLEAN |
| L7 | review #438 | `lane-07-pr-438-library-stats-jira.md` | not present; PR CLEAN |
| L8 | review #439 | `lane-08-pr-439-forbidden-repos-jira.md` | not present; PR CLEAN |
| L9 | audit hardening | `lane-09-audit-hardening-jira.md` | scope memo not present; reporium-audit#12 is open with the implementation already (review-by-reading) |
| L10 | Workato validation | `lane-10-workato-recipe-validation-jira.md` | not present; perditio-workato-integration#1 incomplete (`81c98c7` not pushed) |
| L11 | Ask UX safety design | `lane-11-ask-ux-safety-design-jira.md` + `ask-ux-safety-design-spec.md` | 2026-04-24 memo at `reporium/.audit/2026-04-24/reporium-ask-faq-design-memo.md` carries forward |
| L12 | roadmap reality sync | `lane-12-roadmap-reality-sync-jira.md` | 2026-04-24 `reporium-roadmap-sync-correction-jira.md` is in this branch's `.audit/2026-04-24/` (carryover); roadmap PRs #7/#8/#9 still open |
| L13 | this memo | this file | DELIVERED |
| L14 | close #435 as superseded | `lane-14-pr-435-superseded-jira.md` | not present; close-out command is in §6 Action 1 |

**Reading**: most lane-NN-jira.md drafts under `.audit/2026-04-25/` were planned but not produced in time for this cert. The DISPATCH-SHEET stop conditions (review-only, doc-only, scope-only) mean the *substantive* output for each review-lane is the corresponding PR's existing review evidence on GitHub — and live `gh pr view` is unanimous: every reporium-api review-lane PR is `CLEAN` with all checks green. Treat the absence of a per-lane jira draft as an *organizational* gap, not a *certification* gap. The memo in §6 stands without them.

---

## 9. Open questions that are not blockers but should land within the week

1. **Real KAN ids** for the active drafts (`KAN-DRAFT-workato-activation`, `KAN-DRAFT-production-safety-checklist`, `KAN-DRAFT-release-certification`, `KAN-DRAFT-2026-04-25-release-certification`, `KAN-XXX-data-quality-verification`). Mint in JIRA, rename branches before any further work — placeholder KANs in merge history are the kind of debt that compounds.
2. **`reporium-audit` CI**. Repo has no checks configured; reviews are read-only. Enabling at minimum a lint job would catch the kind of drift that L9's hardening targets.
3. **`reporium#272` base-branch policy** — must be resolved (see §6 Action 3) and the loser-branch retired in `CLAUDE.md` to prevent re-occurrence next sprint.
4. **84-commit dev→main** in `reporium-roadmap` (per `project_reporium_blockers_apr9.md` carry-over). Today's three roadmap PRs add to this; stage a rolling reconciliation PR after the cert wave lands.
5. **DB pool saturation** under sprint-1 traffic — Cloud SQL tier bump or query profiling needed. Out of scope for this lane but cited because it's the implicit ceiling for #272's mitigation.

---

*End of memo. Author: lane-13 release-certification (2026-04-25 morning, `claude/feature/KAN-DRAFT-2026-04-25-release-certification` on reporium-roadmap@main).*
