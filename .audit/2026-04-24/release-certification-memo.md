# Reporium Release Certification — 2026-04-24

**Lane:** 13 (Release Certification & Merge Queue)
**Author:** Opus 4.7, release-certification lane
**Audience:** human operator running the morning merge / deploy pass
**Companion:** [`release-certification-jira.md`](release-certification-jira.md)
**Source ground truth:** earlier-lane outputs in `.audit/2026-04-24/` across
`reporium-api`, `reporium`, `reporium-ingestion`, `reporium-roadmap`,
`reporium-audit`. No PR was re-reviewed from scratch; verdicts are inherited
from the owning review lane and validated for internal consistency only.

---

## 1. Executive summary (read this first)

- **Six PRs are GO** in the right order: `reporium-api` #436 → #438 → #434 →
  #439 → #435; `reporium` #272.
- **One PR is GO with a known caveat** that the human should acknowledge,
  not fix in this cycle: `reporium-api` #439 (the fixture cannot mechanically
  catch issue #365 — see Lane 7's review).
- **One ops action is the morning's hard P1 and must precede anything else
  graph-related**: rotate `reporium-db-url` Secret Manager value to match the
  2026-04-22 postgres password rotation. Without this, the Nightly Graph
  Build will fail again at 08:30 UTC and Cloud SQL-backed Cloud Run Jobs
  stay broken regardless of what merges.
- **Five branches are NOT to be merged today** — all are design specs,
  hardening drafts, or roadmap docs that require additional human review or
  coordination across repos. Enumerated in §4.
- **No deploys triggered from any lane.** All landed work today is local /
  draft / unmerged. The cycle has not yet hit production.

---

## 2. Factual ledger of in-flight artifacts

PR / branch state was inherited from each lane's audit doc. Spot-checked
against the dispatch sheet at `reporium-api/.audit/2026-04-24/DISPATCH-SHEET-2026-04-24.md`.

### 2.1 Merge-ready (CI green, scope respected, no human action besides merge)

| Repo | PR | Title | Verdict source | Notes |
|---|---|---|---|---|
| reporium-api | [#436](https://github.com/perditioinc/reporium-api/pull/436) | `fix(deploy): strip stale traffic tags after promotion` | [`pr-436-closeout.md`](../../reporium-api/.audit/2026-04-24/pr-436-closeout.md) | Single file, +27/−3, deploy.yml only. CI clean (test×2, ask-quality-gate, migration-smoke). Live state has no stale tags today, so first post-merge deploy will log `No stale traffic tags to remove`. |
| reporium-api | [#438](https://github.com/perditioinc/reporium-api/pull/438) | `fix(library): library.stats corpus-wide (#344)` | [`pr-438-review.md`](../../reporium-api/.audit/2026-04-24/pr-438-review.md) | Library aggregates now mirror `/stats`. **Carries #436's `5235333` deploy.yml commit verbatim** — must merge after #436 and rebase to drop the duplicate. |
| reporium-api | [#434](https://github.com/perditioinc/reporium-api/pull/434) | `fix(evaluation): surface hn_mentions_count (#369)` | [`pr-434-review.md`](../../reporium-api/.audit/2026-04-24/pr-434-review.md) | Additive `hn_mentions_count` int field on `/repos/{id}/evaluation`. CI green on all four required checks. |
| reporium-api | [#440](https://github.com/perditioinc/reporium-api/pull/440) | `fix(data-quality): pass X-Admin-Key to /metrics/data-quality` | [`data-quality-check-verification.md`](../../reporium-api/.audit/2026-04-24/data-quality-check-verification.md) | All 4 required CI checks green. Without this, the next Data Quality Check cron 403s at `metrics_api_reachable`. **Time-sensitive** (see §3.1). |

### 2.2 Merge-ready with caveat (operator should ack, not block)

| Repo | PR | Title | Caveat | Source |
|---|---|---|---|---|
| reporium-api | [#439](https://github.com/perditioinc/reporium-api/pull/439) | `test(ask): forbidden_repos golden primitive (#367)` | Primitive is correct; the **specific first-use entry** (`pinecone alternatives`) cannot mechanically catch #365 because the test mocks the DB layer and `fixture_repos` excludes the forbidden repo. Real #365 coverage requires an integration test or a post-deploy watchdog. Ship the primitive, file follow-up. | [`pr-439-review.md`](../../reporium-api/.audit/2026-04-24/pr-439-review.md) |

### 2.3 Needs human review before merge

| Repo | PR / Branch | Status | What the human owes | Source |
|---|---|---|---|---|
| reporium-api | [#435](https://github.com/perditioinc/reporium-api/pull/435) — `fix/health-pool-stats-354` | Local fix `e9d1a97` committed, **not yet pushed / not yet CI-verified on PR**. Local 5/5 pass. | Push the commit, wait for `Tests` and `Dev Tests` to flip green on the PR, then merge. | [`health-pool-nullpool.md`](../../reporium-api/.audit/2026-04-24/health-pool-nullpool.md) |
| reporium | [#272](https://github.com/perditioinc/reporium/pull/272) — FAQ page | Decision lane authored design memo + rate-counter mitigation; whether the mitigation patch is folded into #272 or kept separate is a UX-lead call. | Confirm the spend-surface mitigation has actually landed on the branch; merge if so, else block on lane folding it in. | [`reporium-ask-faq-design-memo.md`](../../reporium/.audit/2026-04-24/reporium-ask-faq-design-memo.md) |
| reporium-ingestion | branch `ci/graph-build-failure-ergonomics` (commit `025a60b`) | Unmerged follow-up to PR #66's diagnostics improvement. | Open the PR, merge to `main`, then propagate workflow file forward to `dev` (see §6.3 GitFlow note). | [`graph-freshness-e2e.md`](../../reporium-ingestion/.audit/2026-04-24/graph-freshness-e2e.md) §5 |
| reporium-audit | branch `claude/feature/KAN-AUDIT-reporium-audit-hardening` | New checks added (KG wiring, schedule-by-name, Cloud Run tags, README PII scan, SKIP status). 29 tests pass locally. **No PR cut yet.** | Cut the PR, run CI, merge after review. | [`reporium-audit-hardening-report.md`](../../reporium-audit/.audit/2026-04-24/reporium-audit-hardening-report.md) |
| reporium-audit | branch `claude/feature/KAN-AUDIT-audit-operator-digest` | Reporter now adds `## Next Actions` block + `Hint` column. Single-file behaviour change in `reporter.py`. **No PR cut yet.** | Cut the PR after the hardening branch lands; do not stack mid-flight. | [`audit-operator-digest.md`](../../reporium-audit/.audit/2026-04-24/audit-operator-digest.md) |
| reporium-ingestion | branch `claude/feature/KAN-TBD-taxonomy-backfill-completion` | Operator script ready, dry-run-able, requires live Cloud SQL + GH token to actually run. | Do not merge mechanically. Run the dry-run on a sample first, capture results, then merge. | [`taxonomy-backfill-completion-jira.md`](../../reporium-ingestion/.audit/2026-04-24/taxonomy-backfill-completion-jira.md) |
| reporium-roadmap | branch `claude/feature/KAN-ROADMAP-roadmap-backlog-convergence` | README, REPORIUM_ROADMAP, roadmap.json updated to 2026-04-24 reality. Working tree currently dirty (lane 12 in progress). | Wait for lane 12 to finish convergence and land its PR. | [`reporium-roadmap-sync-jira.md`](reporium-roadmap-sync-jira.md), [`roadmap-backlog-convergence-jira.md`](roadmap-backlog-convergence-jira.md) |

### 2.4 Blocked (not by code — by external action or by an upstream merge)

| Item | Blocked by | Action |
|---|---|---|
| Nightly Graph Build (cron 08:30 UTC) | Stale `reporium-db-url:latest` secret post-2026-04-22 password rotation. **Code is fine.** | Ops: add a new secret version with the rotated postgres password. Steps in [`nightly-graph-build-root-cause.md`](../../reporium-ingestion/.audit/2026-04-24/nightly-graph-build-root-cause.md). |
| Data Quality Check (cron 09:00 UTC) | PR #440 not merged. Even after #432 (HTTPS rewrite, merged 03:44 UTC), endpoint returns 403 without `X-Admin-Key`. | Merge PR #440 before 09:00 UTC tomorrow. |
| Reporium-roadmap convergence PR | Lane 12 working tree (uncommitted edits to README.md, roadmap.json) | Lane 12 commit + push. |
| Audit-operator-digest branch | Audit-hardening branch (modifies `reporter.py` already; stacking would conflict). | Land hardening first, then digest. |

### 2.5 Superseded (do not act on; recorded for audit)

| Item | Supersedes / Superseded by |
|---|---|
| Lane 8's would-be code patch on `scripts/quality_gates.py` | Superseded by **PR #440** which already owns those files with green CI. Lane 8 produced verification doc only — correct call. |
| PR #432's HTTPS rewrite as standalone fix | Superseded by combination of #432 + #440. #432 alone leaves the cron failing with 403. Both are needed. |
| Earlier roadmap-sync attempt (commit `3a57373` on lane 12 branch) | Refined by lane 12's convergence pass — see `roadmap-backlog-convergence-jira.md` for the two specific drifts being corrected. |

---

## 3. Ordered merge queue

Strict ordering matters for the `reporium-api` deploy-workflow overlap and
for the time-sensitive Data Quality cron. Items inside the same wave can
merge in any order; waves are sequential.

### Wave A — unblock the Data Quality cron *(do today before 09:00 UTC)*
1. **`reporium-api` #440** — `fix(data-quality): pass X-Admin-Key`.
   Rationale: time-sensitive. Data Quality cron at 09:00 UTC will 403 without
   it. Files don't overlap any other PR. Independent of the deploy-workflow
   chain. Merge first because it's the only deadline-bound item.

### Wave B — `reporium-api` deploy chain *(strict order)*
2. **`reporium-api` #436** — stale traffic tags cleanup.
   Rationale: must precede #438 so the audit-trail commit `5235333` lives
   on the single-purpose PR. If #438 merges first, GitHub auto-closes #436
   and the deploy-history entry will read as the library-stats commit message.
   Per [`pr-436-closeout.md`](../../reporium-api/.audit/2026-04-24/pr-436-closeout.md) §"Overlap with PR #438".
3. **PR author rebases `fix/library-stats-corpus-wide-344` onto updated `main`.**
   Duplicate `5235333` drops out cleanly during rebase.
4. **`reporium-api` #438** — library stats corpus-wide.
   Rationale: corrects total/forks/languages page-scoped bug. Per
   [`pr-438-review.md`](../../reporium-api/.audit/2026-04-24/pr-438-review.md).

### Wave C — additive `reporium-api` features *(any order)*
5. **`reporium-api` #434** — `hn_mentions_count` evaluation field.
6. **`reporium-api` #439** — `forbidden_repos` golden-set primitive (with §2.2 caveat ack).

### Wave D — `reporium-api` `/health` (after CI passes on the PR)
7. **`reporium-api` #435** — NullPool-safe `/health` pool telemetry.
   Pre-req: push commit `e9d1a97` to the PR branch and wait for `Tests` /
   `Dev Tests` to flip green. Local 5/5 already pass per
   [`health-pool-nullpool.md`](../../reporium-api/.audit/2026-04-24/health-pool-nullpool.md).
   Merge after CI confirms.

### Wave E — `reporium` UI *(independent of `reporium-api` chain)*
8. **`reporium` #272** — FAQ page.
   Pre-req: confirm the spend-surface mitigation (rate counter + cache) has
   landed on the branch (per [`reporium-ask-faq-design-memo.md`](../../reporium/.audit/2026-04-24/reporium-ask-faq-design-memo.md) §1
   the sibling lane was meant to fold it into PR #272). If yes, merge to
   `dev`, then promote to `main`.

### Wave F — `reporium-roadmap` *(after lane 12 commits)*
9. **Lane 12 convergence PR** to `reporium-roadmap` `main`. Cuts a fresh
   honest snapshot of the suite's state.

### Waves G+ — durable hardening *(separate days)*
10. `reporium-ingestion` branch `ci/graph-build-failure-ergonomics` →
    `main` (then propagate workflow file forward to `dev`).
11. `reporium-audit` `claude/feature/KAN-AUDIT-reporium-audit-hardening`.
12. `reporium-audit` `claude/feature/KAN-AUDIT-audit-operator-digest`
    (after #11).

---

## 4. Explicit do-not-merge list

Each of these has a real artifact today and may **look** ready. They are not.

| Item | Why not today |
|---|---|
| `reporium` `claude/feature/KAN-272-ask-faq-design` (design lane) | Memo + JIRA draft only. No code. Companion ticket KAN-NEXT-1 is for a future lane. Don't open as a PR. |
| `reporium-ingestion` `claude/feature/KAN-TBD-taxonomy-backfill-completion` | Script written, not yet run on any data. Requires a dry-run on staging snapshot per [`taxonomy-backfill-completion-jira.md`](../../reporium-ingestion/.audit/2026-04-24/taxonomy-backfill-completion-jira.md) §"Acceptance criteria" before it ships. |
| `reporium-audit` audit-operator-digest branch (in isolation) | Stacks on top of audit-hardening behaviour. Do not merge before hardening lands or the diff stacks weirdly on `reporter.py`. |
| Any `nightly_graph_build.yml` patch from this cycle | Per [`graph-freshness-e2e.md`](../../reporium-ingestion/.audit/2026-04-24/graph-freshness-e2e.md) §"Decision: no patch from this lane" — would conflict with the unmerged `025a60b` follow-up. The freshness-assertion patch must bundle with that follow-up, not ship standalone. |
| Direct merge of `reporium-roadmap` lane 12 branch into `main` *before* lane 12 finishes its convergence pass | The roadmap working tree is currently mid-edit (`README.md`, `roadmap.json` modified, this directory has untracked drafts). A premature merge would commit a half-converged state. |
| Any deploy from `reporium-api` `main` *before* PR #436 lands | One stale `candidate-*` tag will be created with no automatic cleanup, regenerating the exact problem #436 was filed to fix. Hold deploys until #436 is in. |
| `reporium-graph-build` Cloud Run Job manual execute *before* `reporium-db-url` secret rotation | Will fail with the same `password authentication failed` error and add noise to logs. |

---

## 5. No-regression checklist

Run after each wave merges, or as a single end-of-day pass once Waves A–E
are in. Each row is a one-shot check; a single line of human read-out is
enough.

### 5.1 Deploy safety (after Wave A → B merges trigger Cloud Run deploys)
- [ ] GitHub Actions: `Deploy to Cloud Run` for `reporium-api` ran the
      new step `Remove stale traffic tags from non-serving revisions`
      between `Promote candidate revision to 100% traffic` and
      `Prune old container images`.
- [ ] Step log shows `No stale traffic tags to remove.` (expected on the
      first post-merge run given current clean state) **or** an explicit
      `Removing stale traffic tags: candidate-<sha>,...` followed by
      success.
- [ ] `gcloud run services describe reporium-api --project=perditio-platform --region=us-central1 --format="value(status.traffic)"`
      returns **exactly one** traffic entry, the freshly-deployed revision,
      `percent=100`. (Lane 2 closeout, post-merge step §"Post-merge verification checklist".)

### 5.2 `/health` (after Wave D merges)
- [ ] `curl https://reporium-api-573778300586.us-central1.run.app/health`
      returns HTTP 200, body has `{"status":"ok","db":"ok","pool":{"size":<int>,"checked_out":<int>,"overflow":<int>}}`.
- [ ] `pool.size`, `pool.checked_out`, `pool.overflow` are **integers** in
      production (NullPool returns `None`s only in CI / local). If any are
      `None` in prod, that's a new degradation worth a follow-up.
- [ ] CI for `Tests` and `Dev Tests` on `main` HEAD post-merge are green.
      The whole point of #435 is that they were red on every `/health`-touching
      test before the fix.

### 5.3 Graph freshness (after secret rotation, no merge needed)
- [ ] `gcloud secrets versions list reporium-db-url` shows a version with
      `CREATE_TIME >= 2026-04-24`.
- [ ] `gcloud run jobs execute reporium-graph-build --project=perditio-platform --region=us-central1 --wait`
      → exit 0; no `psycopg2.OperationalError` in execution logs.
- [ ] After a `workflow_dispatch` of `Nightly Graph Build`, `Verify graph
      endpoint returns fresh data` step prints `total_public_repos ≥ 1500`
      and the typed-edge breakdown is non-empty for `ALTERNATIVE_TO`,
      `COMPATIBLE_WITH`, `DEPENDS_ON`.
- [ ] **Manual freshness probe** (covers the §4 blind spot in
      [`graph-freshness-e2e.md`](../../reporium-ingestion/.audit/2026-04-24/graph-freshness-e2e.md)):
      ```bash
      curl -s "https://reporium-api-wypbzj5gpa-uc.a.run.app/graph/edges?limit=1" \
        | python -c "import json,sys,datetime; d=json.load(sys.stdin); g=datetime.datetime.fromisoformat(d['snapshot_generated_at']); print('age_sec=', (datetime.datetime.now(datetime.timezone.utc)-g).total_seconds())"
      ```
      Expect `age_sec` < 3600.
- [ ] Next 08:30 UTC `Nightly Graph Build` scheduled run completes green
      without manual intervention.

### 5.4 Data quality (after Wave A merges)
- [ ] Manual dispatch on the new `main`:
      `gh workflow run "Data Quality Check" --ref main` followed by
      `gh run view <id> --log` shows green.
- [ ] `Run quality gates` step prints five `[PASS]` rows (`primary_category_coverage`,
      `embeddings_coverage`, `null_is_private`, `readme_summary_coverage`,
      `no_private_repos_in_api`). **No** `metrics_api_reachable: GET …
      failed` line.
- [ ] Next scheduled cron at 09:00 UTC also green. If a *data* gate fails
      (e.g., embeddings coverage regression), file a fresh data-quality
      ticket — that is not a regression in this cycle's work.

### 5.5 Ask correctness (after Waves C and E merge)
- [ ] `pytest tests/test_ask_golden_numeric.py -v` green on `main`. The
      new `forbidden_repos` primitive is no-op against existing 50+ entries,
      so the suite should pass identically to pre-#439.
- [ ] FAQ page on the deployed `reporium` Vercel preview opens, expands a
      card, and renders an answer with a source chip. (Manual; no automated
      gate today.)
- [ ] No 5xx surge on `/intelligence/ask` in the first hour post-deploy
      (Cloud Monitoring or Sentry — pick one).

### 5.6 Public spend surface (after Wave E merges)
- [ ] On the deployed FAQ page, expanding a card a second time within
      ~1 hour serves from cache (no new `/intelligence/ask` request in the
      Network panel). Per the spend-surface mitigation in
      [`reporium-ask-faq-design-memo.md`](../../reporium/.audit/2026-04-24/reporium-ask-faq-design-memo.md) §1.
- [ ] FAQ shares the AskBar `reporium_ask_timestamps` 10/min, 100/day
      counter (no longer bypasses it). Manual check via DevTools `localStorage`.
- [ ] Sanity check on Cloud Run request count for `reporium-api` 1h
      post-deploy is not anomalously high vs. the same hour the day before.
- [ ] **Acknowledged residual:** `NEXT_PUBLIC_APP_API_TOKEN` is still in
      the JS bundle. The architectural fix (server-side proxy / HttpOnly
      cookie) is Phase 3 in the design memo, **not** in this cycle. Don't
      sign off as "spend surface closed" — only as "FAQ no longer widens it
      beyond AskBar's existing exposure."

---

## 6. Morning handoff memo (next actions, in order)

This is the punch list for the human who picks up tomorrow.

### 6.1 Pre-flight (before any merges)
1. Confirm JIRA is back; if so, file actual KAN tickets for every
   `*-jira.md` draft under `.audit/2026-04-24/` across all repos. The ones
   from this lane: `release-certification-jira.md`. The high-priority
   others are listed inline in their respective lanes.
2. Confirm you have GCP credentials in this shell:
   `gcloud config get-value project` should print `perditio-platform`.

### 6.2 Time-sensitive ops (do before 09:00 UTC = 02:00 PDT)
3. **Rotate `reporium-db-url` Secret Manager value** to match the
   2026-04-22 postgres password rotation. Exact command in
   [`nightly-graph-build-root-cause.md`](../../reporium-ingestion/.audit/2026-04-24/nightly-graph-build-root-cause.md) §"Smallest fix":
   ```
   printf 'postgresql://postgres:<NEW_PW>@/postgres?host=/cloudsql/perditio-platform:us-central1:reporium-db' \
     | gcloud secrets versions add reporium-db-url \
         --project=perditio-platform --data-file=-
   ```
   Verify: `gcloud secrets versions list reporium-db-url` shows a
   `CREATE_TIME >= 2026-04-24`.
4. **Validate the secret with a manual job execute** before the cron fires:
   `gcloud run jobs execute reporium-graph-build --project=perditio-platform --region=us-central1 --wait` → exit 0.
5. **Merge `reporium-api` PR #440** so the 09:00 UTC Data Quality cron
   doesn't 403 again.

### 6.3 Wave-by-wave merge pass
6. Wave B: merge `reporium-api` PR #436. Then ping the #438 author to
   rebase `fix/library-stats-corpus-wide-344` onto updated `main`. Then
   merge #438.
7. Wave C: merge `reporium-api` #434 and #439 (in either order).
   When approving #439, paste the caveat from `pr-439-review.md` §"PR
   comment (drafted for posting)" so the test-coverage gap on issue #365
   is on the record.
8. Wave D: push the local commit `e9d1a97` from
   `reporium-api/fix/health-pool-stats-354` to the PR. Wait for `Tests`
   and `Dev Tests` to flip green on PR #435. Then merge.
9. Wave E: confirm the FAQ spend-surface mitigation has been folded into
   `reporium` PR #272 (look for a recent commit on the `claude/feature/faq-page`
   branch from the sibling lane). If yes, merge to `dev`, deploy to
   Vercel preview, sanity-check the FAQ page renders, then promote
   `dev` → `main`.

### 6.4 After the merge pass — run the no-regression checklist
10. Walk §5.1–§5.6 above, top to bottom. Check the boxes.
11. If §5.3 fails (graph freshness), the secret fix in step 3 didn't
    propagate — re-execute the job manually and inspect logs. Do not
    block other waves on this; graph build is independent of the
    `reporium-api` merge chain.

### 6.5 Wave F+ — same-day if energy permits, else tomorrow
12. Wave F (`reporium-roadmap` lane 12 PR): land after lane 12 commits.
    Working tree is currently dirty.
13. Cut PRs for `reporium-audit` `KAN-AUDIT-reporium-audit-hardening`
    and (after) `KAN-AUDIT-audit-operator-digest`.
14. Open the PR for `reporium-ingestion` `ci/graph-build-failure-ergonomics`
    (`025a60b`). After merge, propagate `nightly_graph_build.yml` to `dev`
    so GitFlow stops being weird (per `graph-freshness-e2e.md` §5).
15. **Don't** ship `taxonomy-backfill-completion` script as a merge
    today. Run the documented dry-run on a 10-row sample first; capture
    output; then PR and run.

### 6.6 Things to deliberately defer (and why)
16. The `forbidden_repos` integration test against real pgvector (Lane 7
    follow-up) — do not ship in same cycle as the primitive itself.
    Otherwise the primitive's own merit is conflated with the new test
    fixture's merit if anything goes wrong.
17. Migrating `ingestion/graph/ingest_run_manager.py` from psycopg2+password
    to IAM auth — file as a separate JIRA. Today's secret rotation buys
    months; the migration is the durable fix. Don't bundle.
18. Ask/FAQ Phase 1 visibility components (KAN-NEXT-1 in
    `reporium-ask-faq-design-jira.md`) — design only, no implementation
    today.

---

## 7. Risk assessment for the morning operator

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Secret rotation done wrong (typo in DSN, wrong user) | Low–medium (manual op) | Cron stays red another day | The manual `gcloud run jobs execute` in step 4 catches this in 60 seconds. **Do not skip step 4.** |
| #438 author is unavailable for rebase | Medium | Wave B stalls | Acceptable — Wave B is internal-quality, no production breakage if it slips a day. Don't merge #438 without rebase to preserve audit trail. |
| #435 CI still red post-push (different reason from NullPool) | Low (5/5 local pass) | Wave D stalls | Read the failing test name; if it's not `test_health.py` or `test_rate_limiting.py`, root-cause separately, do not amend the NullPool fix. |
| FAQ spend-surface mitigation not folded into #272 | Medium (depends on sibling lane completing) | Wave E partially blocked | If folding hasn't happened, ship #272's UI **without** declaring §5.6 complete. The spend surface stays where it was; it does not regress. |
| Two simultaneous Cloud Run deploys (race from rapid-fire merges of #436, #438) | Low–medium per [`project_reporium_apr15_demo_gates.md`](../../../Users/PERDITIO/.claude/projects/C--DEV-PERDITIO-PLATFORM/memory/project_reporium_apr15_demo_gates.md) gotcha | One promote step's traffic split is overwritten by the next's | Wait for Wave A's deploy to settle (`gcloud run services describe` shows one traffic entry) before merging Wave B; same between B and C. |

---

## 8. Audit trail / process compliance

- **Lane scope respected.** This lane wrote two files, both inside its
  own `.audit/2026-04-24/` namespace. No product code touched. No PR
  merged. No deploy triggered.
- **Branch.** Per process rule 6 the canonical branch name would be
  `claude/feature/KAN-RELEASECERT-release-certification`. Branch was
  **not** cut because the `reporium-roadmap` working tree is held by
  lane 12 with uncommitted edits. The two deliverable files are
  untracked additions — they do not collide with lane 12's tracked-file
  edits and can be committed by the human onto whichever branch they
  choose. If the choice is to commit to `main`, follow rule 5 + rule 6:
  cut `claude/feature/KAN-RELEASECERT-release-certification` from
  `reporium-roadmap` `main`, add only these two files, push.
- **JIRA.** Unavailable in shell. Offline draft at
  [`release-certification-jira.md`](release-certification-jira.md).
- **Verdicts inherited, not redone.** Each lane's review doc was the
  source of record for its PR's verdict. This lane only validated
  internal consistency, the merge-order overlap (§3 Wave B), and the
  cross-lane dependencies enumerated in §2.4.
- **No destructive recommendations.** Every "merge" recommendation
  preserves the audit trail; nothing here proposes force-push, rebase
  history rewrite on `main`, or skip-hooks behaviour.

---

## 9. Pointers (single index)

- Dispatch sheet: [`DISPATCH-SHEET-2026-04-24.md`](../../reporium-api/.audit/2026-04-24/DISPATCH-SHEET-2026-04-24.md)
- PR #436: [`pr-436-closeout.md`](../../reporium-api/.audit/2026-04-24/pr-436-closeout.md), [`pr-436-review.md`](../../reporium-api/.audit/2026-04-24/pr-436-review.md)
- PR #438: [`pr-438-review.md`](../../reporium-api/.audit/2026-04-24/pr-438-review.md)
- PR #434: [`pr-434-review.md`](../../reporium-api/.audit/2026-04-24/pr-434-review.md)
- PR #439: [`pr-439-review.md`](../../reporium-api/.audit/2026-04-24/pr-439-review.md)
- PR #435 / NullPool: [`health-pool-nullpool.md`](../../reporium-api/.audit/2026-04-24/health-pool-nullpool.md)
- PR #440 / DQ verification: [`data-quality-check-verification.md`](../../reporium-api/.audit/2026-04-24/data-quality-check-verification.md)
- Nightly Graph Build RCA: [`nightly-graph-build-root-cause.md`](../../reporium-ingestion/.audit/2026-04-24/nightly-graph-build-root-cause.md)
- Graph freshness validation: [`graph-freshness-e2e.md`](../../reporium-ingestion/.audit/2026-04-24/graph-freshness-e2e.md)
- Audit hardening: [`reporium-audit-hardening-report.md`](../../reporium-audit/.audit/2026-04-24/reporium-audit-hardening-report.md)
- Audit operator digest: [`audit-operator-digest.md`](../../reporium-audit/.audit/2026-04-24/audit-operator-digest.md)
- Roadmap sync: [`reporium-roadmap-sync-jira.md`](reporium-roadmap-sync-jira.md), [`roadmap-backlog-convergence-jira.md`](roadmap-backlog-convergence-jira.md)
- Ask/FAQ design memo: [`reporium-ask-faq-design-memo.md`](../../reporium/.audit/2026-04-24/reporium-ask-faq-design-memo.md)
- Taxonomy backfill: [`taxonomy-backfill-completion-jira.md`](../../reporium-ingestion/.audit/2026-04-24/taxonomy-backfill-completion-jira.md)
