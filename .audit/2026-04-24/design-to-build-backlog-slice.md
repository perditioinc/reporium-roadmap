# Design-to-Build Backlog Slice — Reporium Ask / FAQ

**Date:** 2026-04-24 (hour 9 of overnight run)
**Lane:** `claude/feature/KAN-DESIGN2BUILD-design-to-build-backlog-slice` off `main`
**Author:** Opus 4.7 (design-to-build lane)
**Repo:** `reporium-roadmap` (this repo, docs only)
**Owned scope:** `.audit/2026-04-24/design-to-build-backlog-slice*.md`

> Read-only with respect to application repos. This document **plans** work;
> it does not ship any code. Implementation lanes consume it next.

---

## 0. Source material

| Source | Type | Used for |
|---|---|---|
| `reporium/.audit/2026-04-24/claude-design-implementation-jira.md` | Phase-1 first slice (`<AskBudgetIndicator />`) | Phase 1 enumeration; design principle P2 reference |
| `reporium/.audit/2026-04-24/kan-faq-spend-surface-jira.md` | Concrete diff for FAQPanel mitigation | Phase 1 spend-surface slice |
| `reporium/.audit/2026-04-24/pr-272-faq-decision.md` | Merge verdict + post-merge checklist for PR #272 | Sequencing constraints; FAQ surface |
| `reporium/.audit/2026-04-24/frontend-performance-jira.md` | KAN-248 `StickyAskBarBoot` lazy-boot pattern | Phase 1 perf slice (adjacent) |

### Source material that is **missing**

The Phase-1 first-slice ticket references a parent memo:
`reporium-ask-faq-design-memo.md`. **That file does not exist** anywhere
under `.audit/` in `reporium`, `reporium-roadmap`, or
`figma-make-perditio-website-claude`. Where this backlog refers to a
design-named component (`<GroundingBadge />`, `<CacheAgePill />`,
`<AskStatusMessage />`, "FAQ IA refresh", "progressive friction", "Open in
Ask deep-link banner") the ticket *named* the slice but did not specify it.
Specifications are therefore **assumed** based on the surrounding context
(existing AskBar / StickyAskBar code paths, the four-vector trust story)
and clearly flagged as such in §4 below.

---

## 1. TL;DR

Convert overnight design output into a phased backlog of **11 shippable
slices** plus 4 server-side and 4 observability slices. Drive everything
off four design principles inferable from existing tickets:

- **P1 — Trust scaffolding is visible.** Provenance / verifiability /
  freshness / agreement signals appear inline on every Ask answer
  (per the `/ai-native` four-vector trust story).
- **P2 — Show the budget, don't just enforce it.** The 10/min · 100/day
  cap is rendered as a meter, not an error popup.
- **P3 — One spend counter, one cache, one voice.** AskBar, StickyAskBar,
  and FAQPanel share the `reporium_ask_timestamps` key and a unified
  status-message vocabulary.
- **P4 — Don't pay for the bar on first paint.** StickyAskBar's heavy
  module graph (framer-motion + react-markdown + remark-gfm +
  rehype-sanitize) loads on idle/interaction, not in the root layout
  chunk.

Phase 1 (frontend-only) is a **wave of small parallel PRs** that can
land within the next two days without any backend dependency. Phase 2
(server `Retry-After` + cost header) and Phase 3 (server-side proxy +
HttpOnly session) are real engineering work in `reporium-api` that
unblock the long-term spend-surface story but are **not gating** for the
Phase 1 wave.

---

## 2. Slice catalogue (Part A — split by owner type)

### 2.1 Frontend-only (reporium repo, Next.js)

| ID | Slice | Files (best estimate) | Status of spec |
|---|---|---|---|
| FE-1 | `<AskBudgetIndicator />` budget meter | `src/components/AskBudgetIndicator.tsx` (new), mounts in `AskBar.tsx`, `StickyAskBar.tsx` | **Specified** in `claude-design-implementation-jira.md` |
| FE-2 | FAQPanel spend mitigation (shared rate counter + 1h answer cache) | `src/components/FAQPanel.tsx` (~+55 lines) | **Specified** with full diff in `kan-faq-spend-surface-jira.md` |
| FE-3 | Mount `<AskBudgetIndicator />` in `FAQPanel` | `src/components/FAQPanel.tsx` (~+2 lines) | Trivial; **assumed** from FE-1 + FE-2 + decision memo |
| FE-4 | `<GroundingBadge />` per-answer trust chip | `src/components/GroundingBadge.tsx` (new), call sites in `AskBar`, `StickyAskBar`, `FAQPanel` | **Assumed** — named only |
| FE-5 | `<CacheAgePill />` "answered N min ago / fresh" | `src/components/CacheAgePill.tsx` (new), call sites in `FAQPanel` (where the localStorage cache lives) | **Assumed** — named only |
| FE-6 | `<AskStatusMessage />` unified status voice (consolidates the existing "N questions remaining" warning + rate-limit errors + retry hints into one vocabulary) | `src/components/AskStatusMessage.tsx` (new), replaces inline copy in `AskBar.tsx`, `StickyAskBar.tsx`, `FAQPanel.tsx` | **Assumed** — named only |
| FE-7 | FAQ IA refresh (regroup the 16 curated questions by user intent rather than feature surface) | `src/components/FAQPanel.tsx` (sections array only); content edits | **Assumed** — named only; product-owned |
| FE-8 | Progressive friction at ≥7/10 (soft "you're approaching the cap" UI; e.g. greyed submit, longer cooldown spinner, copy nudge) | `src/components/AskBar.tsx`, `src/components/StickyAskBar.tsx` | **Assumed** — named only |
| FE-9 | "Open in Ask →" deep-link banner from FAQ (mirror of the existing per-card link, but a top-of-page CTA when the user opens FAQ from a `?from=ask-empty-state` referrer) | `src/components/FAQPanel.tsx`, query-param read | **Assumed** — named only |
| FE-10 | `StickyAskBarBoot` lazy boot (KAN-248) | `src/components/StickyAskBarBoot.tsx` (new), `src/components/LayoutShell.tsx` (mount swap) | **Specified** in `frontend-performance-jira.md` |

### 2.2 Backend / API / auth (reporium-api repo, FastAPI on Cloud Run)

| ID | Slice | Surfaces | Status of spec |
|---|---|---|---|
| BE-1 | `Retry-After` header on 429 from `/intelligence/ask` | `app/routers/intelligence.py` (or equivalent), middleware | **Named** in `claude-design-implementation-jira.md` "Phase 2"; spec **assumed** to mean RFC 7231 seconds-form; pair with FE-6 |
| BE-2 | Cost header on every `/intelligence/ask` response (e.g. `X-Ask-Cost-USD`, `X-Ask-Token-Count`) | Same router | **Named** Phase 2; **assumed** to be advisory-only headers consumed by FE-1/FE-5/FE-6 |
| BE-3 | Per-IP quota enforcement on `/intelligence/ask` (server-side cap, not just per-token) | Cloud Run middleware (FastAPI dependency or upstream Nginx/ESPv2 if used) | **Named** in `pr-272-faq-decision.md` as out-of-scope-for-FE; needs spec |
| BE-4 | Server-side proxy for `/intelligence/ask` with HttpOnly session cookie (replace `NEXT_PUBLIC_APP_API_TOKEN` exposure on `reporium.com`) | New Next.js route handler (`src/app/api/ask/route.ts`) **and** API auth changes (short-lived signed token issuance) | **Named** Phase 3; significant — spans both repos |

### 2.3 Product / content (reporium repo, copy + curation)

| ID | Slice | Owner | Status of spec |
|---|---|---|---|
| PC-1 | Curated 16-question list review (re-grade for trust-foundation alignment with `/ai-native` Slides 2 and 4) | Product / @kimmymakesmoves | Implicit in `pr-272-faq-decision.md` post-merge checklist |
| PC-2 | FAQ IA grouping (input to FE-7) | Product | **Assumed** — named only |
| PC-3 | Status-message vocabulary (input to FE-6 — "approaching cap", "cap reached", "retry in N seconds", "served from cache N min ago", "answered live N seconds ago") | Product + FE | **Assumed** |
| PC-4 | Verifiability copy on FAQ ("Open in Ask to re-run this question live" — already present on per-card link; tighten to match Slides 2/4 wording) | Product | Implicit in `pr-272-faq-decision.md` "trust-surface check" |

### 2.4 Observability / spend control

| ID | Slice | Owner | Status of spec |
|---|---|---|---|
| OBS-1 | Verify Ask quota alert policy is armed in GCP (already 6 alert policies live per `project_kan120_session_apr15.md` — confirm `/intelligence/ask` 429-rate is one of them; if not, add) | Ops / @kimmymakesmoves | Implicit post-merge checklist item from `pr-272-faq-decision.md` |
| OBS-2 | Dashboard slice: `/faq` page-views vs `/intelligence/ask` call rate (correlate to confirm FAQ cache + counter are doing their job in the first 48h post-merge) | Ops | Implicit post-merge item |
| OBS-3 | Cost-per-call telemetry (BE-2 emits the headers; capture them server-side in structured logs / Sentry tag for $/day rollups) | API | Pairs with BE-2 |
| OBS-4 | FAQ cache hit-rate metric (frontend ping or server-side inference from referrer + `If-None-Match`-equivalent custom header) | FE + Ops | Validates FE-2 / FE-3 / FE-5 |

---

## 3. Per-slice card (Part B — outcome / owner / risk / deps / validation)

### 3.1 Frontend-only slices

#### FE-1 — `<AskBudgetIndicator />` budget meter
- **Outcome:** Persistent `{minuteCount}/10 · {dayCount}/100` meter with progress bar; amber at ≥7/10 or ≥70/100; red at cap. SSR-safe; `role="status" aria-live="polite"`.
- **Owner type:** Frontend (FE).
- **Risk:** Low. Reads the existing `reporium_ask_timestamps` localStorage key — no schema change. 10s polling interval — verify no perceivable battery cost on mobile.
- **Dependencies:** None — reads keys already written by AskBar/StickyAskBar.
- **Validation:** Jest test (mocks localStorage at thresholds 0/8/10 and 0/70/100); manual smoke per ticket §"Definition of done".

#### FE-2 — FAQPanel spend mitigation
- **Outcome:** FAQ expansions count against the same 10/min · 100/day budget; identical questions served from a 1h localStorage answer cache.
- **Owner type:** Frontend.
- **Risk:** Low. Diff already drafted in `kan-faq-spend-surface-jira.md`; net +55 lines in one file.
- **Dependencies:** **Sequencing** — depends on PR #272 being merged (or fold into #272 as a second commit per the FAQ decision memo).
- **Validation:** Unit test (`getRateLimitState` + `recordRequest` parity with AskBar's helpers); manual smoke per FAQ decision memo.

#### FE-3 — Mount `<AskBudgetIndicator />` in `FAQPanel`
- **Outcome:** Same meter visible in FAQ.
- **Owner type:** Frontend.
- **Risk:** Trivial — 2 lines.
- **Dependencies:** FE-1 **and** PR #272 (FAQPanel must exist on `main`).
- **Validation:** Visual smoke; same Jest mounting test extended to FAQPanel.

#### FE-4 — `<GroundingBadge />`
- **Outcome:** Per-answer chip indicating provenance (e.g. "Grounded in N sources" with hover detail; or "Smart-route: count_repos_by_category"). Operationalizes trust vector P1.
- **Owner type:** Frontend.
- **Risk:** Medium — depends on what the API response carries today. If smart-route metadata is not returned by `/intelligence/ask`, BE work is required first.
- **Dependencies:** Audit `/intelligence/ask` response shape — if `sources` + smart-route name are already present, FE-only; otherwise BE precursor.
- **Validation:** Jest snapshot for grounded vs ungrounded states; manual smoke against three known smart-route paths (count, leaderboard, comparison).

#### FE-5 — `<CacheAgePill />`
- **Outcome:** Pill rendering "Fresh" (live), "Cached 12 min ago", or "Cached 58 min ago" next to FAQ answers, based on FE-2's cache `at` timestamp.
- **Owner type:** Frontend.
- **Risk:** Low. Pure derivation from FE-2's cache shape.
- **Dependencies:** FE-2.
- **Validation:** Jest test with seeded cache entries at 0s / 12 min / 58 min / 61 min.

#### FE-6 — `<AskStatusMessage />` unified voice
- **Outcome:** One component owns all user-facing Ask status copy: idle, near-cap, at-cap, server error, retry hint, served-from-cache. Replaces three sites of inline copy.
- **Owner type:** Frontend.
- **Risk:** **Medium.** This is a refactor across AskBar, StickyAskBar, FAQPanel — each currently has its own copy. Risk of regressing edge cases (the StickyAskBar streaming-error path; AskBar's near-limit warning).
- **Dependencies:** FE-1 (so the meter carries the visible threshold and the message can stay short); ideally PC-3 (product-owned vocabulary) before code merge.
- **Validation:** Jest tests for each status; visual diff in Vercel preview against current production strings.

#### FE-7 — FAQ IA refresh
- **Outcome:** 16 curated questions regrouped by *user intent* rather than *feature surface*; section names tightened.
- **Owner type:** Frontend (mechanical) + Product (semantic).
- **Risk:** Low if PC-2 is provided; medium if FE invents the grouping.
- **Dependencies:** PC-2 (product input).
- **Validation:** Visual review in Vercel preview; no automated test.

#### FE-8 — Progressive friction at ≥7/10
- **Outcome:** Submit button disables for ~2s with an explanatory tooltip when the user is at 7/10 minute or 70/100 day; copy in line with FE-6.
- **Owner type:** Frontend.
- **Risk:** Medium — UX choice that can frustrate users; needs a short A/B or kill-switch flag.
- **Dependencies:** FE-1, FE-6.
- **Validation:** Jest threshold test; opt-in flag (`localStorage['reporium_ask_friction']`) so it can be toggled off without a redeploy.

#### FE-9 — "Open in Ask →" banner
- **Outcome:** When `/faq?from=ask-empty-state` is the referrer, a top-of-page CTA invites the user back to Ask with a pre-seeded question.
- **Owner type:** Frontend.
- **Risk:** Low — additive, query-param-gated.
- **Dependencies:** FE-7 (don't ship the banner until IA is final, to avoid two churn passes on FAQPanel).
- **Validation:** Manual smoke with `?from=ask-empty-state`; no test required.

#### FE-10 — `StickyAskBarBoot` lazy boot (KAN-248)
- **Outcome:** Root layout ships a 56 px placeholder; the real `StickyAskBar` and its 4 heavy deps fetch on idle/interaction. Lighthouse delta to be captured in the PR description.
- **Owner type:** Frontend.
- **Risk:** Medium — placeholder/real swap can layout-shift if classes drift; first keystroke before idle could lose `/`/`Ctrl+K` (mitigated in the ticket).
- **Dependencies:** None — `LayoutShell.tsx` and `StickyAskBar.tsx` are the only files touched. Independent of FAQ work.
- **Validation:** `npm run build` + `npm run type-check`; Lighthouse re-run on Vercel preview; visual smoke per ticket §"Validation".

### 3.2 Backend / API / auth slices

#### BE-1 — `Retry-After` on 429 from `/intelligence/ask`
- **Outcome:** Server-side rate limiter (whatever it is today on the global token) returns `Retry-After: <seconds>` so FE-6 can render an exact cooldown rather than "try again in a minute".
- **Owner type:** Backend.
- **Risk:** Low. Stdlib pattern; no client compat concern (current FE ignores the header).
- **Dependencies:** None.
- **Validation:** pytest assertion that 429 carries `Retry-After`; manual smoke with a tight loop.

#### BE-2 — Cost header on `/intelligence/ask`
- **Outcome:** Every successful response carries `X-Ask-Cost-USD` (computed from token counts × prices) and `X-Ask-Token-Count`. Powers FE-5/OBS-3 and gives Ops a per-call cost lens.
- **Owner type:** Backend.
- **Risk:** Low — additive headers; no client breakage.
- **Dependencies:** None.
- **Validation:** pytest assertion that smart-route answers carry `X-Ask-Cost-USD: 0.000…` (≈0 because no LLM); LLM-answered questions carry a non-zero value; structured-log capture in OBS-3.

#### BE-3 — Per-IP quota
- **Outcome:** Server caps requests per-IP regardless of token, defending against `NEXT_PUBLIC_APP_API_TOKEN` extraction and replay.
- **Owner type:** Backend + infra.
- **Risk:** **Medium-high.** Behind Cloud Run, the IP visible to FastAPI is the load balancer; need `X-Forwarded-For` parsing with a trusted-proxy allowlist. Mis-tuned this can rate-limit legitimate office NAT traffic.
- **Dependencies:** Decision on what "per-IP" actually means (per-IP vs per-IP+UA hash); ops sign-off.
- **Validation:** Loadtest from two source IPs; verify each gets its own bucket; verify `Retry-After` (from BE-1) is sane.

#### BE-4 — Server-side proxy + HttpOnly session
- **Outcome:** Browser no longer carries `NEXT_PUBLIC_APP_API_TOKEN`. Next.js route handler at `/api/ask` mints a short-lived signed token per session (HttpOnly cookie) and proxies to `reporium-api`. Token never leaves the server.
- **Owner type:** Backend (both repos).
- **Risk:** **High.** Touches reporium-api auth, breaks the FAQPanel/AskBar/StickyAskBar/AskPanel/NLFilterBar/dataProvider call sites simultaneously, and changes the contract documented in the FAQ decision memo. Requires a flag-gated rollout and a backwards-compatible window where both auth modes are accepted by reporium-api.
- **Dependencies:** BE-1, BE-2, BE-3 (so the proxy has rate-limit + cost telemetry to forward).
- **Validation:** Phased — start with a single non-prod environment; flip the FE flag to use `/api/ask`; verify all five call sites; verify no `NEXT_PUBLIC_APP_API_TOKEN` left in the bundle (`grep` against `npm run build` output).

### 3.3 Product / content slices

| ID | Outcome | Owner | Risk | Deps | Validation |
|---|---|---|---|---|---|
| PC-1 | 16-question list re-graded against `/ai-native` Slides 2 & 4 trust narrative; replacements proposed for any low-grounding entries | Product | Low | None | Self-review + author sign-off |
| PC-2 | Section names + grouping for FAQ IA | Product | Low | None | Feeds FE-7 |
| PC-3 | Status-message vocabulary doc (5 states minimum) | Product + FE | Low | None | Feeds FE-6 |
| PC-4 | Verifiability copy tightened to match `/ai-native` | Product | Low | PR #272 merged | Visual review |

### 3.4 Observability / spend control slices

| ID | Outcome | Owner | Risk | Deps | Validation |
|---|---|---|---|---|---|
| OBS-1 | Confirm GCP alert policy fires on `/intelligence/ask` 429 rate; add if missing | Ops | Low | None | Synthetic 429 burst in non-prod |
| OBS-2 | Dashboard correlating `/faq` page-views and `/intelligence/ask` call rate (48h post #272 merge) | Ops | Low | PR #272 merged | First-week review meeting |
| OBS-3 | Capture `X-Ask-Cost-USD` in structured logs; daily $/day rollup | Ops + API | Low | BE-2 | Sentry tag visible; daily rollup query returns sane number |
| OBS-4 | FAQ cache hit-rate metric (FE pings `/metrics/ping?event=faq_cache_hit` or sets a header for server-side counting) | FE + Ops | Low | FE-2 | Hit-rate observable in dashboard within 48h |

---

## 4. Unresolved design ambiguities (the missing parent memo would have answered these)

1. **`<GroundingBadge />` exact taxonomy.** Trust vector P1 has four sub-vectors (provenance, verifiability, freshness, agreement). Does this badge encode all four, or just provenance? Source count? Smart-route name? The first-slice ticket only names the component.
2. **`<CacheAgePill />` placement.** Inside the `<details>` body next to the answer, or adjacent to the question summary? The latter affects FAQPanel layout markedly.
3. **`<AskStatusMessage />` vocabulary.** PC-3 is a product input — until it exists, FE-6 is blocked from a clean implementation. Without the parent memo we don't know if "approaching cap" should be soft ("Saving your remaining questions for later?") or factual ("3 questions left this minute").
4. **Progressive friction at ≥7/10 — what shape?** Tooltip? Disabled button + countdown? Modal? The first-slice ticket names the slice but not the interaction model.
5. **FAQ IA grouping.** The current 5-section grouping mirrors feature surfaces (search, taxonomy, leaderboards, …). The "intent-based" regroup is **assumed** but not specified. Could be: "Find tools" / "Compare options" / "Understand the corpus" / "About Reporium" — pure speculation until PC-2 is produced.
6. **"Open in Ask" banner trigger.** `?from=ask-empty-state` is **assumed**; could equally be a generic "ask returned no answer" referrer chain or a session-storage flag.
7. **BE-3 per-IP quota policy.** Limits per-IP, per-IP+UA, per-session-cookie, or per-token? Significant operational difference.
8. **BE-4 rollout strategy.** Flag-gated cutover or hard switch? The FAQ decision memo defers this entirely to "reporium-api + infra" without specifying.

These ambiguities should not block FE-1, FE-2, FE-3, FE-10, BE-1, BE-2,
PC-1, OBS-1, OBS-2, OBS-3, OBS-4 — those slices are specified or
specifiable from existing code. They **do** block FE-4 through FE-9
and BE-3 / BE-4 from going to a coding lane today.

---

## 5. Suggested JIRA decomposition (Part C — one ticket per shippable slice)

Replace `KAN-XXX` with real IDs once JIRA returns. Order in this list is
*creation order*, not *ship order* — see §6 for the dependency graph.

| Proposed ticket | Slice | One-line summary |
|---|---|---|
| KAN-AB1 | FE-1 | Ship `<AskBudgetIndicator />` — make 10/min · 100/day budget visible (already drafted in `claude-design-implementation-jira.md`) |
| KAN-FQ1 | FE-2 | Share Ask rate counter + 1h answer cache in `FAQPanel` (already drafted in `kan-faq-spend-surface-jira.md`) |
| KAN-FQ2 | FE-3 | Mount `<AskBudgetIndicator />` in `FAQPanel` |
| KAN-GR1 | FE-4 | Add `<GroundingBadge />` to Ask answers (FE + API audit) |
| KAN-CA1 | FE-5 | Add `<CacheAgePill />` to FAQ answer cards |
| KAN-SM1 | FE-6 | Consolidate Ask status copy into `<AskStatusMessage />` |
| KAN-IA1 | FE-7 | Refresh FAQ section grouping (intent-based) |
| KAN-PF1 | FE-8 | Progressive friction at ≥7/10 of Ask budget |
| KAN-OL1 | FE-9 | "Open in Ask →" banner from FAQ empty-state referrer |
| KAN-248 | FE-10 | Defer `StickyAskBar` bundle off the initial paint (existing #248) |
| KAN-RA1 | BE-1 | Add `Retry-After` header to `/intelligence/ask` 429 responses |
| KAN-CH1 | BE-2 | Emit `X-Ask-Cost-USD` and `X-Ask-Token-Count` headers |
| KAN-IP1 | BE-3 | Per-IP rate limiting on `/intelligence/ask` |
| KAN-SP1 | BE-4 | Server-side Ask proxy + HttpOnly session token |
| KAN-PC1..4 | PC-1..4 | Product/content slices (one ticket each) |
| KAN-OB1..4 | OBS-1..4 | Observability slices (one ticket each) |

Each ticket is **one branch, one PR, one owned file set** per the dispatch
contract.

---

## 6. Parallel vs sequential (Part C, dependency graph)

### 6.1 What can ship in parallel right now

Five slices are independent and can fan out today (no cross-file conflict;
no shared dependency):

```
FE-1  AskBudgetIndicator       ── can start now
FE-10 StickyAskBarBoot          ── can start now (KAN-248)
BE-1  Retry-After               ── can start now
BE-2  Cost headers              ── can start now
PC-1  16-question re-grade      ── can start now
OBS-1 Quota alert verification  ── can start now
```

These six can ship in any order; none touches the same file as another.

### 6.2 What must wait for PR #272 to merge

PR #272 introduces `src/components/FAQPanel.tsx`. Anything that touches
that file is gated:

```
PR #272 merged
   ├── FE-2  FAQPanel spend mitigation        (or fold into #272 pre-merge)
   │     └── FE-3   Mount AskBudgetIndicator  (needs FE-1 too)
   │     └── FE-5   CacheAgePill              (needs cache from FE-2)
   │     └── PC-4   Verifiability copy
   │
   ├── FE-7  FAQ IA refresh                   (needs PC-2)
   │     └── FE-9   Open-in-Ask banner
   │
   └── OBS-2 page-views vs ask-rate dashboard
```

### 6.3 Sequential refactor train

`<AskStatusMessage />` consolidates copy currently inlined in three
components. Anything that adds *new* status strings should land **before**
FE-6 (so FE-6 sees the full set), or **after** (so FE-6 doesn't fight a
moving target). The cleanest order:

```
FE-1  AskBudgetIndicator    →  FE-6  AskStatusMessage    →  FE-8  Progressive friction
                               (consumes vocab from PC-3)    (uses FE-6 strings)
```

### 6.4 Backend train (long-term spend story)

```
BE-1  Retry-After     ┐
BE-2  Cost headers    ┤
BE-3  Per-IP quota    ┘  →  BE-4  Server-side proxy + HttpOnly session
                              (needs all three to forward + log)
```

BE-4 is the most expensive ticket in the catalogue and should be sized
separately, with its own design review. It is **not** required for any
Phase 1 frontend slice.

### 6.5 Gantt-shaped summary

```
Day 0 (today)        Day +1                Day +2..N
├─ FE-1  ───────────┐
├─ FE-10 ───────────┤
├─ BE-1  ───────────┤   [merge PR #272]
├─ BE-2  ───────────┤        │
├─ PC-1  ───────────┤        ├─ FE-2 ──┐
├─ OBS-1 ───────────┘        ├─ FE-7 ──┤      ├─ FE-3 ─────────┐
                              ├─ FE-3   │      ├─ FE-5         │
                              ├─ PC-4   │      ├─ FE-9         │
                              └─ OBS-2 ─┘      ├─ FE-6 ────────┤
                                                ├─ FE-8         │
                                                ├─ OBS-3 (BE-2) │
                                                └─ OBS-4 (FE-2) ┘

Backend train (parallel, separate review):  BE-1 → BE-2 → BE-3 → BE-4
```

---

## 7. Suggested execution grouping

Feed these groupings directly into the next dispatch sheet:

- **Wave 2A — start now, no dependencies (six lanes, six branches):**
  FE-1, FE-10, BE-1, BE-2, PC-1, OBS-1.
- **Wave 2B — once PR #272 merges (four lanes):** FE-2 (or fold into #272),
  FE-3, OBS-2, PC-4.
- **Wave 2C — after Wave 2B + product input PC-2/PC-3 land (four lanes):**
  FE-5, FE-6, FE-7, OBS-3 (gated on BE-2 having shipped).
- **Wave 2D — UX refinements (two lanes):** FE-8 (depends FE-6), FE-9
  (depends FE-7), OBS-4 (depends FE-2).
- **Wave 3 — backend hardening (two lanes, separate cadence):** BE-3,
  then BE-4 with its own design review.

---

## 8. Stop conditions check

- ✅ Did **not** edit any application repo (`reporium`, `reporium-api`,
  `figma-make-perditio-website-claude`).
- ✅ Did **not** merge or deploy.
- ✅ Parent design memo absent → produced a **partial** backlog with
  **assumed** slices clearly flagged and listed in §4.
- ✅ Branch name follows convention:
  `claude/feature/KAN-DESIGN2BUILD-design-to-build-backlog-slice` off `main`.
- ✅ Owned files are scoped to `.audit/2026-04-24/` in this repo.
- ✅ No invented JIRA IDs in code; placeholders used throughout.

---

## 9. Deliverables produced by this lane

1. `.audit/2026-04-24/design-to-build-backlog-slice.md` (this file).
2. `.audit/2026-04-24/design-to-build-backlog-slice-jira.md` (JIRA fallback).
3. **Suggested execution grouping** — §7 above.
4. **Unresolved design ambiguities** — §4 above.
