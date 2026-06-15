# EP-17: Bench & Availability Forecasting

Bench management dashboard with cost visibility, 30/60/90-day availability forecasting auto-release-aware, and partial availability identification.

**Sprint:** 11 | **Stories:** 3 | **SP:** 8
**Spec refs:** `fsd/FSD.md` §7.6, §9, `prd/PRD.md` §7 (Phase 3)

---

## Story 1: Bench management dashboard — Cost, duration, list

**Size:** M (3 pts) | **Priority:** P2 — Major | **Sprint:** 11
**Labels:** `backend`, `frontend`, `phase-3`, `sprint-11`, `must-have`

## Context (read before starting)

* `fsd/FSD.md` §7.6 — Bench Cost: daily = loaded_cost_monthly / 22, total = daily × days_on_bench
* `prd/PRD.md` §7 — Phase 3: bench list with cost, duration tracking

**As a** CTO, **I want** a bench management dashboard **so that** bench cost and duration are visible in one place.

## Acceptance Criteria

- [ ] Bench dashboard page (accessible to CEO, CTO, DM, HR)
- [ ] Current bench list: resource name, designation, expertise, days on bench, daily cost (INR), total bench cost (INR), tags
- [ ] Summary cards: bench count, total daily cost, total accumulated cost
- [ ] Sort by days on bench, cost, name
- [ ] Filter by designation, tags
- [ ] Bench duration highlighted: green (<7d), yellow (7-14d), red (>14d)
- [ ] Click resource → resource detail
- [ ] Cost columns visible only to CEO/CTO/Finance

## Out of Scope

* Bench resource recommendations
* What-if planning

**Depends On:** EP-7 Story 3 (Bench detection), EP-14 Story 4 (Bench cost)

---

## Story 2: Availability forecasting — 30/60/90 day release view

**Size:** M (3 pts) | **Priority:** P2 — Major | **Sprint:** 11
**Labels:** `backend`, `frontend`, `phase-3`, `sprint-11`, `must-have`

## Context (read before starting)

* `prd/PRD.md` §7 — Phase 3: 30/60/90 day upcoming release view, auto-release aware
* `fsd/FSD.md` §9 — Releasing Soon section

**As a** DM, **I want** to see which resources will be available in the next 30/60/90 days **so that** I can plan ahead.

## Acceptance Criteria

- [ ] Availability forecasting page/section
- [ ] Time horizon toggles: 30 / 60 / 90 days
- [ ] Upcoming releases table: resource name, project, current allocation %, release date, days remaining, projected bench date
- [ ] Auto-release-aware: includes assignments with end_date in the selected window
- [ ] Shows resulting capacity after release (e.g., "Will free 50% capacity on June 30")
- [ ] Groupable by project or by date
- [ ] Summary: N resources releasing, total capacity freeing
- [ ] Timeline view (optional): visual timeline showing releases
- [ ] Accessible to DM, CTO, CEO, HR

## Out of Scope

* What-if resource planner
* Demand forecasting

**Depends On:** EP-7 Story 1 (Availability API)

---

## Story 3: Partial availability identification

**Size:** S (2 pts) | **Priority:** P2 — Major | **Sprint:** 11
**Labels:** `backend`, `phase-3`, `sprint-11`

## Context (read before starting)

* `fsd/FSD.md` §9 — Partially Available section: 0 < total allocation < 100%

**As a** DM, **I want** to identify resources with spare capacity **so that** I can maximize utilization.

## Acceptance Criteria

- [ ] API endpoint or filter: resources with 0 < total_allocation < 100%
- [ ] Shows: resource name, current allocation %, spare capacity %, current projects, skills/tags
- [ ] Sortable by spare capacity (most available first)
- [ ] Filterable by designation, tags, expertise
- [ ] Integrated into availability forecasting page
- [ ] Considers future releases: if a resource will have more capacity after a release, show projected spare capacity

## Out of Scope

* Skill matching recommendations
* Auto-allocation suggestions

**Depends On:** EP-7 Story 1
