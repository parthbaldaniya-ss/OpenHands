# EP-7: Resource Availability

Public resource availability view with bench, partial availability, upcoming releases, and fully allocated sections — visible to ALL users including engineers.

**Sprint:** 5 | **Stories:** 3 | **SP:** 10
**Spec refs:** `fsd/FSD.md` §9 (Resource Availability View), `prd/PRD.md` §4.3

---

## Story 1: Resource availability API — Bench, partial, releasing soon

**Size:** M (3 pts) | **Priority:** P1 — Critical | **Sprint:** 5
**Labels:** `backend`, `phase-1`, `sprint-5`, `must-have`

## Context (read before starting)

* `fsd/FSD.md` §9 — Resource Availability View: 4 sections
* `fsd/FSD.md` §10 — Resource availability visible to ALL including engineers
* `fsd/FSD.md` §7.1 — Utilization calculations

**As a** system, **I want** an API that categorizes resources by availability **so that** the availability view has correct data.

## Acceptance Criteria

- [ ] GET /api/resources/availability — returns categorized data
- [ ] **Bench** (total allocation = 0%): resource name, designation, expertise, days_on_bench, tags
  - days_on_bench = today - max(released_at) of last assignment, or date_of_joining if never assigned
- [ ] **Partially Available** (0 < total allocation < 100%): name, total allocation %, spare capacity %, project names
- [ ] **Releasing Soon** (have end_date within filter window): name, project, allocation %, release date, days remaining
  - Supports filters: 30/60/90 days
- [ ] **Fully Allocated** (total allocation ≥ 100%): name, total allocation %, project names
- [ ] Only active resources included
- [ ] Accessible to ALL roles (including engineers)
- [ ] Project names visible but NOT billing rates, billability, shadow status, or CTC

## Out of Scope

* Availability forecasting with auto-release projection (Phase 3)
* Financial data in availability view

**Depends On:** EP-5 (Assignments exist), EP-6 Story 1 (Utilization calc)

---

## Story 2: Resource availability view — All four sections

**Size:** L (5 pts) | **Priority:** P1 — Critical | **Sprint:** 5
**Labels:** `frontend`, `phase-1`, `sprint-5`, `must-have`

## Context (read before starting)

* `fsd/FSD.md` §9 — Resource Availability View specification with 4 sections
* `prd/PRD.md` §4.3 — Visible to all users

**As a** team member, **I want** to see who is available, who is releasing soon, and who is on bench **so that** I can understand resource availability across the organization.

## Acceptance Criteria

- [ ] **Bench** section: cards or table with resource name, designation, expertise, days on bench, tags
- [ ] **Partially Available** section: table with name, total allocation %, spare capacity %, project names
- [ ] **Releasing Soon** section: table with name, project, allocation %, release date, days remaining
  - Toggle filters: 30 / 60 / 90 days (default 30)
- [ ] **Fully Allocated** section: table with name, total allocation %, project names
- [ ] Section headers with count badges
- [ ] Clickable resource names → resource detail
- [ ] Clickable project names → project detail
- [ ] Responsive layout
- [ ] Accessible via main navigation for all roles
- [ ] No financial data shown (no CTC, billing rate, billability, shadow)

## Out of Scope

* Drag-and-drop resource allocation
* Export to CSV
* Auto-release projection indicators

**Depends On:** Story 1

---

## Story 3: Bench detection and tracking

**Size:** S (2 pts) | **Priority:** P1 — Critical | **Sprint:** 5
**Labels:** `backend`, `phase-1`, `sprint-5`, `must-have`

## Context (read before starting)

* `fsd/FSD.md` §7.6 — Bench cost: bench start = max(released_at) or date_of_joining
* `prd/PRD.md` §5 — Bench definition

**As a** system, **I want** to detect bench resources and track bench duration **so that** bench visibility is accurate.

## Acceptance Criteria

- [ ] Resource is "on bench" when: sum of allocation_pct across ACTIVE assignments = 0%
- [ ] Bench start date = max(released_at) of last released assignment, or date_of_joining if never assigned
- [ ] Days on bench = today - bench_start_date
- [ ] Bench detection recalculated when:
  - Assignment released or auto-released
  - New assignment created
  - Assignment allocation changed
- [ ] Only active resources considered

## Out of Scope

* Bench cost calculation (Phase 2)
* Bench duration alerts (Phase 3)

**Depends On:** EP-5 (Assignments exist)
