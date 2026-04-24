# KAN-DRAFT — Production safety checklist (2026-04-24)

**Type:** Ops / release-gate
**Component:** Reporium suite (reporium-api, reporium-ingestion, reporium-mcp, Workato)
**Priority:** P1 (release gate)
**Lane:** Production safety checklist (docs-only; no application code)
**Process note:** JIRA API unavailable in this shell — this draft carries
the ticket surface until KAN access returns. Back-fill then paste the
body verbatim into the new KAN.

---

## Summary

Nine hours into the 2026-04-24 overnight run, twelve lanes have landed
either review memos, fix commits, or dispatch coordination artifacts.
Before any of the six open `reporium-api` PRs, PR #272, or the pending
ops actions (secret rotation, `e9d1a97` push) are merged/executed, the
human on the next shift needs a single, concrete checklist that tells
them:

1. which production surfaces can regress from this batch of changes,
2. how to validate each before merge,
3. what to watch after merge,
4. what to watch on the next scheduled run.

## Deliverable

`.audit/2026-04-24/production-safety-checklist.md` — production-safety
checklist with per-item: what, why it matters, how to validate, failure
signature, remediation. Items are bucketed into:

- **Pre-merge** — must be green before the human clicks merge
- **Post-merge** — validate once merged, before closing the window
- **Next-scheduled-run** — watch the next cron fire; nothing to do now

Scope: `reporium-api`, `reporium-ingestion`, `reporium-mcp`, public API /
Ask / graph / deploy safety, workflow and nightly validation surfaces.

## Acceptance

- Checklist covers all seven scope items listed in the brief
  (candidate-tag exposure, `/health` safety, graph-build status, graph
  freshness downstream, data-quality validation, Ask spend-surface,
  Workato activation)
- Each item has an operator failure signature the human can match
  against logs/output, not just a pass/fail assertion
- Items that cannot be validated from current evidence are explicitly
  flagged "manual follow-up required" rather than assumed green
- No application code is edited by this lane
- No merge, no deploy performed by this lane

## Lane contract

| Field | Value |
|---|---|
| Repo | workspace-root `.audit/2026-04-24/` (lane output); optional copy in `reporium-roadmap` if the roadmap lane requests it |
| Base branch (if committed) | `main` (in `reporium-roadmap` if copied) |
| Branch name | `claude/feature/KAN-<id>-production-safety-checklist` |
| PR target | `main` only if copied to `reporium-roadmap`; otherwise none |
| Owned files | `.audit/2026-04-24/production-safety-checklist.md`, `.audit/2026-04-24/production-safety-checklist-jira.md` |
| Stop conditions | item requires live prod probe beyond artifact evidence → flag "manual follow-up required"; do not assume live safety based on code alone |

## Non-goals

- Does not re-review any PR already reviewed overnight (L1, L2, L4,
  L5, L6, L7, L8)
- Does not decide merge order — see `release-manager-synthesis.md`
- Does not execute any gcloud command, push, or workflow dispatch
- Does not write a runbook — those live per-lane (e.g.
  `runbook-stale-candidate-tag-cleanup.md`)

## Linked artifacts

Workspace-root audit docs (not mirrored into this repo):

- `.audit/2026-04-24/release-manager-synthesis.md`
- `.audit/2026-04-24/DISPATCH-SHEET.md`

Cross-repo artifacts:

- https://github.com/perditioinc/reporium-api/blob/main/.audit/2026-04-24/pr-436-closeout.md
- https://github.com/perditioinc/reporium-api/blob/main/.audit/2026-04-24/data-quality-check-verification.md
- https://github.com/perditioinc/reporium-ingestion/blob/dev/.audit/2026-04-24/nightly-graph-build-root-cause.md
- https://github.com/perditioinc/reporium/blob/main/.audit/2026-04-24/pr-272-faq-decision.md
