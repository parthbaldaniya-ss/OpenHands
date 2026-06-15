# EP-19: Historical Queries & Audit Viewer

Point-in-time state reconstruction from audit log, historical query API, and audit log browser UI.

**Sprint:** 12 | **Stories:** 3 | **SP:** 11
**Spec refs:** `fsd/FSD.md` §13, `prd/PRD.md` §7 (Phase 3)

---

## Story 1: Point-in-time reconstruction engine

**Size:** L (5 pts) | **Priority:** P3 — Minor | **Sprint:** 12
**Labels:** `backend`, `phase-3`, `sprint-12`

## Context (read before starting)

* `fsd/FSD.md` §13 — Historical Point-in-Time Query algorithm: get current state, replay audit log backwards

**As a** CTO, **I want** to reconstruct the system state at any past date **so that** historical questions can be answered.

## Acceptance Criteria

- [ ] Reconstruction algorithm implemented per FSD §13:
  1. Get current state: SELECT * FROM entity WHERE id = X
  2. Get all changes AFTER target date: SELECT * FROM audit_log WHERE entity_type AND entity_id AND changed_at > target_date ORDER BY changed_at DESC
  3. For each change: revert current_state[field_name] = old_value
- [ ] Supports all tracked entities: Assignment, Milestone, Invoice, Project, Resource, NonHumanCost
- [ ] Handles CREATE entries (entity didn't exist before) → return null/empty
- [ ] Handles DELETE entries (entity was deleted after target date) → reconstruct from audit
- [ ] Returns reconstructed state as JSON matching current entity schema
- [ ] Performance: < 5s for entities with up to 1000 audit entries
- [ ] Service layer reusable for different query patterns

## Out of Scope

* Bulk reconstruction (full system snapshot)
* Differential comparison (state at date A vs date B)

**Depends On:** EP-9 (AuditLog with data)

---

## Story 2: Historical query API — View system state at any past date

**Size:** M (3 pts) | **Priority:** P3 — Minor | **Sprint:** 12
**Labels:** `backend`, `phase-3`, `sprint-12`

## Context (read before starting)

* `fsd/FSD.md` §13 — Point-in-time reconstruction
* `prd/PRD.md` §7 — Phase 3: Historical queries

**As a** CTO, **I want** API endpoints to query historical state **so that** I can answer "what was X on date Y" questions.

## Acceptance Criteria

- [ ] GET /api/history/:entityType/:entityId?date=YYYY-MM-DD — returns reconstructed entity state at date
- [ ] Supported entity types: assignment, milestone, invoice, project, resource, non_human_cost
- [ ] Returns 404 if entity didn't exist on that date
- [ ] Response includes: reconstructed_state, as_of_date, current_state (for comparison)
- [ ] GET /api/history/:entityType/:entityId/changes?from=DATE&to=DATE — returns change timeline
- [ ] Change timeline: ordered list of changes with field, old_value, new_value, changed_by, changed_at
- [ ] Access control: same permissions as viewing the entity currently
- [ ] CEO/CTO only for history queries (restrictive default)

## Out of Scope

* Bulk historical queries
* Historical dashboard snapshots
* Diff view between two dates

**Depends On:** Story 1

---

## Story 3: Audit log viewer UI — Browse by entity, user, date range

**Size:** M (3 pts) | **Priority:** P3 — Minor | **Sprint:** 12
**Labels:** `frontend`, `phase-3`, `sprint-12`

## Context (read before starting)

* `fsd/FSD.md` §2.12 — AuditLog entity structure
* `prd/PRD.md` §7 — Phase 3: Audit log viewer

**As a** CTO, **I want** a UI to browse audit logs **so that** I can investigate changes and understand what happened when.

## Acceptance Criteria

- [ ] Audit Log page (CEO/CTO only)
- [ ] Table columns: Timestamp, Entity Type, Entity ID (linked), Action, Field, Old Value, New Value, Changed By
- [ ] Filter by: entity type (dropdown), date range (date pickers), user (dropdown), action (CREATE/UPDATE/DELETE)
- [ ] Search by entity ID
- [ ] Pagination (50 per page)
- [ ] Sort by timestamp (default: newest first)
- [ ] Click entity link → navigates to entity detail
- [ ] Click user → shows user name
- [ ] Values formatted readably (dates, enums, currency amounts)
- [ ] Export to CSV (optional)
- [ ] Point-in-time query: select entity → enter date → show reconstructed state

## Out of Scope

* Real-time log streaming
* Log archiving/purging

**Depends On:** Story 2, EP-9
