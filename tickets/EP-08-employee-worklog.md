# EP-8: Employee Worklog

Optional per-project daily hour logging, decoupled from billing, with engineer self-service view.

**Sprint:** 5 | **Stories:** 5 | **SP:** 12
**Spec refs:** `fsd/FSD.md` §2.11, §11, `prd/PRD.md` §4.3

---

## Story 1: Worklog database schema

**Size:** XS (1 pt) | **Priority:** P0 — Blocker | **Sprint:** 5
**Labels:** `database`, `phase-1`, `sprint-5`, `must-have`

## Context (read before starting)

* `fsd/FSD.md` §2.11 — Worklog entity with 7 fields

**As a** developer, **I want** the Worklog table created **so that** time entries can be stored.

## Acceptance Criteria

- [ ] Migration creates `worklog` table: id (UUID PK), resource_id (FK), project_id (FK), log_date (DATE, not null), hours (DECIMAL 4,1), note (TEXT), created_at
- [ ] Unique constraint on (resource_id, project_id, log_date) — one entry per resource per project per day
- [ ] Indexes on resource_id, project_id, log_date
- [ ] Migration is reversible

## Out of Scope

* Approval workflow
* Billing integration

**Depends On:** EP-4 Story 1, EP-3 Story 1

---

## Story 2: Worklog CRUD API with validations

**Size:** M (3 pts) | **Priority:** P2 — Major | **Sprint:** 5
**Labels:** `backend`, `phase-1`, `sprint-5`, `must-have`

## Context (read before starting)

* `fsd/FSD.md` §2.11 — Worklog entity, decoupled by design
* `fsd/FSD.md` §11 — 5 worklog validation rules

**As an** engineer, **I want** to log daily hours on my projects **so that** time tracking is recorded.

## Acceptance Criteria

- [ ] GET /api/worklogs — filtered by resource_id, project_id, date range
- [ ] POST /api/worklogs — create entry
- [ ] PUT /api/worklogs/:id — update hours or note
- [ ] DELETE /api/worklogs/:id — remove entry (own entries only)
- [ ] Validation: project.worklog_enabled = false → "Worklog is not enabled for this project"
- [ ] Validation: no ACTIVE assignment for resource on project → "You must have an active assignment to log hours"
- [ ] Validation: log_date > today → "Cannot log hours for future dates"
- [ ] Validation: hours < 0.5 or > 24 → "Hours must be between 0.5 and 24"
- [ ] Validation: duplicate (resource + project + log_date) → "Entry already exists for this date. Edit the existing entry."
- [ ] Half-hour increments (0.5, 1.0, 1.5, ..., 24.0)
- [ ] Backfill allowed if resource was active on that date (check assignment dates)

## Out of Scope

* Approval workflow
* Billing integration (deliberately decoupled)
* Cross-project daily total warnings

**Depends On:** Story 1, EP-5 (Assignments)

---

## Story 3: Worklog access control — SELF_ONLY for engineers

**Size:** S (2 pts) | **Priority:** P2 — Major | **Sprint:** 5
**Labels:** `backend`, `phase-1`, `sprint-5`, `must-have`

## Context (read before starting)

* `fsd/FSD.md` §10 — Engineer: EDIT SELF_ONLY for worklogs
* `prd/PRD.md` §6 — Worklog access: PM/DM view project worklogs

**As a** system, **I want** worklog access scoped correctly **so that** engineers only see their own entries.

## Acceptance Criteria

- [ ] Engineer: create/edit/delete own worklogs only (SELF_ONLY scope)
- [ ] PM: view worklogs for their projects (read-only)
- [ ] DM: view worklogs for their portfolio projects (read-only)
- [ ] CEO/CTO: view all worklogs
- [ ] Finance/HR: no access to worklogs
- [ ] Cannot edit another user's worklog entries

## Out of Scope

* Manager approval workflow

**Depends On:** Story 2, EP-1 Story 4

---

## Story 4: My Assignments — Engineer view

**Size:** M (3 pts) | **Priority:** P2 — Major | **Sprint:** 5
**Labels:** `frontend`, `phase-1`, `sprint-5`, `must-have`

## Context (read before starting)

* `fsd/FSD.md` §9 — My Assignments engineer view specification

**As an** engineer, **I want** a personal dashboard showing my active assignments **so that** I can see my current project allocations.

## Acceptance Criteria

- [ ] "My Assignments" page accessible from main navigation (Engineer role)
- [ ] Active Assignments table: project name, client, allocation %, start date, end date
- [ ] No billability, billing rate, or shadow data shown
- [ ] Project name links to project detail (limited engineer view)
- [ ] Visual indicator for assignments expiring soon (< 30 days)
- [ ] Empty state message if no active assignments

## Out of Scope

* Historical assignments
* Financial data
* Worklog entry (separate story)

**Depends On:** EP-5 (Assignments), EP-1 (Auth)

---

## Story 5: Worklog entry and history UI

**Size:** M (3 pts) | **Priority:** P2 — Major | **Sprint:** 5
**Labels:** `frontend`, `phase-1`, `sprint-5`, `must-have`

## Context (read before starting)

* `fsd/FSD.md` §9 — My Assignments → Worklog Entry and History
* `fsd/FSD.md` §11 — Worklog validations

**As an** engineer, **I want** to log daily hours and view my recent entries **so that** time tracking is easy and accessible.

## Acceptance Criteria

- [ ] Worklog entry form: project dropdown (only worklog-enabled projects with active assignment), date picker (no future dates), hours input (0.5-24, half-hour steps), note (optional)
- [ ] Quick entry: default to today's date
- [ ] Worklog history: table showing past 30 days, columns: date, project, hours, note
- [ ] Edit existing entries (own only): click to edit hours/note
- [ ] Delete entry with confirmation
- [ ] Client-side validations matching server-side rules
- [ ] Warning (not blocking) if total hours across projects > 24 for a day
- [ ] Success/error toast notifications

## Out of Scope

* Weekly/monthly summary views
* Export to CSV
* Manager approval UI

**Depends On:** Story 2, Story 4
