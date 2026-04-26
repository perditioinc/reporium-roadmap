# Production Safety Checklist — 2026-04-24

**Lane:** Production safety checklist (docs-only; no application code,
no merge, no deploy)
**Consumes:** overnight 12-lane outputs (see workspace-root
`.audit/2026-04-24/release-manager-synthesis.md` and
`.audit/2026-04-24/DISPATCH-SHEET.md` — not mirrored into this repo;
workspace filesystem is canonical for those artifacts)
**Intended reader:** the human who picks up the queue next and has to
decide *in what order* to click merge and *what to watch* afterward.

---

## How to read this document

Every item is one row: **item → why it matters → how to validate → bad
output → remediation**. Items are grouped into three buckets by *when*
the human should check them:

- **§A Pre-merge gates** — must be validated before clicking merge on
  the associated PR. If any fails, **do not merge that PR**.
- **§B Post-merge validation** — validate once the change is on `main`
  and Cloud Run has redeployed (or the next scheduled run has fired),
  before walking away from the merge window.
- **§C Next-scheduled-run monitors** — nothing to do now; watch the
  named cron fire and inspect output. Set a reminder or let the
  Workato recipe do it.

"**Manual follow-up required**" tags any item where available artifact
evidence is insufficient and a live probe (curl, gcloud, `gh`) from an
authorized shell is the only way to confirm safety. Do not mark those
items green from code alone.

---

## §A — Pre-merge gates (must validate before merge)

### A.1 `/health` endpoint is NullPool-safe on the merged head

- **Applies to:** PR
  [#435](https://github.com/perditioinc/reporium-api/pull/435)
  (`fix/health-pool-stats-354`)
- **Why it matters:** the unfixed code crashes `/health` with
  `AttributeError: 'NullPool' object has no attribute 'size'` when
  tests run under the pytest fixture that swaps the engine. A red
  `/health` at deploy time aborts the Cloud Run promote gate and
  effectively blocks every other merge on the queue. It is also the
  one lane whose commit is not yet on origin (`e9d1a97`), so merging
  the PR without a push is a silent no-op.
- **How to validate:**
  1. `gh pr view 435 --json headRefOid,mergeable,statusCheckRollup` —
     confirm `headRefOid` matches the pushed `e9d1a97` and
     `statusCheckRollup.state == SUCCESS`.
  2. If `headRefOid` is still `e9b6493`, the commit was never pushed;
     see remediation below.
  3. Locally in `reporium-api`:
     `git log origin/fix/health-pool-stats-354..fix/health-pool-stats-354`
     — must be empty. If non-empty, author still has unpushed work.
  4. `pytest tests/test_health.py -q` on the PR head — every case
     green including the NullPool path.
- **Bad output:**
  - PR #435 still shows 2 FAILURE checks → head is pre-fix
  - `AttributeError: 'NullPool' object has no attribute 'size'` in
    the failing run's traceback
  - `git log origin/.. ..` non-empty → local work isn't on origin
- **Remediation:** push `e9d1a97` to
  `origin/fix/health-pool-stats-354`, wait for CI to re-run, then
  re-check `gh pr view 435`. **Do not rewrite or amend** that commit.
  **Do not** open a second `/health` branch — a duplicate edit will
  conflict and invalidate the existing review.

### A.2 Deploy workflow cleanup step is merged *before* the lib-stats PR

- **Applies to:** PRs
  [#436](https://github.com/perditioinc/reporium-api/pull/436) and
  [#438](https://github.com/perditioinc/reporium-api/pull/438)
- **Why it matters:** #438 was cut from #436's branch and carries the
  identical `deploy.yml` commit (`5235333`). If #438 lands first,
  GitHub auto-closes #436 as "already merged" and the audit trail for
  the stale-tag fix is captured under the library-stats commit
  message. Reversing the order is *not* a functional break but it
  breaks the deployment-history story the stale-tag lane was built
  to tell.
- **How to validate:**
  1. `gh pr view 436 --json mergeStateStatus` → `CLEAN`
  2. `gh pr view 438 --json mergeStateStatus` → `CLEAN`, and confirm
     #438 is **not yet merged**.
  3. `gh pr diff 438 -- .github/workflows/deploy.yml` — shows the
     identical 27/-3 patch as #436. If it does not, the branch has
     drifted; re-read [pr-436-closeout.md](https://github.com/perditioinc/reporium-api/blob/main/.audit/2026-04-24/pr-436-closeout.md).
  4. Confirm no one has pre-merged #438 while the human was reading
     this doc: `gh pr view 438 --json state` → `OPEN`.
- **Bad output:**
  - #438 state == MERGED while #436 is still OPEN → order was reversed
  - #436 mergeStateStatus != CLEAN → rebase needed (investigate
    before merging)
- **Remediation:** merge order is **#436 → rebase #438 → #438**. If
  #438 landed first by accident, re-open #436 is not possible (it is
  auto-closed). Accept the audit-trail loss and move on; do **not**
  force-revert #438.

### A.3 Candidate-tag exposure is closed on the live service (baseline)

- **Applies to:** PR #436 (same PR as §A.2) plus live Cloud Run state.
- **Why it matters:** The stale-tag cleanup step is *new*, meaning the
  current live service has never been cleaned by it. If stale
  `candidate-<sha>` tags already exist on `reporium-api` at merge
  time, the first post-merge deploy will remove them — **potentially
  multiple** — which is fine but should be anticipated. More
  important: confirm baseline is the documented single-tag state so
  the post-merge step has a known reference point.
- **How to validate:**
  ```bash
  gcloud run services describe reporium-api \
    --project=perditio-platform --region=us-central1 \
    --format="value(status.traffic)"
  ```
  Baseline per [pr-436-closeout.md](https://github.com/perditioinc/reporium-api/blob/main/.audit/2026-04-24/pr-436-closeout.md)
  is exactly **one** entry: 100% on `reporium-api-00252-fop`, tag
  `candidate-58ab8cd`. **Manual follow-up required** — this lane
  cannot run gcloud from the current shell.
- **Bad output:**
  - More than one `status.traffic` entry, *or* any entry with
    `percent: 0` and a `tag` that is **not** the live tag
  - The command errors with an auth failure → operator lacks the
    right credentials and cannot reason about this surface
- **Remediation:** if unexpected stale tags appear, run the manual
  cleanup in `pr-436-closeout.md` §"Manual cleanup required" **before
  merging #436**, so the first post-merge deploy's cleanup step logs
  the expected `No stale traffic tags to remove.` line. If unable,
  document the existing tags in the post-merge §B.1 output so the
  tags being removed are expected, not surprising.

### A.4 Data-quality plumbing is really fixed, not half-fixed

- **Applies to:** PR
  [#440](https://github.com/perditioinc/reporium-api/pull/440)
  (`claude/feature/KAN-XXX-data-quality-verification`)
- **Why it matters:** The scheduled Data Quality Check has been red
  for four consecutive days. PR #432 merged a rewrite that was the
  right *direction* but insufficient: production has
  `METRICS_REQUIRE_AUTH=1` and #432 did not send `X-Admin-Key`. The
  live `/metrics/data-quality` endpoint returns **403**. Merging any
  of the other PRs without landing #440 first means the next red run
  is reported as "still broken from yesterday" when it is in fact
  a second, newer, regression.
- **How to validate:**
  1. `gh pr view 440 --json headRefOid,mergeable,statusCheckRollup`
     — all four required checks must be SUCCESS, mergeable CLEAN.
  2. `gh pr diff 440` — confirm scope is exactly:
     `scripts/quality_gates.py`, `.github/workflows/data-quality.yml`.
     `scripts/check_data_quality.py` must **not** be touched (the
     `/library/full` endpoint is public; adding auth there would
     flip a working probe to a failing one).
  3. `gh secret list --repo perditioinc/reporium-api` — `ADMIN_API_KEY`
     must be present. It was added 2026-04-06 and the workflow
     consumes `${{ secrets.ADMIN_API_KEY }}`. If missing, the fix
     doesn't actually work.
- **Bad output:**
  - `/metrics/data-quality` returns 403 after #440 merges → header
    wasn't plumbed, or secret name mismatched
  - `/library/full` starts returning 403 → scope crept into
    `check_data_quality.py` (revert immediately)
  - `ADMIN_API_KEY` not listed in `gh secret list` → merging #440 will
    fix nothing; the workflow will still auth as unauthenticated
- **Remediation:** if `ADMIN_API_KEY` secret is missing, do **not
  merge #440**. Add the secret first (ops action, outside this lane),
  then merge. If the diff touches `check_data_quality.py`, bounce the
  PR back to the author.

### A.5 Ask/FAQ spend surface is not widened (token exposure unchanged)

- **Applies to:** PR
  [#272](https://github.com/perditioinc/reporium/pull/272)
  (`claude/feature/faq-page`)
- **Why it matters:** FAQ renders up to 16 lazy Ask calls per visit.
  Per [pr-272-faq-decision.md](https://github.com/perditioinc/reporium/blob/main/.audit/2026-04-24/pr-272-faq-decision.md)
  the PR does *not* widen token exposure (reuses
  `NEXT_PUBLIC_APP_API_TOKEN`) and every question pins to a
  deterministic smart-route (SQL, ≈0 LLM tokens). Safety depends on
  all three claims staying true in the final merged diff.
- **How to validate:**
  1. `gh pr diff 272 -- src/app/faq/page.tsx src/components/FAQPanel.tsx src/components/StickyNavBar.tsx`
     — confirm no new env var is introduced; token reference is still
     `NEXT_PUBLIC_APP_API_TOKEN`.
  2. `gh pr diff 272 --name-only` — files added must be limited to
     `src/app/faq/page.tsx`, `src/components/FAQPanel.tsx`, and an
     edit to `src/components/StickyNavBar.tsx`. Any other file,
     especially under `api/` or anything introducing a *new* token,
     is out of scope.
  3. Spot-check `FAQPanel.tsx` for `onToggle`-gated fetch (no fetch on
     mount) and the 16 hardcoded questions — FAQ must be lazy, not
     eager, or a single visit spikes 16 concurrent calls on mount.
  4. Confirm `reporium/CLAUDE.md` GitFlow mismatch is acknowledged:
     CLAUDE.md says `reporium` branches target `dev`; PR #272 targets
     `main`. For a single docs/decision lane this is inert, but the
     human merging should *know* they are accepting a base-branch
     deviation.
- **Bad output:**
  - Any new env var added in the diff → token exposure has grown
  - Fetch is **not** `onToggle`-gated → 16 cold calls land per page
    visit, contending with Ask rate-limit at a shared surface
  - Files outside `src/app/faq/**`, `src/components/FAQPanel.tsx`,
    `src/components/StickyNavBar.tsx` → scope grew
- **Remediation:** reject the PR if spend/scope drifts. If scope is
  clean, merge — and **do not** stack the two-part mitigation (shared
  rate counter + 1h cache) into this same PR; it is already drafted
  as a follow-up in
  [kan-faq-spend-surface-jira.md](https://github.com/perditioinc/reporium/blob/main/.audit/2026-04-24/kan-faq-spend-surface-jira.md).

---

## §B — Post-merge validation (check once merged)

### B.1 First deploy after PR #436 logs the expected cleanup line

- **Applies to:** first `main` push post-#436 that triggers Cloud Run
  deploy.
- **Why it matters:** this is the single observable moment where the
  new stale-tag cleanup step proves it works. Missing this window
  means waiting 24h for the next deploy to show the same.
- **How to validate:**
  1. In the GitHub Actions run for `Deploy to Cloud Run`, confirm the
     step `Remove stale traffic tags from non-serving revisions`
     appears between `Promote candidate revision to 100% traffic` and
     `Prune old container images (keep latest 5)`, and completes
     non-red.
  2. Step log matches either:
     - `No stale traffic tags to remove.` (expected given the clean
       current state — §A.3), or
     - `Removing stale traffic tags: candidate-<oldsha>,...` followed
       by a successful `update-traffic` invocation.
  3. `gcloud run services describe reporium-api ... --format="value(status.traffic)"`
     shows exactly one entry, tag = newly-deployed `candidate-<sha>`,
     percent 100. **Manual follow-up required** (gcloud).
  4. Previous deploy's tagged URL
     `https://candidate-<prev_sha>---reporium-api-wypbzj5gpa-uc.a.run.app/healthz`
     returns **404 / no-route** (confirms tag actually removed).
- **Bad output:**
  - Step is red → `continue-on-error: true` should prevent hard
    failure, but investigate the log; the filter expression may be
    misbehaving
  - More than one `status.traffic` entry post-deploy → cleanup step
    didn't run, or the filter predicate is wrong
  - Previous deploy's candidate URL still 200s → tag not actually
    removed; re-run manual remediation
- **Remediation:** the cleanup step is non-blocking
  (`continue-on-error: true`), so a step failure does not break
  deploy. Paste the step's log into the #436 post-merge thread and
  run the manual cleanup in `pr-436-closeout.md`.

### B.2 `/health` returns green on the live service after PR #435 merges

- **Applies to:** live `reporium-api` service after #435 lands.
- **Why it matters:** NullPool is a test-time surface, not a
  production one, but the deploy gate invokes `/health` as a probe.
  A regression on `/health` code *shape* (even if the prod engine is
  QueuePool, not NullPool) breaks the gate.
- **How to validate:**
  ```bash
  curl -sS https://reporium-api-573778300586.us-central1.run.app/health | jq
  ```
  Expect HTTP 200, JSON body with `pool_stats` populated (numbers)
  under real QueuePool. **Manual follow-up required.**
- **Bad output:**
  - HTTP 500 or missing `pool_stats` key → `/health` handler is
    raising; see Cloud Run logs for the traceback
  - `pool_stats` is an error string or `null` → fallback branch fired
    on prod (it should not; QueuePool has the methods); investigate
- **Remediation:** if `/health` is red on prod, **revert PR #435
  immediately** and reopen on a follow-up branch. The fix is guarded
  by a try/except plus method-existence check per the lane 1 JIRA
  draft; a red prod means the guard caught something real that wasn't
  in the test matrix.

### B.3 Data-quality scheduled workflow dispatches green once #440 merges

- **Applies to:** next scheduled run of `.github/workflows/data-quality.yml`
  *after* PR #440 lands — or a manual `workflow_dispatch` run on
  `main`.
- **Why it matters:** without a confirmed green run on the post-fix
  code, the 4-day red streak stays "unresolved" in operator mental
  state. A single green run closes the loop.
- **How to validate:**
  1. After #440 merges:
     `gh workflow run data-quality.yml --repo perditioinc/reporium-api --ref main`
  2. `gh run list --workflow=data-quality.yml --repo perditioinc/reporium-api -L 1`
     — top run completes SUCCESS.
  3. Step `Run quality gates` log contains `metrics_api_reachable:
     ok` (or equivalent) rather than a 403 traceback.
- **Bad output:**
  - Step still fails with 403 → `X-Admin-Key` not sent or wrong
    secret name; re-check §A.4
  - Step fails with a *different* error (psycopg2 socket, timeout,
    etc.) → new regression behind the auth layer; file a fresh ticket
    rather than re-opening the data-quality lane
- **Remediation:** do not silence the cron if it keeps failing
  post-#440 — the new failure is meaningful signal and needs its own
  ticket.

### B.4 Ask rate-limit counter still binds after #272 ships

- **Applies to:** live Ask surface once `/faq` is deployed on Vercel.
- **Why it matters:** pr-272-faq-decision.md §"Spend-surface" notes
  the FAQ reuses the same 10/min / 100/day counter as AskBar. If the
  counter is keyed per-component rather than per-client, FAQ gets its
  own budget and the headline guarantee breaks.
- **How to validate:** Manual follow-up required — this lane cannot
  probe the live client. Acceptance probe:
  1. Open `/faq`, expand enough cards rapidly to trip the rate limit
     (11 in a minute).
  2. Open AskBar on another page; ask one question.
  3. The AskBar call should be rate-limited *already* (shared
     counter), not granted a fresh quota.
- **Bad output:** AskBar grants a fresh call after FAQ burned through
  the minute budget → counter is per-surface, not per-client → spend
  cap is illusory.
- **Remediation:** stand up the two-part mitigation from
  [kan-faq-spend-surface-jira.md](https://github.com/perditioinc/reporium/blob/main/.audit/2026-04-24/kan-faq-spend-surface-jira.md)
  (shared counter + 1h cache) as a **separate** PR. Do not hot-patch
  it into #272's post-merge cleanup.

---

## §C — Next-scheduled-run monitors (nothing to do now; watch the cron)

### C.1 Nightly Graph Build — secret rotation pending

- **Status:** **manual follow-up required.** This is an ops action,
  not a Claude lane. Nightly Graph Build has been red since
  2026-04-23 10:00 UTC; root cause is stale `reporium-db-url:latest`
  secret after the 2026-04-22 password rotation. See
  [nightly-graph-build-root-cause.md](https://github.com/perditioinc/reporium-ingestion/blob/dev/.audit/2026-04-24/nightly-graph-build-root-cause.md).
- **Why it matters:** every nightly run stays red until a new secret
  version is added. The graph does not refresh downstream; staleness
  accumulates by 24h each missed run.
- **How to validate (after ops adds the new secret version):**
  1. `gcloud secrets versions list reporium-db-url --project=perditio-platform`
     — confirm a new version dated ≥ 2026-04-24 exists.
  2. `gcloud run jobs execute reporium-graph-build --project=perditio-platform --region=us-central1 --wait`
     — ad-hoc execution returns SUCCESS.
  3. Next scheduled run on `.github/workflows/nightly_graph_build.yml`
     completes green on `main`.
  4. `reporium-api`'s graph-node count on `/repos?limit=1`'s trust
     metadata is bumped forward in time (per
     `project_ask_sprint1_apr22.md`, backfill job runs daily).
- **Bad output:**
  - Ad-hoc `jobs execute` still returns `FATAL: password
    authentication failed for user "postgres"` → the new secret
    version has the wrong password
  - Job runs green but `nightly_graph_build.yml` still fails → second
    regression; capture logs from the new ergonomics branch
    (`ci/graph-build-failure-ergonomics`)
- **Remediation:** follow the smallest-fix block in
  `nightly-graph-build-root-cause.md`. If IAM conversion is on the
  roadmap, file a follow-up; do **not** couple it to today's secret
  rotation.

### C.2 Graph freshness downstream (consumers of graph snapshots)

- **Status:** **manual follow-up required.** Downstream Ask quality,
  category coverage, and repo leaderboards all depend on the nightly
  graph refresh. With Nightly Graph Build red (see §C.1), freshness
  is degrading.
- **Why it matters:** a silent regression — Ask queries return stale
  graph distances and leaderboards freeze. No user-visible error.
- **How to validate:**
  1. Hit `/repos?limit=1` and inspect the response's last-built
     timestamp (or equivalent trust metadata field).
  2. Compare against today's date. Gap > 24h on the day of a
     successful schedule = stale.
  3. Cross-check against the latest Cloud Run Job execution timestamp
     from §C.1.
- **Bad output:**
  - Last-built timestamp ≥ 48h behind wall clock → cron has missed
    more than one run
  - Leaderboard endpoints return identical ranks across calendar
    days → graph is frozen
- **Remediation:** unblock §C.1 (secret rotation) and let the next
  scheduled run catch up. If freshness continues to drift, trigger
  `gcloud run jobs execute reporium-graph-build ... --wait` manually.

### C.3 Workato recipe activation assumptions

- **Status:** **manual follow-up required.** Lane 10 (Workato recipe
  validation) is **not started** per
  [release-manager-synthesis.md](release-manager-synthesis.md) §2.
  Recipe `01-graph-regression-guard` and `03-nightly-health-report`
  have explicit upstream dependencies (§C.1 secret rotation for #1;
  #440 merge for #3). Recipes beyond those two have unknown
  activation state because Lane 10 did not start.
- **Why it matters:** if the "nightly health report" recipe is
  *active* and subscribing to the Data Quality Check workflow, it
  will have paged the on-call every day for the last four days. If
  the "graph regression guard" recipe is active, it will have paged
  every night since the password rotation. Neither is a code bug —
  both are expected at this point — but they should not continue
  paging under false-positive conditions.
- **How to validate:**
  1. In `perditio-workato-integration`, read the recipe manifest to
     learn current activation state. (No dispatch output for this
     lane exists to tell us.)
  2. For each recipe, confirm its trigger is gated on a schedule or
     on a specific workflow-run identifier, not on a generic "any
     failure" pattern that fires for any red workflow.
  3. For recipes #1 and #3, confirm they are *paused* until §C.1 and
     PR #440 respectively are resolved, or confirm the on-call is
     prepared for the known-false-positive pages.
- **Bad output:**
  - Any recipe firing into a paging integration with "Nightly Graph
    Build failed" signal *and* active alert policy → human is being
    woken for a known issue
  - Recipe `03-nightly-health-report` active before PR #440 merges →
    same thing for data-quality
  - Workato workflow log shows recipe enabled but payload has no
    correlation with the workflow-run that actually failed → the
    trigger predicate is too broad
- **Remediation:** pause recipes #1 and #3 until the upstream
  dependencies clear. Do **not** patch recipe YAML until Lane 10
  properly starts; pause-then-resume is the intended degraded mode.

### C.4 Data-quality metrics are sane (not just reachable)

- **Status:** **manual follow-up required** after §B.3 closes.
- **Why it matters:** PR #440 fixes the *plumbing* — gates can now
  *read* `/metrics/data-quality`. It does not fix underlying data
  quality. Per the data-quality-check-verification memo, a real
  data-quality regression may be hiding behind the plumbing break
  (categories count, tags count, classified% thresholds from
  `reporium/CLAUDE.md`: `categories >= 10`, `tags >= 50`,
  `classified >= 90%`).
- **How to validate (after PR #440 green run from §B.3):**
  ```bash
  curl -sS -H "X-Admin-Key: $ADMIN_API_KEY" \
    https://reporium-api-573778300586.us-central1.run.app/metrics/data-quality | jq
  ```
  Confirm: `categories >= 10`, `tags >= 50`, `classified >= 90%`.
- **Bad output:**
  - `categories < 10` → enrichment regression; re-read
    `ENRICHMENT_PROMPT_V2.md` thresholds and file a fresh ticket
    *separate from the plumbing fix*
  - `classified < 90%` → bulk-import skipped enrichment (see
    `project_reporium_regression.md`)
  - 4xx on this endpoint after #440 merges → §B.3 wasn't actually
    validated; go back
- **Remediation:** plumbing (PR #440) and data (this check) are
  different tickets. File a new `data:` ticket if thresholds are
  breached; do not re-open #440.

### C.5 MCP surface unchanged (pre-emptive monitor)

- **Status:** **manual follow-up required.** No lane today touched
  `reporium-mcp`; the repo is at baseline with zero open PRs. Listed
  here so it is not forgotten during the post-merge sweep.
- **Why it matters:** `reporium-mcp` consumes `reporium-api`'s public
  endpoints. If any of #434, #435, #438, #439, #440 change a response
  shape, the MCP client breaks silently.
- **How to validate:** spot-check the MCP smoke test (if present in
  `reporium-mcp/tests/`) after each reporium-api merge settles. If
  no smoke test exists, this is itself a manual follow-up — file a
  fresh ticket to add one; do not add it under the current dispatch.
- **Bad output:** MCP client throws on schema mismatch; JSON paths
  like `library.stats.total_repos` return `undefined`.
- **Remediation:** scope a follow-up ticket for the specific endpoint
  contract; do not revert the reporium-api change unless it explicitly
  violated a published contract.

---

## §D — Bucket summary (fast reference)

| Item | Surface | Bucket | Depends on |
|---|---|---|---|
| A.1 `/health` NullPool-safe | PR #435 | Pre-merge | `e9d1a97` pushed |
| A.2 Deploy-YAML merge order | PR #436, #438 | Pre-merge | — |
| A.3 Candidate-tag baseline | Cloud Run live | Pre-merge | gcloud access (**manual**) |
| A.4 Data-quality plumbing | PR #440 | Pre-merge | `ADMIN_API_KEY` secret present |
| A.5 Ask spend-surface | PR #272 | Pre-merge | scope diff clean |
| B.1 Cleanup step live | First deploy | Post-merge | PR #436 merged |
| B.2 `/health` live green | Cloud Run live | Post-merge | PR #435 merged (**manual**) |
| B.3 Data-quality green run | Scheduled workflow | Post-merge | PR #440 merged |
| B.4 Rate-limit binds FAQ + Ask | Live client | Post-merge | PR #272 merged (**manual**) |
| C.1 Nightly Graph Build | Cron + Cloud Run Job | Next run | ops secret rotation (**manual**) |
| C.2 Graph freshness downstream | `/repos` trust meta | Next run | C.1 (**manual**) |
| C.3 Workato recipe activation | Workato | Next run | Lane 10 finishes (**manual**) |
| C.4 Data-quality thresholds sane | /metrics/data-quality | Next run | B.3 (**manual**) |
| C.5 MCP contract unchanged | reporium-mcp | Next run | any reporium-api merge (**manual**) |

Items flagged **manual** require an authenticated shell (gcloud, curl
with admin key, Vercel preview, Workato admin). They cannot be
discharged from the current lane's artifact evidence alone.

---

## §E — Operator failure signatures (quick-match reference)

Paste-match section — if the human sees any of these strings in a log
during/after merge, match to the row above and follow remediation.

| Signature (substring) | Matches item |
|---|---|
| `'NullPool' object has no attribute 'size'` | A.1 |
| `GitHub: PR #436 closed as "already merged"` | A.2 |
| `status.traffic` lists 2+ entries, one with `percent: 0` | A.3 / B.1 |
| `{"detail":"Admin key required for metrics endpoints"}` on `/metrics/data-quality` | A.4 / B.3 |
| `psycopg2.OperationalError: ... password authentication failed for user "postgres"` | C.1 |
| `gcloud.run.jobs.execute ... The execution failed` on `reporium-graph-build` | C.1 |
| `Nightly Graph Build failed` (GH Actions red) | C.1 |
| `metrics_api_reachable: fail` (quality-gates step) | A.4 / B.3 |
| `AskBar: rate limit hit after FAQ` mismatch | B.4 |
| `last_built` timestamp > 24h old on `/repos` trust meta | C.2 |
| Workato page overnight with "Nightly Graph Build failed" payload | C.3 |
| `categories < 10` or `classified < 90` on `/metrics/data-quality` | C.4 |
| `library.stats.total_repos is undefined` in MCP client | C.5 |

---

## §F — Stop-condition audit

| Stop condition | Triggered? | Notes |
|---|---|---|
| Any checklist item relies on live-prod probe this lane cannot run | Yes — flagged **manual follow-up required** in A.3, B.2, B.4, C.1–C.5 | Items are included but explicitly flagged, not assumed green |
| Lane edits application code | No | Docs-only; no source file touched |
| Lane performs merge or deploy | No | All merge/deploy actions framed as human-owned steps |
| Lane asserts live safety from code alone | No | Every code-only signal is paired with a live-probe how-to-validate and marked "manual" if the probe is blocked |
