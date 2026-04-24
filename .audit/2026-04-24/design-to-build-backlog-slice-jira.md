# JIRA fallback — Design-to-Build backlog slice (Reporium Ask / FAQ)

> JIRA API is not reachable from this lane. This file stands in for the ticket
> per process rule. A real `KAN-<id>` should replace `KAN-DESIGN2BUILD` once
> JIRA access is restored.

## Title

Convert overnight Ask / FAQ design output into a phased engineering backlog slice

## Type / Priority

- Type: Chore (planning / decomposition)
- Priority: Medium — produces the dispatch substrate that subsequent
  implementation lanes will consume; does not itself ship code.

## Owner / Lane

Design-to-build backlog slice lane (2026-04-24 multi-lane dispatch, hour 9).
Read-only with respect to application repos; only docs in `reporium-roadmap`
are written.

## Repo / base / branch / PR target

- Repo: `reporium-roadmap`
- Base: `main`
- Branch: `claude/feature/KAN-DESIGN2BUILD-design-to-build-backlog-slice`
- PR target: `main` (PR not opened by this lane — out of scope)

## Owned files

- `.audit/2026-04-24/design-to-build-backlog-slice.md` (the substantive deliverable)
- `.audit/2026-04-24/design-to-build-backlog-slice-jira.md` (this file)

## Inputs consumed

- `reporium/.audit/2026-04-24/claude-design-implementation-jira.md` — Phase 1
  first-slice ticket (`<AskBudgetIndicator />`). Names but does not enumerate
  remaining Phase 1 slices in detail (they are listed but specifications are
  TBD): `<GroundingBadge />`, `<CacheAgePill />`, `<AskStatusMessage />`,
  FAQ IA refresh, progressive friction at ≥7/10, "Open in Ask" deep-link banner.
- `reporium/.audit/2026-04-24/kan-faq-spend-surface-jira.md` — full diff for
  the FAQPanel spend mitigation (rate counter sharing + 1h answer cache).
- `reporium/.audit/2026-04-24/pr-272-faq-decision.md` — merge verdict for
  PR #272 plus post-merge checklist.
- `reporium/.audit/2026-04-24/frontend-performance-jira.md` — KAN-248,
  `StickyAskBarBoot` lazy-boot pattern. Adjacent surface; relevant because
  it touches the same Ask-bar bundle.

## Inputs **not** found

- `reporium-ask-faq-design-memo.md` — referenced as the parent design memo
  in `claude-design-implementation-jira.md` but does **not** exist on disk
  in any `.audit/2026-04-24/` directory under `reporium`,
  `reporium-roadmap`, or `figma-make-perditio-website-claude`. The backlog
  slice therefore reconstructs Phase 1 / 2 / 3 from the ticket's
  enumeration only and explicitly marks individual slice contents as
  **assumed** wherever the ticket names a component without specifying it.

## Acceptance criteria

1. `.audit/2026-04-24/design-to-build-backlog-slice.md` exists and contains:
   - Phased implementation slices grouped by **owner type** (frontend-only,
     backend/API/auth, product/content, observability/spend control).
   - For each slice: outcome, owner type, risk, dependencies, validation
     method.
   - Suggested JIRA decomposition (one JIRA per shippable slice, with a
     proposed title and short description).
   - Explicit parallel-vs-sequential plan with a dependency graph.
   - A separate "Unresolved design ambiguities" section that flags what the
     missing parent design memo would have answered.
2. No application-repo files are edited from this lane (process rule 7).
3. No merge or deploy from this lane (process rule 8).
4. Branch and file names follow the dispatch-sheet convention.

## Stop conditions honored

- Parent design memo not found → produced a partial backlog slice and
  explicitly marked assumptions, instead of fabricating slice specs.
- No code changes proposed against `reporium`, `reporium-api`, or
  `figma-make-perditio-website-claude`; those repos remain read-only.
- No merge, no deploy, no PR opened from this lane.

## Out of scope

- Implementation of any of the proposed slices.
- Edits to `roadmap.json` / `REPORIUM_ROADMAP.md` (those belong to the
  separate roadmap-sync lane already in flight, see
  `reporium-roadmap-sync-jira.md` on a sibling branch).
- Mutating tickets in JIRA (API unavailable; this file is the placeholder).
