# EP-6: Utilization Dashboards

Company-wide, per-DM, per-client, per-project, and per-resource utilization views with KPI cards and drill-down.

**Sprint:** 5 | **Stories:** 5 | **SP:** 16
**Spec refs:** `fsd/FSD.md` §7.1, §9 (Company Dashboard), `prd/PRD.md` §4.3 (Utilization Dashboards)

---

## Story 1: Utilization calculation engine — Company and per-resource

**Size:** M (3 pts) | **Priority:** P1 — Critical | **Sprint:** 5
**Labels:** `backend`, `phase-1`, `sprint-5`, `must-have`

## Context (read before starting)

* `fsd/FSD.md` §7.1 — Utilization formulas: Total Allocation, Billable Allocation, Utilization Rate, Company Utilization

**As a** system, **I want** accurate utilization calculations **so that** dashboards show correct data.

## Acceptance Criteria

- [ ] Total Allocation (resource) = SUM(allocation_pct) across all ACTIVE assignments
- [ ] Billable Allocation (resource) = SUM(billability_pct) where is_shadow = false
- [ ] Utilization Rate (resource) = Billable Allocation / 100 × 100%
- [ ] Company Utilization = SUM(all billable alloc) / (active_resource_count × 100) × 100%
- [ ] Only ACTIVE assignments with start_date ≤ today contribute
- [ ] Handles edge cases: no resources (0%), no assignments (0%), division by zero
- [ ] Calculation exposed as service layer for reuse across endpoints

## Out of Scope

* Historical utilization trends
* Financial utilization (revenue-weighted)

**Depends On:** EP-5 (Assignments exist)

---

## Story 2: Company dashboard — Data API with role scoping

**Size:** M (3 pts) | **Priority:** P2 — Major | **Sprint:** 5
**Labels:** `backend`, `phase-1`, `sprint-5`, `must-have`

## Context (read before starting)

* `fsd/FSD.md` §9 — Company Dashboard widgets specification
* `fsd/FSD.md` §10 — CEO/CTO see all data

**As a** CEO/CTO, **I want** a single API endpoint that returns all dashboard data **so that** the dashboard loads efficiently.

## Acceptance Criteria

- [ ] GET /api/dashboard/company — returns aggregated metrics
- [ ] Billable Utilization: company-wide percentage
- [ ] Bench Count: count + list of resource names with 0 ACTIVE assignments
- [ ] Shadow Allocation: count of shadow assignments + total allocation %
- [ ] Active Projects: count by type (FP, T&M, Onboarding)
- [ ] Upcoming Releases: assignments with end_date in next 30 days
- [ ] Overdue Milestones: count + list (planned_date < today AND status = PLANNED) — placeholder until Phase 2
- [ ] Role-scoped: CEO/CTO see all, DM sees portfolio, others restricted
- [ ] Response time < 2s for typical dataset (30-40 resources)

## Out of Scope

* Revenue summary (Phase 2)
* Financial widgets

**Depends On:** Story 1

---

## Story 3: Company dashboard — UI with KPI cards and widgets

**Size:** L (5 pts) | **Priority:** P2 — Major | **Sprint:** 5
**Labels:** `frontend`, `phase-1`, `sprint-5`, `must-have`

## Context (read before starting)

* `fsd/FSD.md` §9 — Company Dashboard specification with 7 widgets

**As a** CEO/CTO, **I want** a visual dashboard with key metrics **so that** I can assess company health at a glance.

## Acceptance Criteria

- [ ] Billable Utilization KPI card: large number with percentage
- [ ] Bench Count card: number with expandable list of bench resources
- [ ] Shadow Allocation card: count and total %
- [ ] Active Projects card: count with type breakdown (pie/donut chart or badges)
- [ ] Upcoming Releases widget: table with resource name, project, release date, days remaining
- [ ] Overdue Milestones widget: table or count card (placeholder until Phase 2)
- [ ] Responsive layout: cards grid, widgets below
- [ ] Loading states for each widget
- [ ] Drill-down links: bench resources → resource detail, projects → project list, upcoming releases → resource detail
- [ ] Auto-refresh interval (optional, e.g., every 5 minutes)

## Out of Scope

* Revenue vs Actual chart (Phase 2)
* Custom date range filters
* Export to PDF/CSV

**Depends On:** Story 2

---

## Story 4: Project-level utilization view

**Size:** M (3 pts) | **Priority:** P2 — Major | **Sprint:** 5
**Labels:** `frontend`, `phase-1`, `sprint-5`

## Context (read before starting)

* `fsd/FSD.md` §7.1 — Per-resource utilization
* `prd/PRD.md` §4.3 — Per-project utilization view

**As a** project manager, **I want** to see utilization metrics for my project **so that** I understand resource efficiency.

## Acceptance Criteria

- [ ] Utilization section on project detail page
- [ ] Total allocation across all assignments
- [ ] Total billable allocation (non-shadow)
- [ ] Resource count (total, billable, shadow)
- [ ] Per-resource utilization breakdown: name, allocation %, billability %, utilization rate
- [ ] Visual indicator: bar chart or progress bars per resource

## Out of Scope

* Financial metrics (Phase 2)
* Historical utilization trends

**Depends On:** Story 1, EP-3 Story 6

---

## Story 5: Per-DM portfolio utilization view

**Size:** S (2 pts) | **Priority:** P2 — Major | **Sprint:** 5
**Labels:** `frontend`, `phase-1`, `sprint-5`

## Context (read before starting)

* `prd/PRD.md` §4.3 — Per-DM utilization view

**As a** delivery manager, **I want** to see aggregated utilization across my portfolio **so that** I can identify under/over-utilized areas.

## Acceptance Criteria

- [ ] DM portfolio dashboard page or section
- [ ] Portfolio utilization: average across all DM's projects
- [ ] Per-project utilization table: project name, resource count, avg allocation, avg billability
- [ ] Bench resources in portfolio: resources assigned to DM's projects with spare capacity
- [ ] Accessible from main navigation for DM role

## Out of Scope

* Cross-DM comparison (CEO/CTO only)
* Financial portfolio metrics

**Depends On:** Story 1, Story 2
