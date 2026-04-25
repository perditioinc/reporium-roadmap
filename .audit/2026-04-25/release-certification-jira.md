# JIRA Draft — Release Certification 2026-04-25 (Lane 13)

> **Status**: draft, not yet filed in JIRA. JIRA Atlassian CLI not available from this lane; per project rule §4 this file is the substitute. Mint a real KAN id and replace `KAN-DRAFT-2026-04-25-release-certification` before pushing or merging the certification branch.

---

**Summary**: Reporium release certification + merge queue for the 2026-04-24 wave (validated 2026-04-25 morning).

**Issue type**: Task

**Project**: KAN

**Reporter**: Claude (release-certification lane 13)

**Assignee**: human merger / on-call engineer (2026-04-25 AM)

**Branch**: `claude/feature/KAN-DRAFT-2026-04-25-release-certification` on `reporium-roadmap`

**Related**:
- `reporium-api#441`, `#440`, `#439`, `#438`, `#436`, `#435`, `#434`
- `reporium#273` (supersedes `#272`)
- `reporium-ingestion#67`
- `reporium-audit#11`, `#12`
- `reporium-roadmap#7`, `#8`, `#9`
- `perditio-workato-integration#1` (org: `Perditio-Labs`, not `perditioinc`)
- Workspace dispatch: `.audit/2026-04-25/DISPATCH-SHEET.md`
- Yesterday's cert: `.audit/2026-04-24/release-certification-v3.md`
- Yesterday's handoff: `.audit/2026-04-24/morning-handoff-2026-04-25.md`
- Memory: `project_reporium_p2_resolved_apr24.md`, `project_reporium_apr16_audit.md`, `project_ask_sprint1_apr22.md`, `project_neon_quota_migration.md`

**Priority**: P1 (gates the wave; not P0 because no on-call surface is currently red — only scheduled workflows are red and they are tracked).

---

## Description

The 2026-04-24 wave produced 7 open `reporium-api` PRs, 2 `reporium` PRs (`#272` + the green replacement `#273`), 1 `reporium-ingestion` PR, 2 `reporium-audit` PRs, 3 `reporium-roadmap` PRs, and 1 `perditio-workato-integration` PR. This certification ledger states which are merge-ready, which need human review, which are blocked, and which are superseded — with explicit merge order, dependency reasoning, and a no-regression checklist.

Two supersessions are live:
- `reporium-api#435` → `#441` (NullPool-safe `/health`). Close #435; merge #441.
- `reporium#272` → `#273` (FAQ + client spend-surface mitigation). Close #272; merge #273.

Two scheduled workflows on `main` remain red (`Nightly Graph Build`, `data-quality.yml`) — tracked, not blockers; one awaits a GCP secret rotation, the other awaits PR #440 merging.

## Acceptance criteria

- [ ] All seven items in §3 of `release-certification-memo.md` (the `reporium-api` queue) are merged in the order specified, with green CI between each.
- [ ] `reporium-api#435` is closed with the supersession comment (no merge).
- [ ] `reporium#272` is closed with the supersession comment (no merge); `#273` is merged after the base-branch policy decision.
- [ ] GCP ops rotates `reporium-db-url` and the next Nightly Graph Build run is green.
- [ ] `data-quality.yml` next dispatch on `main` is green (or red on real thresholds, not on plumbing).
- [ ] No `KAN-DRAFT-*` placeholder branch is merged into a default branch without acknowledgement.
- [ ] No-regression checklist (§5 of the memo) — every checkbox passes after the wave lands.
- [ ] `release-certification-memo.md` and this jira draft are linked from the roadmap PR that lands the certification snapshot.

## Out of scope

- Code edits in any product repo (this lane is read + write-docs only).
- Merging or deploying any PR (the human acts; this lane records the order).
- GCP IAM changes, secret rotations, Cloud Run revision pinning (ops actions).
- Any `KAN-DRAFT-*` → real `KAN-<id>` re-naming (separate JIRA ops task).

## Deliverables (this lane)

- `.audit/2026-04-25/release-certification-memo.md` — the full ledger, merge order, do-not-merge list, no-regression checklist, morning handoff (sections 1–9).
- `.audit/2026-04-25/release-certification-jira.md` — this file.
- Branch: `claude/feature/KAN-DRAFT-2026-04-25-release-certification` on `reporium-roadmap`.
- PR: to be opened against `reporium-roadmap@main` after human review.

## Definition of done

- Memo and jira draft committed to the certification branch.
- PR opened against `reporium-roadmap@main`; CI green (`test`).
- Linked from `reporium-roadmap#7` close-out (or its v3 refresh) so the roadmap reflects the active certification.
- One human merger (the Action 1–5 owner in the morning-handoff) signs off that they read §6 before draining the queue.

---

*End of jira draft.*
