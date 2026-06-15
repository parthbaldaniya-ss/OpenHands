# EP-14: Revenue & Margin Calculations

Projected revenue from billability × rates, actual revenue from invoices, margin calculations at project/client/company levels, and bench cost tracking.

**Sprint:** 8–9 | **Stories:** 6 | **SP:** 16
**Spec refs:** `fsd/FSD.md` §7.2–7.7, `prd/PRD.md` §5

---

## Story 1: Projected revenue calculation engine

**Size:** M (3 pts) | **Priority:** P1 — Critical | **Sprint:** 8
**Labels:** `backend`, `phase-2`, `sprint-8`, `must-have`

## Context (read before starting)

* `fsd/FSD.md` §7.3 — Projected Revenue formula: billability_pct/100 × working_days × 8 × billing_rate
* `fsd/FSD.md` §2.14 — SystemConfig: working_days=22, working_hours=8

**As a** system, **I want** projected revenue calculated from billability and billing rates **so that** financial forecasts are available.

## Acceptance Criteria

- [ ] Per-assignment projected revenue = billability_pct / 100 × working_days × working_hours × billing_rate
- [ ] Project projected revenue = SUM(per-assignment) for non-shadow ACTIVE assignments
- [ ] Shadow resources excluded from projected revenue (is_shadow = true → 0 revenue)
- [ ] Projected revenue in billing currency, converted to INR using latest exchange rate (or 1.0 for INR)
- [ ] Working days from SystemConfig (default 22)
- [ ] Working hours from SystemConfig (default 8)
- [ ] Handles null billing_rate gracefully (excluded, not zero)
- [ ] Handles assignments with future start_date (excluded from current month)
- [ ] Exposed via GET /api/projects/:id/financials

## Out of Scope

* Month-by-month historical projections
* Leave-adjusted calculations

**Depends On:** EP-10 (billing_rate exists), EP-5 (assignments)

---

## Story 2: Actual revenue from invoices

**Size:** S (2 pts) | **Priority:** P1 — Critical | **Sprint:** 9
**Labels:** `backend`, `phase-2`, `sprint-9`, `must-have`

## Context (read before starting)

* `fsd/FSD.md` §7.4 — Actual Revenue = SUM(invoice.amount_inr) where status ∈ {APPROVED, PAID}

**As a** system, **I want** actual revenue computed from approved/paid invoices **so that** real financial data is available alongside projections.

## Acceptance Criteria

- [ ] Actual Revenue (project) = SUM(amount_inr) for invoices with status APPROVED or PAID
- [ ] Supports period filtering: monthly, quarterly, yearly, all-time
- [ ] Actual revenue is source of truth for financial reporting
- [ ] Exposed via GET /api/projects/:id/financials (alongside projected)
- [ ] Returns both billing currency total and INR total

## Out of Scope

* Payment tracking details
* Accounts receivable aging

**Depends On:** EP-12 (Invoices exist)

---

## Story 3: Margin calculation — Projected and actual

**Size:** M (3 pts) | **Priority:** P1 — Critical | **Sprint:** 9
**Labels:** `backend`, `phase-2`, `sprint-9`, `must-have`

## Context (read before starting)

* `fsd/FSD.md` §7.5 — Margin formulas: Projected Margin = Projected Revenue − Total Cost, Actual Margin = Actual Revenue − Total Cost, Margin % = Margin / Revenue × 100

**As a** CEO/CTO/Finance user, **I want** margin calculations showing profitability **so that** I can assess project health.

## Acceptance Criteria

- [ ] Total Project Cost = Resource Cost (§7.2) + Non-Human Cost (INR)
- [ ] Projected Margin = Projected Revenue (INR) − Total Project Cost
- [ ] Actual Margin = Actual Revenue (INR) − Total Project Cost
- [ ] Margin % = Margin / Revenue × 100 (handle zero revenue → 0%)
- [ ] Includes shadow resource costs (they count toward cost but not revenue)
- [ ] Exposed via GET /api/projects/:id/financials
- [ ] Restricted to CEO, CTO, Finance, configurable for DM
- [ ] Returns null for unauthorized roles

## Out of Scope

* Margin alerts (Phase 3)
* What-if scenario planning
* Month-over-month margin trends

**Depends On:** Story 1, Story 2, EP-10 Story 3, EP-13

---

## Story 4: Bench cost calculation

**Size:** S (2 pts) | **Priority:** P2 — Major | **Sprint:** 9
**Labels:** `backend`, `phase-2`, `sprint-9`

## Context (read before starting)

* `fsd/FSD.md` §7.6 — Bench Cost: Daily = loaded_cost_monthly / 22, Total = Daily × days_on_bench

**As a** CTO, **I want** bench cost quantified **so that** the financial impact of idle resources is visible.

## Acceptance Criteria

- [ ] Daily Bench Cost (resource) = loaded_cost_monthly / working_days_per_month
- [ ] Total Bench Cost (resource) = Daily Cost × days_on_bench
- [ ] Company total bench cost = SUM(all bench resource costs)
- [ ] Resources without loaded_cost_monthly: excluded
- [ ] Exposed via GET /api/dashboard/bench-costs (CEO/CTO/Finance)
- [ ] Per-resource bench cost in resource availability response

## Out of Scope

* Historical bench cost trends
* Bench cost projections

**Depends On:** EP-7 Story 3 (Bench detection), EP-10 Story 1

---

## Story 5: Client-level financial aggregation

**Size:** M (3 pts) | **Priority:** P2 — Major | **Sprint:** 9
**Labels:** `backend`, `phase-2`, `sprint-9`

## Context (read before starting)

* `fsd/FSD.md` §7.5 — "Client-level: sum across all projects"
* `prd/PRD.md` §4.1 — Client dashboard: total billing, total cost, aggregate margin

**As a** CEO/CTO, **I want** financial metrics aggregated at the client level **so that** client profitability is visible.

## Acceptance Criteria

- [ ] GET /api/clients/:id/financials — returns aggregated metrics
- [ ] Total Projected Revenue (INR) = SUM across all client's active projects
- [ ] Total Actual Revenue (INR) = SUM across all client's invoices
- [ ] Total Cost (INR) = SUM(resource cost + non-human cost) across all projects
- [ ] Projected Margin = Projected Revenue − Total Cost
- [ ] Actual Margin = Actual Revenue − Total Cost
- [ ] Active resource count deployed to client
- [ ] Restricted to CEO, CTO, Finance

## Out of Scope

* Client revenue trends
* Client-level billing reports

**Depends On:** Story 3

---

## Story 6: Company-level financial aggregation

**Size:** M (3 pts) | **Priority:** P2 — Major | **Sprint:** 9
**Labels:** `backend`, `phase-2`, `sprint-9`

## Context (read before starting)

* `fsd/FSD.md` §7.5 — "Company-level: sum across all projects"

**As a** CEO, **I want** company-wide financial metrics **so that** I can assess overall business health.

## Acceptance Criteria

- [ ] GET /api/dashboard/financials — returns company-wide aggregation
- [ ] Total Projected Revenue (INR) across all active projects
- [ ] Total Actual Revenue (INR) across all invoices (APPROVED/PAID)
- [ ] Total Resource Cost across all projects
- [ ] Total Non-Human Cost across all projects
- [ ] Total Bench Cost
- [ ] Projected Margin and Actual Margin with percentages
- [ ] Breakdown by project type (FP, T&M, Onboarding)
- [ ] Restricted to CEO, CTO, Finance

## Out of Scope

* Historical financial snapshots
* Budget vs actual comparison

**Depends On:** Story 3, Story 4, Story 5
