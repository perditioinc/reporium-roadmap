# JIRA fallback: Ask roadmap decision package

JIRA is unavailable from this lane; this file stands in for the ticket per
process rule. A real KAN ticket should replace `KAN-ROADMAP` once JIRA
access is restored.

## Title
Ask/FAQ roadmap decision package — lock Now/Next/Later scope and architectural boundary

## Type / Priority
Chore (coordination) · Medium — locks scope so future lanes stop re-opening the same debate.

## Owner / Lane
Ask roadmap decision package lane (2026-04-24 multi-lane dispatch, wave 2)

## Branch
`claude/feature/KAN-ROADMAP-ask-roadmap-decision-package` → `main`

## Owned files
- `.audit/2026-04-24/ask-roadmap-decision-package.md` (decision package — primary deliverable)
- `.audit/2026-04-24/ask-roadmap-decision-package-jira.md` (this file)

## Out of scope for this lane
- No `roadmap.json` / `REPORIUM_ROADMAP.md` / `README.md` edits. Those belong to the
  sibling `KAN-ROADMAP-reporium-roadmap-sync` lane on its own branch, merged separately.
- No application-repo edits (per process rule 7).
- No merge or deploy (per process rule 8).

## Problem
Three overnight lanes independently addressed pieces of the Ask/FAQ surface:
1. [pr-272-faq-decision.md](../../../reporium/.audit/2026-04-24/pr-272-faq-decision.md)
   — product decision on the `/faq` page (merge PR #272, apply small local mitigation).
2. [ask-retrieval-correctness-jira.md](../../../reporium-api/.audit/2026-04-24/ask-retrieval-correctness-jira.md)
   — runtime retrieval fixes for #365 / #378.
3. [reporium-ask-faq-design-memo.md](../../../reporium/.audit/2026-04-24/reporium-ask-faq-design-memo.md)
   + [claude-design-implementation-jira.md](../../../reporium/.audit/2026-04-24/claude-design-implementation-jira.md)
   — design memo with six UX principles and phased Now/Next/Later.

These outputs are internally consistent but scattered across three repos. Without a
single decision package, the next scheduling round will re-open questions these
lanes already closed: "should we wait for a proxy before merging #272?", "should
the runtime retrieval fix be tied to FAQ?", "should FAQ do grounding badges or
defer to design?". Each re-opening costs a reviewer-day.

## Goal
Produce one artefact future lanes can point at to settle:
- what merges now without further debate
- what requires backend auth/proxy work
- what is product/design-only
- what is retrieval/runtime quality work
- a phased Now/Next/Later plan with effort/risk framing
- explicit non-goals and "do not reopen next week" list

## Acceptance criteria
1. `.audit/2026-04-24/ask-roadmap-decision-package.md` exists and contains:
   - Decision summary (one screen).
   - Decision tree: merge-now / backend-auth / product-design / retrieval-runtime.
   - Phased roadmap (Now / Next / Later) with per-item owning repo, branch, effort, risk.
   - Dependencies list (what blocks what).
   - Non-goals.
   - "What not to reopen next week" explicit list.
2. The package cites the three overnight source docs with repo-relative paths.
3. Each claim traces to one of those docs; novel claims are marked provisional.
4. No application-repo files modified from this lane.

## Definition of done
- PR opened against `main` from the lane branch.
- One commit, one branch, one owned file set (this file + the decision package).
- No edits outside `.audit/2026-04-24/`.

## Stop-conditions check
- ✅ Read-only lane (decision package only).
- ✅ No merge, no deploy, no application-repo edits.
- ✅ No overlap with the sibling `reporium-roadmap-sync` lane: that lane owns
  `roadmap.json` / `REPORIUM_ROADMAP.md` / `README.md`; this lane owns only the
  `.audit/2026-04-24/` memo pair.
- ✅ If one of the three overnight sources is missing at read time, the decision
  package marks the relevant section provisional rather than fabricating content.
