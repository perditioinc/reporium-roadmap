# KAN-ROADMAP-STATUS-LANE — overnight roadmap/status alignment lane (2026-04-25)

**JIRA fallback** — no JIRA tool available to this lane. When JIRA returns, copy the body below into a ticket under epic `KAN-ROADMAP` and link the four `reporium-roadmap` PRs (`#10`, `#9`, `#8`, `#7`).

## Lane scope

10-hour overnight (2026-04-25 04:35 PDT → ~14:35 PDT) monitor lane to keep `reporium-roadmap` docs aligned with the live overnight queue **without** reopening solved work or creating duplicate PRs.

This is a **monitor / refresh** lane, not a primary doc-edit lane:

- The canonical roadmap surface (`roadmap.json` / `README.md` / `REPORIUM_ROADMAP.md` / `CHANGELOG.md`) is owned by PR `#10`, last validated at 09:34 UTC and reflects the FAQ supersession (`reporium#273` over `reporium#272`).
- The four open `reporium-roadmap` PRs were independently classified by the merge-gate lane at ~03:10 PDT — see `.audit/2026-04-25/reporium-roadmap-merge-gate-jira.md`. This lane does **not** re-litigate that ledger.

## Live state validated 2026-04-25 04:35 PDT

### `reporium-roadmap` (this repo)

- `origin/main` HEAD: `9b95c1f build(40): nightly update 2026-04-25`.
- 4 open PRs, all CLEAN/MERGEABLE:
  - `#10` — FAQ-sync v0.8.0→v0.8.3 — head `72a779e` — `Tests` SUCCESS at 09:34 UTC.
  - `#9` — production safety checklist (2026-04-24 batch) — head `1f604a7` — green.
  - `#8` — Ask/FAQ decision package — head `f7db506` — green.
  - `#7` — release-cert 2026-04-24 — head `952b1ec` — green.
- 35/35 tests pass on PR #10's branch (`pytest tests/test_generate.py`, 1.69s).
- `roadmap.json` is valid JSON; top-level `version` is `v0.7.0` (public-facing) and changelog top entry is `v0.8.3-roadmap-sync-pr273` 2026-04-25 (per-iteration). Both intentional — not drift.

### Upstream critical-path PRs (state at 04:35 PDT)

| PR | Repo | Head | mergeStateStatus | Notes |
|---|---|---|---|---|
| `#441` | reporium-api | `3b52231` | CLEAN | NullPool-safe `/health`; supersedes `#435`. |
| `#436` | reporium-api | `755fb17` | CLEAN | Force-pushed 09:23 UTC; converged green at 09:27 UTC. |
| `#440` | reporium-api | `eda9625` | CLEAN | Data-quality auth fix; merge unblocks `data-quality.yml` on `main`. |
| `#273` | reporium | `ca0fbbc` | CLEAN | Force-pushed 10:59 UTC; converged green (was UNSTABLE in v4 cert). |
| `#272` | reporium | `63c33e4` | CLEAN | To be **closed as superseded**, not merged. |
| `#435` | reporium-api | `e9b6493` | UNSTABLE | To be **closed as superseded** by `#441`. |

`reporium-api` `main` HEAD: `58ab8cd` (intelligence column-name fix).
`reporium` `main` HEAD: `53e36ae` (library data refresh 2026-04-25).

### Workflows on `main`

- `reporium-ingestion / Nightly Graph Build` — **3-night failure streak** (04-25 / 04-24 / 04-23 fail; 04-22 / 04-21 ok; 04-20 fail). Cause is unchanged: GCP secret rotation (`reporium-db-url`), **outside this repo**. Not a roadmap-doc blocker.
- `reporium-api / data-quality.yml` — newest fail 2026-04-25 09:40 UTC; awaits PR #440 merge + manual re-dispatch.

## Drift assessment vs. PR #10's last push (02:33 PDT, ~2 hours ago)

| Surface | Status |
|---|---|
| `#273` supersedes `#272` framing | Still correct. |
| `#441` (green) replaces `#435` (red NullPool) | Still correct. |
| `fixing_now` references in `roadmap.json` | Still correct (#441/#436/#440/#273 + ingestion #67). |
| Per-repo main HEADs in roadmap evidence | Two have advanced (reporium-api `58ab8cd`, reporium `53e36ae`), but PR #10's roadmap-evidence HEADs were dated 2026-04-22 already — this is a known stale-by-design item flagged in PR #10's body. |
| Graph-edge total (6,209 on 1,406-corpus claim) | Still flagged stale in PR #10's body's `not_working` and "unresolved unknowns". |

**No new drift introduced overnight that affects the canonical roadmap surface.** No tiny patch proposed for PR #10 — patching now would invalidate the 09:34 UTC CI run and add doc churn the brief asks to avoid.

## PR-by-PR disposition (this lane)

| PR | Disposition | Why |
|---|---|---|
| `#10` | **MERGE NOW** (per the merge-gate lane) — keep monitoring during the overnight window. No edits. | Canonical surface aligned with live state at 09:34 UTC; 35/35 tests pass; no drift since. |
| `#9` | **MERGE NOW** — dated 2026-04-24 batch artifact. No edits. | Pure historical record; patching it would rewrite history. |
| `#8` | **MERGE AFTER HUMAN SPOT-CHECK** — architectural §1–§5 hold. No edits. | Decision package architecture survives the #272→#273 supersession; reviewer should sanity-check that no row decision-pivots on the spend-surface delta. |
| `#7` | **MERGE AFTER HUMAN SPOT-CHECK** — dated 2026-04-24 release-cert. No edits. | Central `#441 (green) vs #435 (red NullPool)` finding still correct as of 04-24; #441 was opened 04-25 02:53 PDT and is the natural follow-up to be reflected in the next release-cert lane (NOT here). |

## Out-of-scope items observed (NOT actioned by this lane)

1. **Unpushed local branch `claude/feature/KAN-DRAFT-2026-04-25-release-certification`** has 3 commits (`30501be`, `c30525f`, `90b8f3b`) authored by an earlier session, modifying `.audit/2026-04-25/release-certification-{jira,memo}.md` (release-cert v4). These are the **release-certification lane's** work product, not this lane's; pushing them would either duplicate PR #7 or create an unowned PR. Left in place for the release-cert lane to triage.
2. **Untracked `.audit/2026-04-24/release-certification-{jira,memo}.md`** in workspace — same prior-session origin, same disposition.
3. **Untracked `.audit/2026-04-24/roadmap-backlog-convergence-jira.md`** — prior lane artifact, leave alone.
4. **Untracked `.audit/2026-04-25/reporium-roadmap-merge-gate-jira.md`** — the merge-gate lane's JIRA fallback; comprehensive ledger, written ~03:10 PDT, intentionally not committed by that lane. This file informs this lane's dispositions.
5. **Parity routine `trig_01VeJffvaKRWoFvTcRXaUMun`** (per `MEMORY.md` `project_reporium_apr25_merge_queue`) is the existing scheduled remote agent for the `generate.py` parity gap, scheduled to fire **2026-04-28 09:00 PDT**. **Reused, not duplicated.** This lane does not file a new parity routine.

## Stop conditions honored

- No new branch created by this lane.
- No edits to any of the four PRs' owned files.
- No tiny patches proposed.
- No merge or deploy performed (per overnight rule).
- The existing parity routine is reused, not duplicated.

## Scheduled follow-ups (this lane)

Per the brief, this lane refreshes itself at +2h, +6h, +9h:

- **+2h (~06:35 PDT)** — re-read upstream PRs and `nightly-graph-build`; refresh PR #10 comment if upstream queue advanced.
- **+6h (~10:35 PDT)** — re-validate roadmap docs against any merges that landed; refresh handoff-facing surfaces.
- **+9h (~13:35 PDT)** — final pre-handoff state read; finalize morning note for human reviewer.

If scheduling tooling is unavailable, the schedule is recorded in `.audit/2026-04-25/roadmap-status-scheduled-followups.md`.

## Provenance

- `gh pr list --repo perditioinc/reporium-roadmap --state open` → 4 PRs, all CLEAN.
- `gh pr view <n>` against the four upstream critical-path PRs (`#441`, `#436`, `#440`, `#273`, `#272`, `#435`).
- `gh run list --workflow="Nightly Graph Build"` → 3-night failure streak confirmed.
- `gh api repos/perditioinc/<repo>/branches/main` → main HEADs captured.
- `pytest tests/test_generate.py` → 35 passed in 1.69s.
- `python -c "json.loads(open('roadmap.json').read())"` → valid.

## Refresh log

- **2026-04-25 06:35 PDT (+2h)** — no-op refresh. State line: `roadmap-roadmap@9b95c1f / api@58ab8cd / reporium@53e36ae; #10/9/8/7 head OIDs unchanged; #441/#440/#436/#273 CLEAN unchanged; #435 closed 11:38:47Z + #272 closed 11:39:02Z (both match baseline supersession disposition); Nightly Graph Build latest run 09:14Z 2026-04-25 (no new run since baseline).` Next checkpoint: +6h ~10:35 PDT.
- **2026-04-25 16:43 PDT (+6h, fired late — scheduled for 10:35 PDT, late by ~6h08m)** — **TINY PATCH** v0.8.4-roadmap-status-plus6h-refresh. Drift: PR #272 closed 2026-04-25T11:39:02Z (superseded by #273) and PR #435 closed 2026-04-25T11:38:47Z (superseded by #441). v0.8.2/v0.8.3 documented these as "remains open / still open / slated for close-out"; closures completed at 04:38–04:39 PDT (~2h after C0 baseline) but the literal status word in roadmap.json/README/REPORIUM_ROADMAP went stale. The +2h checkpoint (06:35 PDT) chose no-op because closures matched supersession disposition; at +6h (settled state, late fire) updated only the affected status words to `closed <ISO>` — no architectural shift. Files touched: `roadmap.json` (3 string updates + new v0.8.4 changelog), `README.md` (3 mirror string updates + new v0.8.4 section), `REPORIUM_ROADMAP.md` (rows 1, 4, NullPool gotcha closing line), `CHANGELOG.md` (new top entry). Validation: `python -c "json.loads(open('roadmap.json').read())"` → valid, version v0.7.0, changelog top v0.8.4. `pytest tests/test_generate.py` → 35 passed in 1.57s. No upstream PRs merged in the +6h window. Per-repo main HEADs unchanged from C0 baseline (reporium-api `58ab8cd`, reporium `53e36ae`, reporium-ingestion `4c5f2f3`). Nightly Graph Build streak unchanged (no new run since baseline 09:14Z 2026-04-25). Stop conditions honored: no edits to PR #7/#8/#9 owned files; no merges by this lane; existing parity routine `trig_01VeJffvaKRWoFvTcRXaUMun` reused. Next checkpoint: +9h ~13:35 PDT (likely also fires late given current scheduling drift).
