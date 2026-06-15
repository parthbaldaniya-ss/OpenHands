# EP-5: Allocation & Assignment Tracking

Core assignment entity with allocation/billability model, shadow resources, auto-release job, designation resolution, and over-allocation warnings.

**Sprint:** 4 | **Stories:** 10 | **SP:** 27
**Spec refs:** `fsd/FSD.md` §2.7, §6.1, §8, §11, `prd/PRD.md` §4.3, §5

---

## Story 1: Assignment database schema

**Size:** S (2 pts) | **Priority:** P0 — Blocker | **Sprint:** 4
**Labels:** `database`, `phase-1`, `sprint-4`, `must-have`

## Context (read before starting)

* `fsd/FSD.md` §2.7 — Assignment entity with 15 fields, ENUMs, constraints

**As a** developer, **I want** the Assignment table created **so that** resource-to-project mappings can be tracked.

## Acceptance Criteria

- [ ] Migration creates `assignment` table with all fields from FSD §2.7
- [ ] ENUM: status (ACTIVE, RELEASED, AUTO_RELEASED)
- [ ] FK constraints: project_id → project, resource_id → resource
- [ ] billing_rate column present (nullable, Phase 2)
- [ ] Indexes on project_id, resource_id, status, start_date, end_date
- [ ] No unique constraint on (project_id, resource_id) — multiple assignments possible but only one ACTIVE per pair
- [ ] Migration is reversible

## Out of Scope

* billing_rate population (Phase 2)

**Depends On:** EP-3 Story 1 (Project schema), EP-4 Story 1 (Resource schema)

---

## Story 2: Assignment CRUD API with all validations

**Size:** L (5 pts) | **Priority:** P1 — Critical | **Sprint:** 4
**Labels:** `backend`, `phase-1`, `sprint-4`, `must-have`

## Context (read before starting)

* `fsd/FSD.md` §2.7 — Assignment entity definition
* `fsd/FSD.md` §11 — 7 assignment validation rules
* `fsd/FSD.md` §14 — Edge cases for assignments

**As a** project manager, **I want** to assign resources to projects with allocation percentages **so that** resource utilization is tracked accurately.

## Acceptance Criteria

- [ ] GET /api/projects/:projectId/assignments — list assignments for a project
- [ ] GET /api/resources/:resourceId/assignments — list assignments for a resource
- [ ] POST /api/assignments — create with project_id, resource_id, allocation_pct (1-100), billability_pct (0-100), is_shadow, project_designation, project_expertise, start_date, end_date
- [ ] PUT /api/assignments/:id — update allocation, billability, dates, designation, expertise
- [ ] Validation: billability_pct ≤ allocation_pct → error "Billability cannot exceed allocation percentage"
- [ ] Validation: is_shadow = true AND billability_pct > 0 → error "Shadow resources cannot have billability"
- [ ] Validation: end_date ≤ start_date → error "End date must be after start date"
- [ ] Validation: duplicate active assignment (same resource+project) → error "Resource already has an active assignment on this project"
- [ ] Validation: project.status ≠ ACTIVE → error "Cannot create assignment on a non-active project"
- [ ] Validation: allocation_pct < 1 or > 100 → error "Allocation must be between 1% and 100%"
- [ ] Over-allocation (total > 100%): WARNING response (not blocking) "This will bring total allocation to {X}%"
- [ ] start_date in future: valid, ACTIVE status

## Out of Scope

* billing_rate assignment (Phase 2)
* Auto-release logic (separate story)
* Release/status transitions (separate story)

**Depends On:** Story 1, EP-1 (Auth)

---

## Story 3: Assignment lifecycle — RELEASED/AUTO_RELEASED transitions

**Size:** M (3 pts) | **Priority:** P1 — Critical | **Sprint:** 4
**Labels:** `backend`, `phase-1`, `sprint-4`, `must-have`

## Context (read before starting)

* `fsd/FSD.md` §6.1 — Assignment lifecycle state machine
* `fsd/FSD.md` §14 — Edge cases: PM extends end_date after auto-release, same resource reassigned

**As a** project manager, **I want** to manually release assignments and understand auto-release behavior **so that** resource allocation stays current.

## Acceptance Criteria

- [ ] PATCH /api/assignments/:id/release — manual release:
  - status → RELEASED
  - released_at = now()
  - Recalculate resource total allocation
  - If before end_date, log as early release in audit
- [ ] Cannot release an already RELEASED or AUTO_RELEASED assignment
- [ ] Cannot modify a RELEASED/AUTO_RELEASED assignment (return 400: "Cannot modify released assignment. Create new assignment.")
- [ ] Same resource can be re-assigned after release (if previous is RELEASED/AUTO_RELEASED)
- [ ] One ACTIVE assignment per resource per project enforced
- [ ] Audit logged for all status transitions

## Out of Scope

* Auto-release job (separate story)

**Depends On:** Story 2

---

## Story 4: Auto-release scheduled job

**Size:** M (3 pts) | **Priority:** P1 — Critical | **Sprint:** 4
**Labels:** `backend`, `infrastructure`, `phase-1`, `sprint-4`, `must-have`

## Context (read before starting)

* `fsd/FSD.md` §8 — Auto-release logic specification
* `fsd/FSD.md` §14 — Edge case: extension on release day

**As a** system, **I want** a daily job that auto-releases expired assignments **so that** allocations are kept accurate without manual intervention.

## Acceptance Criteria

- [ ] Scheduled job runs daily (midnight IST)
- [ ] Processes all assignments where: status = ACTIVE AND end_date IS NOT NULL AND end_date ≤ today
- [ ] For each: set status = AUTO_RELEASED, released_at = end_date 23:59:59
- [ ] Creates alert (type: ASSIGNMENT_AUTO_RELEASED) for PM and DM
- [ ] Inserts audit_log entry for each release
- [ ] Recalculates resource total allocation
- [ ] Idempotent: safe to re-run (skips already released)
- [ ] If PM extended end_date before job runs: job skips (end_date now in future)
- [ ] Job failures for individual records don't block processing of others
- [ ] Job execution logged (start time, records processed, success/failure count)

## Out of Scope

* Alert notification UI (Phase 3)

**Depends On:** Story 2, Story 3

---

## Story 5: Assignment access control with portfolio scoping

**Size:** S (2 pts) | **Priority:** P1 — Critical | **Sprint:** 4
**Labels:** `backend`, `phase-1`, `sprint-4`, `must-have`

## Context (read before starting)

* `fsd/FSD.md` §10 — Scope rules for assignment data
* `prd/PRD.md` §6 — Allocation and billability access matrix

**As a** system, **I want** assignment data scoped to user roles **so that** allocation information is appropriately restricted.

## Acceptance Criteria

- [ ] CEO/CTO: view/edit all assignments
- [ ] DM: view/edit assignments on projects where dm_id = self
- [ ] PM: view/edit assignments on projects where pm_id = self
- [ ] Finance: view all assignments (no edit)
- [ ] HR: view assignments (no edit, no billability/shadow data)
- [ ] Engineer: view own assignments only
- [ ] billability_pct hidden from HR and Engineer
- [ ] is_shadow hidden from HR and Engineer

## Out of Scope

* billing_rate restrictions (Phase 2)

**Depends On:** Story 2, EP-1 Story 4

---

## Story 6: Designation resolution logic — Fallback from assignment to resource

**Size:** S (2 pts) | **Priority:** P1 — Critical | **Sprint:** 4
**Labels:** `backend`, `phase-1`, `sprint-4`, `must-have`

## Context (read before starting)

* `fsd/FSD.md` §2.7 — project_designation, project_expertise nullable fields
* `fsd/FSD.md` §11 — Designation Resolution fallback rule

**As a** system, **I want** to resolve designations using assignment-level overrides with resource-level fallbacks **so that** project-specific roles are displayed correctly.

## Acceptance Criteria

- [ ] All API responses show resolved designation: assignment.project_designation if set, else resource.designation
- [ ] Same fallback for expertise: assignment.project_expertise if set, else resource.technical_expertise
- [ ] Search and filter endpoints use resolved values
- [ ] List views show resolved values
- [ ] NULL project_designation defaults to resource.designation in all contexts

## Out of Scope

* UI display (handled in assignment UI stories)

**Depends On:** Story 2

---

## Story 7: Assignment list view — Per project with all columns

**Size:** M (3 pts) | **Priority:** P1 — Critical | **Sprint:** 4
**Labels:** `frontend`, `phase-1`, `sprint-4`, `must-have`

## Context (read before starting)

* `fsd/FSD.md` §9 — Project Detail View → Resource Assignments section
* `fsd/FSD.md` §2.7 — Assignment fields

**As a** project manager, **I want** to see all resource assignments on my project **so that** I can manage the project team.

## Acceptance Criteria

- [ ] Table columns: Resource Name, Designation (resolved), Allocation %, Billability % (if authorized), Shadow (badge, if authorized), Start Date, End Date, Status
- [ ] Sortable by name, allocation, status
- [ ] Filter by status (Active, Released, All)
- [ ] Total allocation summary row
- [ ] Status badges: Active (green), Released (gray), Auto-Released (orange)
- [ ] Over-allocation warning icon next to resource name if total > 100%
- [ ] Row actions: Edit, Release (for ACTIVE only)

## Out of Scope

* Billing rate column (Phase 2)
* Drag-and-drop allocation

**Depends On:** Story 2, EP-3 Story 6

---

## Story 8: Assignment create/edit form — Allocation, billability, shadow toggle

**Size:** M (3 pts) | **Priority:** P1 — Critical | **Sprint:** 4
**Labels:** `frontend`, `phase-1`, `sprint-4`, `must-have`

## Context (read before starting)

* `fsd/FSD.md` §2.7 — Assignment entity fields
* `fsd/FSD.md` §11 — Validation rules

**As a** project manager, **I want** a form to assign resources to projects **so that** I can manage team composition.

## Acceptance Criteria

- [ ] Resource dropdown: searchable, shows only active resources
- [ ] Allocation % input (1-100, required)
- [ ] Billability % input (0-100, required, constrained ≤ allocation)
- [ ] Shadow toggle: when enabled, billability auto-sets to 0 and disables
- [ ] Project Designation (optional): override for this project
- [ ] Project Expertise (optional): override for this project
- [ ] Start Date (required), End Date (optional)
- [ ] Client-side validation matching all server-side rules
- [ ] Over-allocation warning shown inline (not blocking)
- [ ] Edit mode: pre-populates, resource field is read-only
- [ ] Success/error feedback

## Out of Scope

* Billing rate field (Phase 2)
* Bulk assignments

**Depends On:** Story 2

---

## Story 9: Over-allocation warning UI

**Size:** S (2 pts) | **Priority:** P2 — Major | **Sprint:** 4
**Labels:** `frontend`, `phase-1`, `sprint-4`

## Context (read before starting)

* `fsd/FSD.md` §2.7 — "System does NOT hard-block >100% total allocation. Raises over-allocation alert instead."

**As a** project manager, **I want** to see a warning when a resource is over-allocated **so that** I can make informed decisions.

## Acceptance Criteria

- [ ] In assignment form: when allocation would bring total > 100%, show yellow warning with total value
- [ ] In resource list: allocation column shows red when total > 100%
- [ ] In resource detail: allocation summary shows warning state
- [ ] Warning does not block form submission
- [ ] Warning text: "This will bring total allocation to {X}%"

## Out of Scope

* Over-allocation alert notifications (Phase 3)
* Historical over-allocation tracking

**Depends On:** Story 7, Story 8

---

## Story 10: Assignment audit logging

**Size:** XS (1 pt) | **Priority:** P2 — Major | **Sprint:** 4
**Labels:** `backend`, `phase-1`, `sprint-4`

## Context (read before starting)

* `fsd/FSD.md` §13 — Assignment: ALL fields tracked

**As a** system, **I want** all assignment changes logged **so that** allocation history is fully traceable.

## Acceptance Criteria

- [ ] CREATE logged with all field values
- [ ] UPDATE logged per changed field: allocation_pct, billability_pct, is_shadow, project_designation, project_expertise, start_date, end_date
- [ ] Status transitions (RELEASED, AUTO_RELEASED) logged with old/new status
- [ ] changed_by captured from session (or "SYSTEM" for auto-release job)

## Out of Scope

* billing_rate changes (Phase 2)

**Depends On:** Story 2, EP-9
