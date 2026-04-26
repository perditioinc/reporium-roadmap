# Ask / FAQ — Roadmap Decision Package

**Date:** 2026-04-24
**Lane:** `claude/feature/KAN-ROADMAP-ask-roadmap-decision-package` → `main`
**Author:** Opus 4.7 (roadmap decision lane, 9h into overnight dispatch)
**Purpose:** Lock scope so next week's dispatch does not re-open the same architectural debate.

## Source documents (three overnight lanes consumed)

| # | Source | Repo | Type |
|---|---|---|---|
| A | [pr-272-faq-decision.md](../../../reporium/.audit/2026-04-24/pr-272-faq-decision.md) + [kan-faq-spend-surface-jira.md](../../../reporium/.audit/2026-04-24/kan-faq-spend-surface-jira.md) | reporium | Product decision on PR #272 |
| B | [ask-retrieval-correctness-jira.md](../../../reporium-api/.audit/2026-04-24/ask-retrieval-correctness-jira.md) | reporium-api | Runtime retrieval fix for #365/#378 |
| C | [reporium-ask-faq-design-memo.md](../../../reporium/.audit/2026-04-24/reporium-ask-faq-design-memo.md) + [claude-design-implementation-jira.md](../../../reporium/.audit/2026-04-24/claude-design-implementation-jira.md) | reporium | UX safety design memo (Phase 1 slice) |

All three are present and mutually consistent on 2026-04-24. No section below
is marked provisional; gaps are filed under §7 Non-goals instead.

---

## 1. Decision summary (one screen)

> **The Ask/FAQ surface is not one problem; it is four, each with a different
> owner, a different repo, and a different cost profile. This package assigns
> each to a phase and freezes the architectural boundary.**

1. **Merge now:** PR #272 (`/faq` page) — additive frontend, no token-surface
   expansion, every curated question maps to a deterministic smart-route. Fold
   in the FAQ-local mitigation commit (shared rate counter + 1h answer cache)
   from source A before merging.
2. **Ship next (backend runtime):** `reporium-api` negated-product filter
   (#365) + `_ROUTE_COMPARISON` regex broadening (#378). Bounded, unit-tested,
   no infra change.
3. **Ship next (frontend design — Phase 1 slice 1):** `<AskBudgetIndicator />`
   component from source C. Reads existing localStorage key; no API change.
4. **Defer to later:** Phase 2 (server `Retry-After` + cost header) and
   Phase 3 (server-side proxy with HttpOnly session cookie). These are the only
   real spend-containment answer, but they are `reporium-api` + infra work and
   are out of scope for every frontend lane until separately scheduled.

The four problems and their owners:

| Problem | Owner repo | Phase | Effort | Risk |
|---|---|---|---|---|
| `/faq` surface exists and respects the shared Ask budget | `reporium` | Now | S (1 PR, folded into #272) | Low |
| "alternatives to X" returns X; "X vs Y" misses one side | `reporium-api` | Next | S (pure-function filter + regex) | Low |
| Budget is invisible; grounding is under-dramatized | `reporium` | Next | M (6 components over ≥2 PRs) | Low |
| Public `NEXT_PUBLIC_APP_API_TOKEN` enables unbounded spend | `reporium-api` + `reporium` | Later | L (auth + proxy + session) | Medium |

---

## 2. Decision tree — what goes where

```
                   ┌─ Is the fix in the browser bundle? ─┐
                   │                                      │
                  YES                                    NO
                   │                                      │
     ┌─ Does it touch `src/app/faq` or `FAQPanel`?  ─┐   ┌─ Is it retrieval / ranking / SQL?
     │                                                │   │
    YES                                              NO   YES → reporium-api runtime lane (B)
     │                                                │         e.g. negated-product filter,
   PR #272 + sibling mitigation (source A)           │         regex route broadening, pgvector
   ─ merge now                                       │         rerank logic.
                                                     │
                         ┌─ Is it UX-visible state? ─┤
                         │                             │
                        YES                           NO
                         │                             │
           Design slice (source C)                Auth / proxy / cookie /
           ─ budget meter                         per-IP quota  →  reporium-api
           ─ grounding badge                     + reporium joint lane (Phase 3,
           ─ cache age pill                       §4.3 below). Not a UX ticket.
           ─ unified status voice
           ─ progressive friction
```

### Router rules future lanes must apply before scheduling

1. **A UX change that improves *accidental* spend is not a substitute for Phase 3.**
   Do not close a Phase 3 ticket because a Phase 1 slice shipped. Source C §8.
2. **A retrieval bug (wrong repo in answer) is never solved in the frontend.**
   The "alternatives to pinecone returns pinecone" shape must be fixed at the
   retrieval layer (source B), not via prompt or client filter.
3. **Product decisions on `/faq` do not gate backend work and vice versa.** If a
   lane finds itself blocked waiting for the other, re-read this section.
4. **The public token is a pre-existing condition, not a regression introduced
   by FAQ.** Source A §Spend-surface assessment is the authoritative framing.

---

## 3. Phased roadmap

### 3.1 Now (2026-04-24 — 2026-04-30)

One outcome: PR #272 merges with the FAQ-local mitigation folded in.

| Item | Repo | Branch | Owner | Effort | Risk | Status today |
|---|---|---|---|---|---|---|
| PR #272 base commit (FAQ page) | `reporium` | `claude/feature/faq-page` | kimmymakesmoves | — | Low | CI-green, Vercel preview green |
| Fold-in: shared rate counter + 1h cache (source A §Minimal patch, +54 LOC in `FAQPanel.tsx`) | `reporium` | `claude/feature/KAN-272-faq-spend-surface` → fold into #272 | Opus lane (sibling, not this one) | S | Low | Diff drafted in source A, not yet committed to PR #272 |

**Blocking deploy check before merge** (from source A §Post-merge):
- `NEXT_PUBLIC_APP_API_TOKEN` set in Vercel production (already required by AskBar — no new env var).
- `reporium-api#433` (newest/oldest SQL column fix) live before marking 16/16 FAQ cards green.
- Confirm Ask quota alert policy still armed (memory: `project_kan120_session_apr15.md` — 6 alert policies live).

**Explicit non-actions in Now:**
- Do **not** wait on Phase 3 (server-side proxy) before merging #272. Source A
  §Wait-for-stronger-Ask-architecture is definitive: architectural fixes live
  in a different repo and are not a gate on a 344-line frontend page.
- Do **not** add grounding badges / budget meter / status voice refactor in
  this PR. Those are Phase 1 design slices (Next).

### 3.2 Next (2026-05-01 — 2026-05-15, order-independent)

Two independent workstreams; they do not block each other.

#### 3.2.1 Next-A — Runtime retrieval correctness (source B)

| Item | Repo | Branch | Effort | Risk | Ticket |
|---|---|---|---|---|---|
| `_extract_negated_repos` helper + post-retrieval filter for #365 | `reporium-api` | `claude/feature/KAN-<id>-ask-retrieval-correctness` | S | Low | Pending |
| `_ROUTE_COMPARISON` regex broadening (`X vs Y`, `X versus Y`, `X or Y`) for #378 | `reporium-api` | same branch | S | Low | Pending |
| Unit tests in `tests/test_ask_retrieval_correctness.py` | `reporium-api` | same branch | S | Low | Pending |

**Files owned (from source B §Deliverables):**
- `app/routers/intelligence.py` (pure additions: `_extract_negated_repos`, filter call at L2588, regex at L287-290).
- `tests/test_ask_retrieval_correctness.py` (new).

**Explicit residuals (source B §Residual gaps) — must be filed as separate
tickets, not silently deferred:**
- Retrieval coverage for named-product-less queries ("vector databases similar to…").
- Multi-word / hyphenated product names beyond single tokens.
- Canonical-repo disambiguation (`LIKE '%X%'` picks most-starred, not canonical).
- Semantic cache poisoning from pre-fix bad answers (TTL wait or bust).

#### 3.2.2 Next-B — Phase 1 design slice 1 (source C §7 Next)

| Item | Repo | Branch | Effort | Risk | Ticket |
|---|---|---|---|---|---|
| `<AskBudgetIndicator />` mounted in `AskBar`, `StickyAskBar` | `reporium` | `claude/feature/KAN-<id>-claude-design-implementation` | S | Low | Draft in source C JIRA |
| (After #272 lands) mount `<AskBudgetIndicator />` in `FAQPanel` header | `reporium` | separate one-line follow-up | XS | Low | Pending |

**Intentionally deferred to later Phase 1 slices (source C JIRA §Out of scope):**
- `<GroundingBadge />` — derives from existing API response; no backend needed.
- `<CacheAgePill />` — needs the sibling-lane cache (`at` field).
- `<AskStatusMessage />` — unified voice layer; replaces four current strings.
- FAQ IA refresh (cost-ascending section order, label rewrites, section pills).
- Progressive friction at ≥7/10 in `FAQPanel.onToggle`.
- "Open in Ask" arrival banner.

Each remaining slice is a separate one-PR lane. Do **not** merge them as a
single big refactor — the design memo explicitly specifies one-PR-per-slice
(source C §10).

### 3.3 Later (2026-05-15+, sequencing depends on ops capacity)

These items are joint `reporium-api` + `reporium` work; they are not frontend-only.

| Item | Repos | Effort | Risk | Notes |
|---|---|---|---|---|
| `/intelligence/ask` returns `Retry-After` header on 429 | `reporium-api` | S | Low | Unblocks UI countdown instead of retry loops |
| `/intelligence/ask` returns `X-Reporium-Ask-Cost: llm|smart` header | `reporium-api` | XS | Low | Removes `tokens_used.total === 0` heuristic from `<GroundingBadge />` |
| UI consumes both headers (countdown + cost pill) | `reporium` | S | Low | Phase 2 frontend follow-up |
| Server-side `/api/ask` route handler in Next.js **or** Cloud Run middleware | `reporium` or `reporium-api` | L | Medium | Holds `APP_API_TOKEN` server-side |
| HttpOnly session cookie issuance + per-IP quota enforcement | `reporium-api` | L | Medium | Replaces client counter as authoritative limit |
| Delete `NEXT_PUBLIC_APP_API_TOKEN` from all client bundles | `reporium` | S | Low | Cannot start until server-side `/api/ask` is live |

**Hard ordering inside Later:** Phase 2 header work is independent and can
ship anytime. Phase 3 proxy must land before the token is removed from the
client bundle; do not attempt the reverse.

**Effort estimate — Phase 3 total:** ~1 engineering-week at priority
(source C §7 Later-later).

---

## 4. Dependencies

### 4.1 What blocks what

```
#272 (Now)
   └── (independent) Next-A runtime retrieval
   └── Next-B AskBudgetIndicator slice 1
         └── (after #272) mount AskBudgetIndicator in FAQPanel
         └── GroundingBadge slice (needs no #272 dep)
         └── CacheAgePill slice (needs #272 sibling-lane cache `at` field)
         └── AskStatusMessage slice (needs no #272 dep)
         └── FAQ IA refresh (needs #272 landed)
         └── Progressive friction (needs #272 landed)

Later Phase 2 headers
   └── enables precise <GroundingBadge cost=...> (removes heuristic)
   └── enables <AskStatusMessage kind='rate' retryAfterSeconds=...>

Later Phase 3 proxy
   └── unblocks removal of NEXT_PUBLIC_APP_API_TOKEN
   └── makes per-IP rate limits enforceable server-side
```

### 4.2 External dependencies

- `reporium-api#433` (newest/oldest SQL column fix) must be live before
  16/16 FAQ cards are marked green — source A §Post-merge checklist.
- Ask quota alert policy must remain armed (6 policies live since
  2026-04-15 per memory `project_kan120_session_apr15.md`).
- Cloud SQL pool at ceiling (memory: `project_ask_sprint1_apr22.md`) —
  FAQ worst-case (16 calls × N visitors) must not coincide with Ask-traffic
  pressure. Mitigation cache brings steady-state to ~0 after first visit.

### 4.3 Phase 3 policy conflict (known inert risk)

Memory `project_ask_sprint1_apr22.md` and overnight release-manager synthesis
note a base-branch policy conflict: the dispatch contract says `main`, while
`reporium/CLAUDE.md` says `dev`. This lane ships to `main` per contract. If
Phase 3 work touches `reporium` and `reporium-api` jointly, resolve the
policy conflict before starting — do not discover it mid-lane.

---

## 5. What must *not* be reopened next week

**For each row below, the question has been answered. If a future lane
proposes re-opening it, the first response is: read this row.**

| Question | Answer | Source |
|---|---|---|
| "Should we block PR #272 until we have a server-side proxy?" | No. The token is pre-existing; FAQ does not widen exposure. Phase 3 is a separate repo and separate schedule. | A §Spend-surface, C §8 |
| "Should the `/faq` page pre-render answers via ISR?" | No. Freezes answer freshness and needs a staleness policy we do not have. Not required to ship #272. | A §Out-of-scope |
| "Should FAQ lazy-fetch via `<details>` be replaced with auto-fetch-on-mount?" | No. Lazy is the spend-conscious default; 16 cards × auto-fetch-on-mount is the failure mode we designed against. | A §Exact runtime behavior |
| "Should we add a CAPTCHA to gate Ask?" | No. Destroys the marketing-surface feel for a problem Phase 3 solves more cleanly. | C §6 anti-pattern |
| "Should we change the embedding model to fix #365?" | No. Architectural, not retrieval. Out of scope. The bounded fix is a post-retrieval negated-product filter. | B §Explicitly out of scope |
| "Should #365 be fixed by rewriting the LLM prompt?" | No. Retrieval layer. Prompt rewrite is a different lane. | B §Root cause |
| "Can the Lane 7 `forbidden_repos` golden-set primitive catch #365?" | No (by construction). Golden set mocks `sources` from fixture_repos; the forbidden repo never enters the mocked list. Runtime fix (source B) is the only path. | B header §Lane 7 note |
| "Should Phase 1 slices be bundled into one big PR?" | No. One-PR-per-slice per design memo §10. Bundling re-introduces the review cost we are trying to avoid. | C §7 |
| "Should the `<AskBudgetIndicator />` refactor the existing 'N questions remaining' warning?" | No. First slice is strictly additive; consolidation is a separate later slice. | C JIRA §Acceptance criteria |
| "Should we add a Cloudflare Turnstile ahead of Phase 3?" | No. Only if post-proxy abuse is observed. Do not deploy preemptively. | C §7 Later-later |
| "Can Phase 1 UX work replace Phase 3 server-side proxy?" | No. Phase 1 reduces accidental over-fetching; Phase 3 stops an attacker reading the bundle. Different threat models. | C §8 |
| "Should `roadmap.json` / `REPORIUM_ROADMAP.md` updates happen in this lane?" | No. Owned by the sibling `KAN-ROADMAP-reporium-roadmap-sync` lane. Merge separately. | This package §1 |

---

## 6. Non-goals (this lane)

This lane produced:
- This decision package.
- The JIRA draft at `.audit/2026-04-24/ask-roadmap-decision-package-jira.md`.

This lane did **not** and will **not**:
- Edit `roadmap.json`, `REPORIUM_ROADMAP.md`, or `README.md` in `reporium-roadmap`.
  (Sibling `KAN-ROADMAP-reporium-roadmap-sync` lane owns those.)
- Edit any files in `reporium`, `reporium-api`, `reporium-ingestion`,
  `reporium-db`, `reporium-mcp`, `reporium-events`, `reporium-audit`,
  `figma-make-perditio-website-claude`, `perditio-workato-integration`.
- Merge PR #272, open it for merge, or request review.
- Deploy anything.
- Create JIRA tickets in the external system (access unavailable from this
  lane; see process rule).
- Write new test coverage (owned by downstream implementation lanes).
- Estimate $-cost impact with numeric precision; effort is T-shirt-sized only.

Items deliberately left unresolved for later decision packages:
- Whether Phase 2 and Phase 3 should be merged into a single backend
  workstream (the design memo treats them as distinct). Defer until Phase 1
  slice 1 (`<AskBudgetIndicator />`) ships and we have real quota-hit data.
- Which specific KAN ticket numbers replace `KAN-ROADMAP` / `KAN-<id>`
  placeholders (pending JIRA access).
- Whether `reporium-mcp` grows an Ask bridge (out of scope here; belongs
  in the suite roadmap sync lane if anywhere).

---

## 7. Architectural boundary — in one paragraph

The Ask surface is a client that holds a publicly-readable token and calls a
public endpoint. **UX work in `reporium` can reduce accidental over-fetching,
make grounding visible, and improve the product's trust story — it cannot
prevent a scripted actor from using the token at will.** Retrieval quality
work in `reporium-api` can fix what the answer says — it cannot change who is
allowed to ask. Real spend containment requires a server-side proxy with
HttpOnly session cookies and per-IP quotas, which is joint
`reporium-api` + `reporium` work filed as Phase 3 and intentionally out of
scope for every lane until separately scheduled. Future lanes should route
their work to the right side of this boundary on the first pass.

---

## 8. Stop-conditions check

- ✅ All three overnight sources were read in full before synthesis.
- ✅ No section is fabricated; every claim traces to one of the three sources
  or to an auto-memory entry explicitly cited.
- ✅ No files edited outside `.audit/2026-04-24/` in this repo.
- ✅ No application-repo edits.
- ✅ No merge, no deploy, no PR request.
- ✅ Package length stays under one-sitting read budget (≈500 lines).
