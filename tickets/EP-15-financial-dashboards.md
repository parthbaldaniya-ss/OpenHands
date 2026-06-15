# EP-15: Financial Dashboards

Revenue, cost, and margin visual dashboards for Finance, CEO, and CTO — with project and client drill-down.

**Sprint:** 9 | **Stories:** 4 | **SP:** 14
**Spec refs:** `fsd/FSD.md` §9, `prd/PRD.md` §7 (Phase 2)

---

## Story 1: Financial dashboard data API — Revenue, cost, margin

**Size:** M (3 pts) | **Priority:** P2 — Major | **Sprint:** 9
**Labels:** `backend`, `phase-2`, `sprint-9`, `must-have`

## Context (read before starting)

* `fsd/FSD.md` §7.2–7.5 — All financial calculation formulas
* `fsd/FSD.md` §9 — Company Dashboard financial widgets

**As a** CEO/Finance user, **I want** a consolidated financial data API **so that** dashboards load efficiently.

## Acceptance Criteria

- [ ] GET /api/dashboard/financial — returns all financial metrics
- [ ] Revenue Summary: projected vs actual (INR), by project type
- [ ] Cost Summary: resource cost, non-human cost, bench cost (INR)
- [ ] Margin Summary: projected margin, actual margin, margin %
- [ ] Top 5 projects by revenue, Top 5 by margin
- [ ] Revenue by client (top 10)
- [ ] Monthly trend data: last 6 months of projected vs actual
- [ ] Restricted to CEO, CTO, Finance
- [ ] Response time < 2s

## Out of Scope

* Custom date range (default: current month + last 6 months)
* Export functionality

**Depends On:** EP-14 (All calculation engines)

---

## Story 2: Financial dashboard UI — Revenue vs cost widgets

**Size:** L (5 pts) | **Priority:** P2 — Major | **Sprint:** 9
**Labels:** `frontend`, `phase-2`, `sprint-9`, `must-have`

## Context (read before starting)

* `prd/PRD.md` §7 — Phase 2: Financial Dashboards for Finance, CEO, CTO
* `fsd/FSD.md` §9 — Company Dashboard: Revenue Summary widget

**As a** CEO, **I want** a visual financial dashboard **so that** I can assess company financial health at a glance.

## Acceptance Criteria

- [ ] Revenue KPI cards: Projected Revenue (INR), Actual Revenue (INR), Variance
- [ ] Cost KPI cards: Resource Cost, Non-Human Cost, Bench Cost
- [ ] Margin KPI cards: Projected Margin %, Actual Margin %
- [ ] Revenue vs Cost bar chart (projected vs actual)
- [ ] Revenue by project type pie/donut chart
- [ ] Monthly trend line chart: projected vs actual revenue (last 6 months)
- [ ] Top projects table: name, projected revenue, actual revenue, margin %
- [ ] Drill-down links to project detail
- [ ] Responsive layout
- [ ] Loading states for each widget
- [ ] Only visible to CEO, CTO, Finance roles

## Out of Scope

* Custom date range selector
* PDF export
* Budget tracking

**Depends On:** Story 1

---

## Story 3: Project financial summary — Projected vs actual

**Size:** M (3 pts) | **Priority:** P2 — Major | **Sprint:** 9
**Labels:** `frontend`, `phase-2`, `sprint-9`

## Context (read before starting)

* `fsd/FSD.md` §9 — Project Detail View → Financials section (restricted)

**As a** CEO/CTO/Finance user, **I want** financial metrics displayed on the project detail page **so that** per-project profitability is visible.

## Acceptance Criteria

- [ ] Financial section on project detail page (CEO/CTO/Finance, configurable for DM)
- [ ] Projected Revenue (billing currency + INR)
- [ ] Actual Revenue (INR, from invoices)
- [ ] Resource Cost (INR)
- [ ] Non-Human Cost (INR)
- [ ] Total Cost (INR)
- [ ] Projected Margin (INR + %)
- [ ] Actual Margin (INR + %)
- [ ] Revenue vs Cost visual (progress bar or simple chart)
- [ ] Section completely hidden for unauthorized roles

## Out of Scope

* Monthly breakdown within project
* Cost burn rate analysis

**Depends On:** EP-14, EP-3 Story 6

---

## Story 4: Client financial summary view

**Size:** M (3 pts) | **Priority:** P2 — Major | **Sprint:** 9
**Labels:** `frontend`, `phase-2`, `sprint-9`

## Context (read before starting)

* `prd/PRD.md` §4.1 — Client dashboard: total billing, total cost, aggregate margin
* `fsd/FSD.md` §7.5 — Client-level aggregation

**As a** CEO/Finance user, **I want** financial metrics on the client detail page **so that** client relationship profitability is visible.

## Acceptance Criteria

- [ ] Financial section on client detail page (CEO/CTO/Finance only)
- [ ] Total Active Resources Deployed
- [ ] Total Monthly Billing (INR) — projected
- [ ] Total Actual Revenue (INR)
- [ ] Total Cost (INR)
- [ ] Aggregate Margin (INR + %)
- [ ] Revenue by project breakdown table
- [ ] Section hidden for unauthorized roles

## Out of Scope

* Client revenue history/trends
* Client-level invoicing summary

**Depends On:** EP-14 Story 5, EP-2 Story 5
