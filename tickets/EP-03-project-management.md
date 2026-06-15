# EP-3: Project Management

Project CRUD for all three types (Fixed Price, Time & Material, Client Onboarding), status lifecycle, portfolio-scoped access, and type-specific views.

**Sprint:** 3 | **Stories:** 9 | **SP:** 26
**Spec refs:** `fsd/FSD.md` §2.6, §6.4, `prd/PRD.md` §4.2

---

## Story 1: Project database schema

**Size:** S (2 pts) | **Priority:** P0 — Blocker | **Sprint:** 3
**Labels:** `database`, `phase-1`, `sprint-3`, `must-have`

## Context (read before starting)

* `fsd/FSD.md` §2.6 — Project entity with 14 fields, 3 ENUMs

**As a** developer, **I want** the Project table created with type-specific constraints **so that** all three project types can be stored.

## Acceptance Criteria

- [ ] Migration creates `project` table with all fields from FSD §2.6
- [ ] ENUM types: type (FIXED_PRICE, TIME_AND_MATERIAL, CLIENT_ONBOARDING), status (ACTIVE, COMPLETED, ON_HOLD, CANCELLED)
- [ ] FK constraints to client, dm (resource), pm (resource)
- [ ] Indexes on client_id, dm_id, pm_id, status, type
- [ ] contract_value column present (used in Phase 2 for FP revenue)
- [ ] billing_currency defaults to 'INR'
- [ ] Migration is reversible

## Out of Scope

* Milestone table (EP-11)
* Invoice table (EP-12)

**Depends On:** EP-2 Story 1 (Client schema), EP-4 Story 1 (Resource schema)

---

## Story 2: Project CRUD API — All three project types with validations

**Size:** L (5 pts) | **Priority:** P1 — Critical | **Sprint:** 3
**Labels:** `backend`, `phase-1`, `sprint-3`, `must-have`

## Context (read before starting)

* `fsd/FSD.md` §2.6 — Project entity definition
* `prd/PRD.md` §4.2.1–4.2.3 — Type-specific requirements
* `fsd/FSD.md` §11 — Validation rules

**As a** project manager, **I want** to create and manage projects of any type **so that** all project information is captured correctly.

## Acceptance Criteria

- [ ] GET /api/projects — paginated list with filters: type, status, client_id, dm_id, pm_id
- [ ] GET /api/projects/:id — single project with client name, DM name, PM name, assignment count
- [ ] POST /api/projects — create with type-specific validations:
  - FIXED_PRICE: contract_value required
  - TIME_AND_MATERIAL: contract_end_date required
  - CLIENT_ONBOARDING: contract_end_date required
- [ ] PUT /api/projects/:id — update with same validations
- [ ] billing_currency validated as ISO 4217 code (USD, EUR, GBP, INR, etc.)
- [ ] dm_id and pm_id must reference active resources
- [ ] worklog_enabled toggle works
- [ ] Consistent error responses

## Out of Scope

* Project status transitions (separate story)
* Financial calculations
* Milestone and invoice management

**Depends On:** Story 1, EP-1 (Auth)

---

## Story 3: Project status transitions — ACTIVE/COMPLETED/ON_HOLD/CANCELLED

**Size:** M (3 pts) | **Priority:** P1 — Critical | **Sprint:** 3
**Labels:** `backend`, `phase-1`, `sprint-3`, `must-have`

## Context (read before starting)

* `fsd/FSD.md` §6.4 — Project status state machine
* `fsd/FSD.md` §14 — Edge cases: completed with unpaid invoices

**As a** delivery manager, **I want** to transition project status through defined states **so that** project lifecycle is tracked accurately.

## Acceptance Criteria

- [ ] PATCH /api/projects/:id/status — accepts new status
- [ ] Valid transitions: ACTIVE→COMPLETED, ACTIVE⇄ON_HOLD, ACTIVE→CANCELLED
- [ ] Invalid transitions return 400 with descriptive message
- [ ] When COMPLETED or CANCELLED: all ACTIVE assignments auto-released with status=RELEASED, released_at=now()
- [ ] No new assignments can be created on COMPLETED/CANCELLED projects
- [ ] ON_HOLD allows existing assignments but no new ones
- [ ] Project completed with unpaid invoices: allowed
- [ ] Audit logged for status changes

## Out of Scope

* Financial impact calculations on status change

**Depends On:** Story 2

---

## Story 4: Project access control — DM/PM portfolio scoping

**Size:** S (2 pts) | **Priority:** P1 — Critical | **Sprint:** 3
**Labels:** `backend`, `phase-1`, `sprint-3`, `must-have`

## Context (read before starting)

* `fsd/FSD.md` §10 — Scope rules: DM sees project.dm_id=self, PM sees project.pm_id=self
* `prd/PRD.md` §6 — Access matrix for project details

**As a** delivery manager, **I want** to see only projects in my portfolio **so that** data access is appropriately scoped.

## Acceptance Criteria

- [ ] CEO/CTO: see all projects
- [ ] DM: see only projects where dm_id = current user's resource_id
- [ ] PM: see only projects where pm_id = current user's resource_id
- [ ] Finance: see all projects (financial data only)
- [ ] HR: see all projects (profiles only, no financials)
- [ ] Engineer: see only projects where they have an ACTIVE assignment
- [ ] Scope applied to both list and detail endpoints
- [ ] DM change on project: new DM gains visibility, old DM loses it

## Out of Scope

* Field-level restrictions for financial data (Phase 2)

**Depends On:** Story 2, EP-1 Story 4 (Access middleware)

---

## Story 5: Project list view — Filterable by type, status, client

**Size:** M (3 pts) | **Priority:** P1 — Critical | **Sprint:** 3
**Labels:** `frontend`, `phase-1`, `sprint-3`, `must-have`

## Context (read before starting)

* `prd/PRD.md` §4.2 — Project as operational unit
* `fsd/FSD.md` §2.6 — Project entity fields

**As a** delivery manager, **I want** to view all my projects in a filterable list **so that** I can quickly navigate to any project.

## Acceptance Criteria

- [ ] Table columns: Name, Client, Type (badge), Status (badge), DM, PM, Billing Currency, Resource Count, Start Date
- [ ] Type filter: FP, T&M, Onboarding (multi-select)
- [ ] Status filter: Active, Completed, On Hold, Cancelled
- [ ] Client filter dropdown
- [ ] Search by project name
- [ ] Sortable columns
- [ ] Pagination
- [ ] Row click navigates to project detail

## Out of Scope

* Financial columns (Phase 2)
* Dashboard widgets

**Depends On:** Story 2

---

## Story 6: Project detail view — Type-specific sections

**Size:** L (5 pts) | **Priority:** P1 — Critical | **Sprint:** 3
**Labels:** `frontend`, `phase-1`, `sprint-3`, `must-have`

## Context (read before starting)

* `fsd/FSD.md` §9 — Project Detail View specification
* `prd/PRD.md` §4.2.1–4.2.3 — Type-specific attributes

**As a** project manager, **I want** a comprehensive project detail page showing all relevant sections **so that** I have full visibility into project status.

## Acceptance Criteria

- [ ] Header: project name, client, type badge, status badge, billing currency, DM, PM
- [ ] Resource Assignments section: table with name, designation (with fallback), allocation %, billability %, shadow flag, dates, status
- [ ] Add/Edit/Release assignment actions (PM+)
- [ ] Type-specific sections: Milestones tab (FP only — placeholder for Phase 2), Contract end date (T&M/Onboarding)
- [ ] Worklog tab: visible only if worklog_enabled, shows resource/date/hours/note table
- [ ] Edit project button (authorized roles)
- [ ] Status transition buttons (based on valid transitions)
- [ ] Notes section

## Out of Scope

* Non-human costs section (Phase 2)
* Financial summary section (Phase 2)
* Invoice section (Phase 2)

**Depends On:** Story 2, EP-5 (Assignments)

---

## Story 7: Project create/edit form — Type-specific fields

**Size:** M (3 pts) | **Priority:** P1 — Critical | **Sprint:** 3
**Labels:** `frontend`, `phase-1`, `sprint-3`, `must-have`

## Context (read before starting)

* `fsd/FSD.md` §2.6 — Project entity fields and constraints
* `prd/PRD.md` §4.2 — Project type descriptions

**As a** delivery manager, **I want** a project creation form that adapts to project type **so that** the correct fields are captured.

## Acceptance Criteria

- [ ] Form fields: Name (required), Client dropdown (required), Type dropdown (required), Billing Currency, Start Date, DM dropdown (required), PM dropdown (required), Worklog Enabled toggle, Notes
- [ ] Type-specific fields appear/hide based on selection:
  - FIXED_PRICE: Contract Value (required)
  - TIME_AND_MATERIAL: Contract End Date (required)
  - CLIENT_ONBOARDING: Contract End Date (required)
- [ ] Client-side validations match server-side
- [ ] DM/PM dropdowns load active resources
- [ ] Edit mode pre-populates all fields; type is read-only on edit
- [ ] Success toast with redirect to project detail

## Out of Scope

* Billing rate assignment (Phase 2)
* Milestone setup during creation

**Depends On:** Story 2

---

## Story 8: Project status transition UI

**Size:** S (2 pts) | **Priority:** P1 — Critical | **Sprint:** 3
**Labels:** `frontend`, `phase-1`, `sprint-3`, `must-have`

## Context (read before starting)

* `fsd/FSD.md` §6.4 — Project status state machine and valid transitions

**As a** delivery manager, **I want** status transition buttons on the project detail page **so that** I can manage project lifecycle visually.

## Acceptance Criteria

- [ ] Status badge shows current state with color coding
- [ ] Action buttons show only valid transitions (e.g., Active shows: Complete, Put On Hold, Cancel)
- [ ] Confirmation dialog for destructive transitions (Complete, Cancel) with warning about assignment releases
- [ ] UI updates immediately after successful transition
- [ ] Error toast if transition fails (e.g., server-side validation)

## Out of Scope

* Bulk status changes
* Scheduled transitions

**Depends On:** Story 3, Story 6

---

## Story 9: Project audit logging

**Size:** XS (1 pt) | **Priority:** P2 — Major | **Sprint:** 3
**Labels:** `backend`, `phase-1`, `sprint-3`

## Context (read before starting)

* `fsd/FSD.md` §13 — Tracked: status, contract_end_date, contract_value

**As a** system, **I want** all project changes logged **so that** a complete audit trail exists.

## Acceptance Criteria

- [ ] CREATE logged with all field values
- [ ] UPDATE logged per changed field: status, contract_end_date, contract_value, dm_id, pm_id
- [ ] Status transitions logged with old and new status
- [ ] changed_by captured from session

## Out of Scope

* Audit log viewer (Phase 3)

**Depends On:** Story 2, EP-9 (Audit service)
