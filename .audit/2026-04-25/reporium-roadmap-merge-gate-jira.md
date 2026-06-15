# KAN-ROADMAP-MERGE-GATE — reporium-roadmap docs/support PR merge gate (2026-04-25)

**JIRA fallback** — written because no JIRA tool was available to this lane. If/when JIRA returns, copy the body below into a ticket under epic KAN-ROADMAP and link the four PRs.

## Lane scope

Decide whether `reporium-roadmap#10`, `#9`, `#8`, `#7` are still current enough to merge after PR #10's AM revalidation, with special attention to whether the older `2026-04-24`-dated docs are stale once #10's FAQ supersession (PR #273 supersedes PR #272) hits main.

## Live state validated 2026-04-25 ~03:10 PDT

- `origin/main` HEAD: `9b95c1f build(40): nightly update 2026-04-25`
- Open PRs in `perditioinc/reporium-roadmap`: 4 (`#10`, `#9`, `#8`, `#7`). No others.
- All four CLEAN / MERGEABLE. All four have green `Tests` workflow runs (`test` + skipped `notify-on-failure`). #10 was just re-tested at 09:34 UTC today.
- Cross-repo verification: `gh pr view 272/273 --repo perditioinc/reporium` → both still OPEN/MERGEABLE, confirming PR #10's supersession framing is current.

## File ownership map (no conflicts)

| PR | Owned files |
|---|---|
| #10 | `roadmap.json`, `README.md`, `REPORIUM_ROADMAP.md`, `CHANGELOG.md`, `tests/test_generate.py`, `.audit/2026-04-24/reporium-roadmap-sync-{,-correction-}jira.md`, `.audit/2026-04-25/reporium-roadmap-sync-jira.md` |
| #9  | `.audit/2026-04-24/production-safety-checklist{,-jira}.md` |
| #8  | `.audit/2026-04-24/ask-roadmap-decision-package{,-jira}.md` |
| #7  | `.audit/2026-04-24/release-certification{,-jira}.md` |

All four PRs are file-disjoint. Order matters only for narrative coherence, not for rebase mechanics.

## PR ledger

### #10 — `KAN-ROADMAP: roadmap sync v0.8.0 → v0.8.3 (FAQ lane PR #273 supersedes #272)`
- **Branch:** `claude/feature/KAN-ROADMAP-reporium-roadmap-sync` → `main`
- **Size:** +1,039 / −207 across 8 files
- **What it does:** the only PR in this set that patches the canonical roadmap surface (`roadmap.json` / `README.md` / `REPORIUM_ROADMAP.md` / `CHANGELOG.md`). Cumulates four versions on one branch (v0.8.0–v0.8.3). v0.8.3 is today's AM revalidation that re-pointed the FAQ lane onto PR #273 and advanced `as_of` 2026-04-24 → 2026-04-25.
- **CI:** Tests workflow green (re-run today 09:34 UTC). Author confirms `pytest tests/test_generate.py` → 35 passed.
- **Known unresolved unknowns called out in PR body** — none block merge: (a) `generate.py` parity gap (hand-written sections will be overwritten by next nightly auto-build — separate lane already scheduled per `MEMORY.md` reference `4508 / S1342`), (b) stale graph-edge total (already in `not_working`), (c) stale `reporium-db` published count.
- **Decision: MERGE NOW** — freshest snapshot, canonical files, green CI, AM revalidation already done.

### #9 — `KAN-DRAFT: production safety checklist for 2026-04-24 overnight batch`
- **Branch:** `claude/feature/KAN-DRAFT-production-safety-checklist` → `main`
- **Size:** +610 / 0 across 2 files
- **What it does:** dated operator-facing checklist for 2026-04-24 overnight batch — pre-merge / post-merge / next-scheduled-run gates for `#436 candidate-tag`, `#435 /health NullPool`, nightly graph build, data-quality (#440), Ask spend-surface (#272), Workato.
- **Staleness vs. #10:** the Ask spend-surface item references PR #272. PR #273 now supersedes #272, but the checklist is **explicitly stamped as the 2026-04-24 batch record** — it is a historical artifact, not a live runbook. Editing it would rewrite history.
- **Decision: MERGE NOW** — pure docs, dated record, accurate-as-of-its-date. Per stop condition, do not patch around stale specifics in a dated artifact.

### #8 — `KAN-ROADMAP: Ask/FAQ roadmap decision package`
- **Branch:** `claude/feature/KAN-ROADMAP-ask-roadmap-decision-package` → `main`
- **Size:** +376 / 0 across 2 files
- **What it does:** synthesizes three overnight Ask-surface lane outputs into a four-axis decision tree (merge-now / backend-auth / product-design / retrieval-runtime), Now/Next/Later roadmap, dependency graph, 12-row "do-not-reopen" table.
- **Staleness vs. #10:** PR #10's body explicitly notes "Architectural §1–§5 hold; reviewer should note PR #273 supersession when reading." So the architectural framing in #8 survives the #272 → #273 supersession (the FAQ feature itself is unchanged; #273 only adds spend-surface mitigation). Specific PR-number references in #8 are dated 2026-04-24.
- **Decision: MERGE AFTER HUMAN SPOT-CHECK** — content survives, but a reviewer should glance at §1–§5 to confirm none of the architectural rows depend on #272's *lack* of mitigation (the new spend-surface posture is the one decision-meaningful delta between #272 and #273).

### #7 — `docs(release-cert): 2026-04-24 post-wave certification snapshot`
- **Branch:** `claude/feature/KAN-DRAFT-release-certification` → `main`
- **Size:** +333 / 0 across 2 files
- **What it does:** evidence-only certification of the 12-lane dispatch from earlier on 2026-04-24. Calls out 5 PRs safe to merge (`reporium-api` #434/#436/#438/#439/#440) and 1 red (`#435` /health NullPool).
- **Staleness vs. live state:** the central `#435` red finding is correct (NullPool incompatibility). Does **not** mention `#441`, the green replacement that was opened 2026-04-25 ~02:53 (per `MEMORY.md` ref `4513`). PR #10's body confirms: "memo's PR #272 references are now stale per AM revalidation, but its central PR #441 (green) vs PR #435 (red NullPool) finding is still correct" — i.e. the absence of `#441` is a freshness gap, not a correctness gap, and the artifact is dated 2026-04-24.
- **Decision: MERGE AFTER HUMAN SPOT-CHECK** — historical certification, correct on its date. Reviewer should treat it as the 2026-04-24 record, not the live merge-queue. If the reviewer wants the post-#441 picture, that belongs in a fresh release-cert lane, not a patch on this one.

## Recommended merge order

1. **#10 first.** Brings canonical roadmap files (`roadmap.json` / `README.md` / `REPORIUM_ROADMAP.md` / `CHANGELOG.md`) to the live FAQ-supersession state, so any reviewer of #7/#8/#9 reading those files immediately after sees the current narrative.
2. **#9 second.** Pure historical artifact, no review judgment needed beyond the spot-check that the file lives only under `.audit/2026-04-24/`.
3. **#8 third.** Spot-check §1–§5 first; merge if architectural framing holds against the #273 mitigation delta (expected to hold).
4. **#7 fourth.** Spot-check that the reviewer is content treating it as a 2026-04-24 snapshot rather than the live merge-queue.

The order is logical, not mechanical — there are zero file conflicts. If the reviewer is comfortable batching, all four can land in one queue session in this order.

## Tiny patch

**None proposed.** Both `MERGE AFTER HUMAN SPOT-CHECK` PRs (`#7`, `#8`) are dated artifacts. Patching them to add post-2026-04-24 context would (a) violate the dated-record framing, (b) duplicate the reviewer note already in PR #10's body, and (c) generate exactly the kind of docs churn the lane brief asks to avoid.

## Stop conditions honored

- No new branch created by this lane.
- No edits to any of the four PRs' owned files.
- No merge or deploy performed.
- No new docs churn beyond this single JIRA-fallback file.

## Provenance

- `gh pr list --repo perditioinc/reporium-roadmap --state open` (validated 2026-04-25 ~03:10 PDT) — all four CLEAN/MERGEABLE.
- `gh pr view 10/9/8/7 --json files,statusCheckRollup,body` — file lists, CI rollups, and bodies above.
- `gh pr view 272/273 --repo perditioinc/reporium --json state,mergeable` — both OPEN/MERGEABLE, confirming the supersession framing in #10 still applies.
- `MEMORY.md` reference `project_reporium_apr25_merge_queue.md` — independently corroborates the merge-queue claims in #7 and the sync claims in #10.
