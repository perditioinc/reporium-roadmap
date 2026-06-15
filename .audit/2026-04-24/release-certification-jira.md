# JIRA fallback: Reporium Release Certification — 2026-04-24

JIRA is unavailable from this lane; this file stands in for the ticket per
process rule 4. A real KAN ticket should replace `KAN-RELEASECERT` when JIRA
access is restored.

## Title
Release certification and merge-queue ordering for the 2026-04-24 multi-lane dispatch

## Type / Priority
Chore · High (gatekeeps ~6 in-flight PRs across reporium-api, reporium, reporium-ingestion, reporium-audit, reporium-roadmap)

## Owner / Lane
Lane 13 — Release Certification (2026-04-24 multi-lane dispatch)

## Branch
`claude/feature/KAN-RELEASECERT-release-certification` → `main`
(Not cut in this lane — no code change, two docs only. If the human commits
these docs, cut the branch from `reporium-roadmap` `main`, not from lane 12's
convergence branch.)

## Owned files (this lane only)
- `.audit/2026-04-24/release-certification-jira.md` (this file)
- `.audit/2026-04-24/release-certification-memo.md`

No product code, no workflow, no deploy config is touched by this lane.

## Problem
Eight lanes produced JIRA drafts and audit artifacts today. Without a
coordination pass, the merge order is ambiguous (PR #436/#438 share a
commit; #440 must land before the next Data Quality Check cron fires;
#435 needs CI-green verification of the NullPool fix), and no single
document tells the morning operator what to do first.

## Acceptance criteria
1. Every open reporium-suite PR touched by the dispatch is classified as
   merge-ready, needs-human-review, blocked, or superseded.
2. Merge order is explicit, with dependency reasoning per PR.
3. A do-not-merge list enumerates the drafts/branches that must **not**
   ship without further human review.
4. A no-regression checklist is given for each of six post-merge
   surfaces: deploy safety, `/health`, graph freshness, data-quality,
   Ask correctness, public spend surface.
5. Morning handoff memo gives the human numbered next actions, in order.
6. No code merged, no deploys triggered, no edits outside owned files.

## Deliverable
See [`release-certification-memo.md`](release-certification-memo.md).

## Out of scope
- JIRA ticket creation (API unavailable).
- Committing the memo to a branch (lane 12 holds the roadmap working tree).
- Any secret-rotation, snapshot rebuild, or Cloud Run action.
- Fixes for anything uncovered during the audit — this lane reports only.
