# EP-2: Client Management

Full client profiles with CRUD, multi-project support, deactivation logic, and client dashboard.

**Sprint:** 2 | **Stories:** 7 | **SP:** 15
**Spec refs:** `fsd/FSD.md` §2.4, §14, `prd/PRD.md` §4.1

---

## Story 1: Client database schema

**Size:** XS (1 pt) | **Priority:** P0 — Blocker | **Sprint:** 2
**Labels:** `database`, `phase-1`, `sprint-2`, `must-have`

## Context (read before starting)

* `fsd/FSD.md` §2.4 — Client entity with 10 fields

**As a** developer, **I want** the Client table created **so that** client data can be stored and queried.

## Acceptance Criteria

- [ ] Migration creates `client` table: id (UUID PK), name (unique, not null), industry, contact_name, contact_email, contact_phone, engagement_start_date, notes (TEXT), is_active (default true), created_at
- [ ] Index on name and is_active
- [ ] Migration is reversible

## Out of Scope

* Client CRUD API
* Client dashboard aggregations

**Depends On:** EP-1 Story 1 (auth schema)

---

## Story 2: Client CRUD API with validations and access control

**Size:** M (3 pts) | **Priority:** P1 — Critical | **Sprint:** 2
**Labels:** `backend`, `phase-1`, `sprint-2`, `must-have`

## Context (read before starting)

* `fsd/FSD.md` §2.4 — Client entity definition
* `fsd/FSD.md` §10 — Client access: CEO/CTO full, DM/PM own portfolio, Finance/HR view
* `prd/PRD.md` §4.1 — Client profile capabilities

**As a** CEO/CTO, **I want** to create, view, update, and manage client records **so that** all client information is centralized.

## Acceptance Criteria

- [ ] GET /api/clients — paginated list with search by name, filter by industry, is_active
- [ ] GET /api/clients/:id — single client with project count and summary
- [ ] POST /api/clients — create with name (required), industry, contact info, engagement date, notes
- [ ] PUT /api/clients/:id — update all editable fields
- [ ] Name uniqueness validated
- [ ] Role-based access enforced: CEO/CTO can edit, DM/PM view own portfolio, Finance/HR view only
- [ ] Consistent error responses with descriptive messages

## Out of Scope

* Client deactivation (separate story)
* Financial aggregations (Phase 2)
* Client history/trends

**Depends On:** Story 1, EP-1 (Auth middleware)

---

## Story 3: Client deactivation handling — Block if active projects exist

**Size:** S (2 pts) | **Priority:** P1 — Critical | **Sprint:** 2
**Labels:** `backend`, `phase-1`, `sprint-2`, `must-have`

## Context (read before starting)

* `fsd/FSD.md` §14 — "Client deactivated with active projects → Block"
* `fsd/FSD.md` §2.4 — is_active flag

**As a** CEO/CTO, **I want** the system to prevent deactivating a client with active projects **so that** data integrity is maintained.

## Acceptance Criteria

- [ ] PATCH /api/clients/:id/deactivate — soft delete (is_active = false)
- [ ] If client has any projects with status = ACTIVE or ON_HOLD → return 400: "Complete or cancel all projects first."
- [ ] If all projects are COMPLETED/CANCELLED → allow deactivation
- [ ] Deactivated clients excluded from default list (filterable to include)
- [ ] Audit logged

## Out of Scope

* Reactivation flow
* Cascade deletion

**Depends On:** Story 2

---

## Story 4: Client list view — Filterable, sortable table

**Size:** M (3 pts) | **Priority:** P1 — Critical | **Sprint:** 2
**Labels:** `frontend`, `phase-1`, `sprint-2`, `must-have`

## Context (read before starting)

* `prd/PRD.md` §4.1 — Multi-project view, client dashboard
* `fsd/FSD.md` §2.4 — Client entity fields

**As a** delivery manager, **I want** to see all clients in a searchable, filterable table **so that** I can quickly find client information.

## Acceptance Criteria

- [ ] Table columns: Name, Industry, Contact, Engagement Start Date, Active Projects Count, Status
- [ ] Sortable by name, engagement date, project count
- [ ] Search by client name
- [ ] Filter by industry, status (active/inactive)
- [ ] Pagination (25 per page default)
- [ ] Empty state message when no clients exist
- [ ] Row click navigates to client detail view

## Out of Scope

* Financial columns (Phase 2)
* Client dashboard widgets

**Depends On:** Story 2

---

## Story 5: Client detail view — Profile with projects summary

**Size:** M (3 pts) | **Priority:** P1 — Critical | **Sprint:** 2
**Labels:** `frontend`, `phase-1`, `sprint-2`, `must-have`

## Context (read before starting)

* `prd/PRD.md` §4.1 — Client dashboard: resources deployed, project count by type
* `fsd/FSD.md` §2.4 — Client entity
* `fsd/FSD.md` §3 — Client → Project (1:N)

**As a** delivery manager, **I want** a client detail page showing profile info and linked projects **so that** I have complete visibility into a client relationship.

## Acceptance Criteria

- [ ] Header: client name, industry, contact info, engagement start date
- [ ] Status badge (Active/Inactive)
- [ ] Notes section (expandable)
- [ ] Projects table: name, type (FP/T&M/Onboarding), status, resource count
- [ ] Project count by type summary cards
- [ ] Total active resources deployed count
- [ ] Edit button (for authorized roles)
- [ ] Navigation back to client list

## Out of Scope

* Financial metrics (revenue, cost, margin — Phase 2)
* Client history/trends

**Depends On:** Story 2

---

## Story 6: Client create/edit form

**Size:** S (2 pts) | **Priority:** P1 — Critical | **Sprint:** 2
**Labels:** `frontend`, `phase-1`, `sprint-2`, `must-have`

## Context (read before starting)

* `fsd/FSD.md` §2.4 — Client entity fields and constraints

**As a** CEO/CTO, **I want** a form to create and edit client records **so that** client information can be entered efficiently.

## Acceptance Criteria

- [ ] Form fields: Name (required), Industry, Contact Name, Contact Email, Contact Phone, Engagement Start Date, Notes
- [ ] Client-side validation: name required, email format check
- [ ] Duplicate name check (shows error before submit)
- [ ] Edit mode pre-populates all fields
- [ ] Success toast with redirect to client detail
- [ ] Error display for server-side validation failures
- [ ] Cancel button returns to previous page

## Out of Scope

* Bulk client import
* Contact management (multiple contacts per client)

**Depends On:** Story 2

---

## Story 7: Client audit logging

**Size:** XS (1 pt) | **Priority:** P2 — Major | **Sprint:** 2
**Labels:** `backend`, `phase-1`, `sprint-2`

## Context (read before starting)

* `fsd/FSD.md` §13 — Tracked entities (Client is not explicitly listed but follows pattern)
* `fsd/FSD.md` §2.12 — AuditLog entity

**As a** system, **I want** all client changes logged to the audit trail **so that** there is a complete history of modifications.

## Acceptance Criteria

- [ ] CREATE action logged with all field values
- [ ] UPDATE action logged per changed field (old_value, new_value)
- [ ] Deactivation logged as UPDATE on is_active field
- [ ] changed_by captured from current session user

## Out of Scope

* Audit log viewer UI (Phase 3)

**Depends On:** Story 2, EP-9 (Audit Logging service)
