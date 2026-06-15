# EP-4: Resource Management

Resource profiles with designations, technical expertise, tags, self-referencing reporting hierarchy, and access-controlled views.

**Sprint:** 2–3 | **Stories:** 8 | **SP:** 19
**Spec refs:** `fsd/FSD.md` §2.5, §14, `prd/PRD.md` §4.3

---

## Story 1: Resource & ResourceTag database schema

**Size:** S (2 pts) | **Priority:** P0 — Blocker | **Sprint:** 2
**Labels:** `database`, `phase-1`, `sprint-2`, `must-have`

## Context (read before starting)

* `fsd/FSD.md` §2.5 — Resource entity (10 fields) + ResourceTag join table

**As a** developer, **I want** the Resource and ResourceTag tables created **so that** employee data can be stored.

## Acceptance Criteria

- [ ] Migration creates `resource` table: id (UUID PK), employee_id (unique), name, designation, technical_expertise (nullable), date_of_joining, reporting_manager_id (self-ref FK, nullable), loaded_cost_monthly (nullable, Phase 2), is_active, created_at
- [ ] Migration creates `resource_tag` table: resource_id (FK), tag (STRING 100), composite PK on (resource_id, tag)
- [ ] Self-referencing FK on reporting_manager_id allows null (CEO)
- [ ] Indexes on employee_id, reporting_manager_id, is_active, designation
- [ ] Migration is reversible

## Out of Scope

* loaded_cost_monthly population (Phase 2)

**Depends On:** EP-1 Story 1

---

## Story 2: Resource CRUD API with tags management

**Size:** M (3 pts) | **Priority:** P1 — Critical | **Sprint:** 2
**Labels:** `backend`, `phase-1`, `sprint-2`, `must-have`

## Context (read before starting)

* `fsd/FSD.md` §2.5 — Resource and ResourceTag definitions
* `prd/PRD.md` §4.3 — Resource profile attributes and tags
* `fsd/FSD.md` §10 — Resource scope rules

**As a** HR manager, **I want** to create and manage resource profiles with tags **so that** all employee information is centralized.

## Acceptance Criteria

- [ ] GET /api/resources — paginated list with search by name/employee_id, filter by designation, is_active, tags
- [ ] GET /api/resources/:id — single resource with tags, reporting manager name, current assignments summary
- [ ] POST /api/resources — create with employee_id (required, unique), name, designation, expertise, date_of_joining, reporting_manager_id, tags array
- [ ] PUT /api/resources/:id — update profile fields + replace tags
- [ ] POST /api/resources/:id/tags — add individual tags
- [ ] DELETE /api/resources/:id/tags/:tag — remove individual tag
- [ ] employee_id uniqueness enforced
- [ ] reporting_manager_id must reference existing active resource or be null

## Out of Scope

* loaded_cost_monthly field (Phase 2)
* Deactivation logic (separate story)
* Assignment details (Assignment module)

**Depends On:** Story 1, EP-1 (Auth)

---

## Story 3: Resource access control and field-level restrictions

**Size:** S (2 pts) | **Priority:** P1 — Critical | **Sprint:** 2
**Labels:** `backend`, `phase-1`, `sprint-2`, `must-have`

## Context (read before starting)

* `fsd/FSD.md` §10 — Field-level restrictions: loaded_cost_monthly restricted to CEO/CTO/Finance
* `prd/PRD.md` §6 — Resource access matrix

**As a** system, **I want** resource data filtered by role **so that** sensitive information is protected.

## Acceptance Criteria

- [ ] CEO/CTO: full access to all resource data
- [ ] HR: full profile access, can edit profiles, no financial data
- [ ] DM: view resources on their projects
- [ ] PM: view resources on their projects
- [ ] Finance: view all resources with cost data
- [ ] Engineer: view own profile + resource availability (public view)
- [ ] loaded_cost_monthly returns null for non-authorized roles
- [ ] Scope filtering applied consistently on list and detail endpoints

## Out of Scope

* billing_rate restrictions (Phase 2)
* Per-user permission overrides (Phase 3)

**Depends On:** Story 2, EP-1 Story 4

---

## Story 4: Resource deactivation — Release all active assignments

**Size:** S (2 pts) | **Priority:** P1 — Critical | **Sprint:** 3
**Labels:** `backend`, `phase-1`, `sprint-3`, `must-have`

## Context (read before starting)

* `fsd/FSD.md` §14 — "Resource deactivated while assigned → All ACTIVE assignments released"

**As a** HR manager, **I want** resource deactivation to automatically release all assignments **so that** project allocations stay accurate.

## Acceptance Criteria

- [ ] PATCH /api/resources/:id/deactivate — sets is_active = false
- [ ] All ACTIVE assignments for this resource: status → RELEASED, released_at = now()
- [ ] Deactivated resources cannot receive new assignments
- [ ] Deactivated resources excluded from default list (filterable to include)
- [ ] Each released assignment audit logged
- [ ] Cannot deactivate resource if they are a DM or PM on active projects (warning, not block)
- [ ] Audit logged

## Out of Scope

* Reactivation flow
* Impact analysis before deactivation

**Depends On:** Story 2, EP-5 (Assignment exists)

---

## Story 5: Resource list view — Search, filter by designation/tags

**Size:** M (3 pts) | **Priority:** P1 — Critical | **Sprint:** 3
**Labels:** `frontend`, `phase-1`, `sprint-3`, `must-have`

## Context (read before starting)

* `prd/PRD.md` §4.3 — Resource profile attributes
* `fsd/FSD.md` §2.5 — Resource entity fields

**As a** delivery manager, **I want** to search and filter resources by skills and availability **so that** I can find the right people for projects.

## Acceptance Criteria

- [ ] Table columns: Employee ID, Name, Designation, Technical Expertise, Tags (chips), Total Allocation %, Status
- [ ] Search by name, employee ID
- [ ] Filter by designation, tags (multi-select), status
- [ ] Sortable columns
- [ ] Pagination
- [ ] Tags displayed as chips/badges
- [ ] Color-coded allocation: green (<80%), yellow (80-100%), red (>100%)
- [ ] Row click navigates to resource detail

## Out of Scope

* Loaded cost column (Phase 2)
* Availability forecasting (Phase 3)

**Depends On:** Story 2

---

## Story 6: Resource detail/profile view — Assignments, tags, availability

**Size:** M (3 pts) | **Priority:** P1 — Critical | **Sprint:** 3
**Labels:** `frontend`, `phase-1`, `sprint-3`, `must-have`

## Context (read before starting)

* `prd/PRD.md` §4.3 — Resource current assignments view
* `fsd/FSD.md` §9 — Views specifications

**As a** delivery manager, **I want** a resource profile page showing all assignments and availability **so that** I can make informed allocation decisions.

## Acceptance Criteria

- [ ] Header: name, employee ID, designation, technical expertise, date of joining
- [ ] Reporting manager link
- [ ] Tags section with add/remove capability (HR+)
- [ ] Current Assignments table: project name, client, allocation %, billability %, shadow flag, start/end date, status
- [ ] Total Allocation % summary (sum of all active)
- [ ] Availability indicator: Bench / Partially Available / Fully Allocated / Over-Allocated
- [ ] Edit button (HR+)
- [ ] Deactivate button with confirmation (HR+)

## Out of Scope

* Loaded cost display (Phase 2)
* Historical assignments
* Worklog summary

**Depends On:** Story 2, EP-5 (Assignments exist)

---

## Story 7: Resource create/edit form with tag management

**Size:** M (3 pts) | **Priority:** P1 — Critical | **Sprint:** 3
**Labels:** `frontend`, `phase-1`, `sprint-3`, `must-have`

## Context (read before starting)

* `fsd/FSD.md` §2.5 — Resource and ResourceTag fields

**As a** HR manager, **I want** a form to create and edit resource profiles with tags **so that** employee records are accurate.

## Acceptance Criteria

- [ ] Form fields: Employee ID (required, unique), Name (required), Designation (required), Technical Expertise, Date of Joining, Reporting Manager dropdown
- [ ] Tags input: type-ahead with existing tags suggestions, add new tags
- [ ] Employee ID uniqueness validated before submit
- [ ] Reporting Manager dropdown filtered to active resources
- [ ] Edit mode pre-populates all fields including tags
- [ ] Success toast with redirect to resource detail

## Out of Scope

* Loaded cost field (Phase 2)
* Bulk import

**Depends On:** Story 2

---

## Story 8: Resource audit logging

**Size:** XS (1 pt) | **Priority:** P2 — Major | **Sprint:** 3
**Labels:** `backend`, `phase-1`, `sprint-3`

## Context (read before starting)

* `fsd/FSD.md` §13 — Tracked: designation, loaded_cost, is_active

**As a** system, **I want** resource changes logged **so that** profile modifications are traceable.

## Acceptance Criteria

- [ ] CREATE logged
- [ ] UPDATE logged per changed field: designation, technical_expertise, reporting_manager_id, is_active
- [ ] Tag additions/removals logged
- [ ] changed_by captured from session

## Out of Scope

* loaded_cost changes (Phase 2)

**Depends On:** Story 2, EP-9
