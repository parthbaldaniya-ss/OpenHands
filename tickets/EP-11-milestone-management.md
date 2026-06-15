# EP-11: Milestone Management

Full milestone lifecycle for Fixed Price projects — PLANNED through PAID with delivery delay detection.

**Sprint:** 6–7 | **Stories:** 7 | **SP:** 16
**Spec refs:** `fsd/FSD.md` §2.8, §6.2, `prd/PRD.md` §4.2.1

---

## Story 1: Milestone database schema

**Size:** S (2 pts) | **Priority:** P0 — Blocker | **Sprint:** 6
**Labels:** `database`, `phase-2`, `sprint-6`, `must-have`

## Context (read before starting)

* `fsd/FSD.md` §2.8 — Milestone entity: 9 fields, FIXED_PRICE only

**As a** developer, **I want** the Milestone table created **so that** fixed price project milestones can be tracked.

## Acceptance Criteria

- [ ] Migration creates `milestone` table: id (UUID PK), project_id (FK), name, amount (DECIMAL 15,2), planned_delivery_date, actual_delivery_date (nullable), status (ENUM: PLANNED/DELIVERED/APPROVED/INVOICED/PAID), sort_order (INTEGER), created_at
- [ ] FK constraint: project_id → project (must be FIXED_PRICE type)
- [ ] Indexes on project_id, status
- [ ] Migration is reversible

## Out of Scope

* Invoice linking (EP-12)
* Milestone overdue alerts (Phase 3)

**Depends On:** EP-3 Story 1 (Project schema)

---

## Story 2: Milestone CRUD API with FP project validation

**Size:** M (3 pts) | **Priority:** P1 — Critical | **Sprint:** 7
**Labels:** `backend`, `phase-2`, `sprint-7`, `must-have`

## Context (read before starting)

* `fsd/FSD.md` §2.8 — Milestone entity definition
* `prd/PRD.md` §4.2.1 — FP milestone attributes

**As a** project manager, **I want** to create and manage milestones on Fixed Price projects **so that** delivery and payment can be tracked.

## Acceptance Criteria

- [ ] GET /api/projects/:projectId/milestones — list milestones ordered by sort_order
- [ ] GET /api/milestones/:id — single milestone with project context
- [ ] POST /api/projects/:projectId/milestones — create with name, amount, planned_delivery_date, sort_order
- [ ] PUT /api/milestones/:id — update name, amount, planned_date, sort_order
- [ ] DELETE /api/milestones/:id — only if status = PLANNED (no deletion of delivered+)
- [ ] Validation: project must be FIXED_PRICE type
- [ ] Validation: amount > 0
- [ ] Milestone amounts can be modified during the project (not necessarily equal)
- [ ] Access: PM/DM for own projects, CEO/CTO for all

## Out of Scope

* Status transitions (separate story)
* Invoice creation from milestone
* Auto-sum validation against contract value

**Depends On:** Story 1, EP-3 (Project CRUD)

---

## Story 3: Milestone lifecycle — PLANNED→DELIVERED→APPROVED→INVOICED→PAID

**Size:** M (3 pts) | **Priority:** P1 — Critical | **Sprint:** 7
**Labels:** `backend`, `phase-2`, `sprint-7`, `must-have`

## Context (read before starting)

* `fsd/FSD.md` §6.2 — Milestone lifecycle state machine with 5 states
* `fsd/FSD.md` §6.2 — Transition side effects and authorization

**As a** project manager, **I want** to transition milestones through their lifecycle **so that** delivery and payment progress is tracked.

## Acceptance Criteria

- [ ] PATCH /api/milestones/:id/transition — accepts target_status
- [ ] PLANNED → DELIVERED: sets actual_delivery_date, flags delay if actual > planned (PM)
- [ ] DELIVERED → APPROVED: client approved the deliverable (PM/DM)
- [ ] APPROVED → INVOICED: creates Invoice with amount, exchange_rate, amount_inr (Finance)
- [ ] INVOICED → PAID: updates Invoice status to PAID (Finance)
- [ ] Invalid transitions return 400 with message
- [ ] INVOICED and PAID are terminal — no further forward transitions
- [ ] Audit logged for each transition

## Out of Scope

* Backward transitions (separate story)
* Credit notes

**Depends On:** Story 2

---

## Story 4: Milestone backward transitions with guards

**Size:** S (2 pts) | **Priority:** P1 — Critical | **Sprint:** 7
**Labels:** `backend`, `phase-2`, `sprint-7`, `must-have`

## Context (read before starting)

* `fsd/FSD.md` §6.2 — "DELIVERED can revert to PLANNED (rejected). APPROVED can revert to DELIVERED (withdrawn)."

**As a** project manager, **I want** to revert milestone status when needed **so that** incorrect transitions can be corrected.

## Acceptance Criteria

- [ ] DELIVERED → PLANNED: resets actual_delivery_date to null (rejection)
- [ ] APPROVED → DELIVERED: withdrawal of approval
- [ ] INVOICED → cannot revert (terminal, use credit note)
- [ ] PAID → cannot revert (terminal)
- [ ] Guard: only PM/DM can revert, Finance cannot revert to pre-INVOICED
- [ ] Audit logged for backward transitions
- [ ] UI shows backward transition buttons when valid

## Out of Scope

* Credit note creation
* Automatic milestone resets

**Depends On:** Story 3

---

## Story 5: Milestone list and transition UI

**Size:** M (3 pts) | **Priority:** P1 — Critical | **Sprint:** 7
**Labels:** `frontend`, `phase-2`, `sprint-7`, `must-have`

## Context (read before starting)

* `fsd/FSD.md` §9 — Project Detail View → Milestones section (FP only)
* `prd/PRD.md` §4.2.1 — Milestone lifecycle UI

**As a** project manager, **I want** to view and manage milestones on my Fixed Price project **so that** delivery progress is visible.

## Acceptance Criteria

- [ ] Milestone table in project detail view (FP projects only)
- [ ] Columns: Sort Order, Name, Amount (in billing currency), Planned Date, Actual Date, Status
- [ ] Status badges color-coded: PLANNED (blue), DELIVERED (yellow), APPROVED (green), INVOICED (purple), PAID (gray)
- [ ] Action buttons for valid transitions based on current status and user role
- [ ] Confirmation dialog for status transitions with side effect description
- [ ] Add milestone button (form: name, amount, planned date)
- [ ] Edit milestone (PLANNED only)
- [ ] Delete milestone with confirmation (PLANNED only)
- [ ] Reorder milestones via sort_order
- [ ] Delay indicator: red text when actual_delivery_date > planned_delivery_date

## Out of Scope

* Drag-and-drop reordering
* Gantt chart view

**Depends On:** Story 2, Story 3, EP-3 Story 6

---

## Story 6: Milestone delivery delay detection

**Size:** S (2 pts) | **Priority:** P2 — Major | **Sprint:** 7
**Labels:** `backend`, `phase-2`, `sprint-7`

## Context (read before starting)

* `prd/PRD.md` §4.2.1 — "Delivery delay flagged when actual exceeds planned"
* `fsd/FSD.md` §6.2 — PLANNED → DELIVERED sets actual_delivery_date

**As a** delivery manager, **I want** delayed milestones flagged **so that** delivery risks are visible.

## Acceptance Criteria

- [ ] When status transitions to DELIVERED: compare actual_delivery_date with planned_delivery_date
- [ ] If actual > planned: flag as delayed in API response (delayed: true, delay_days: N)
- [ ] Delay visible in milestone list (red indicator, "X days late")
- [ ] GET /api/projects/:id/milestones includes delay_info for each milestone
- [ ] Summary: count of delayed milestones per project

## Out of Scope

* Milestone overdue alerts (Phase 3 — alerts for PLANNED milestones past due date)
* Delay trend analysis

**Depends On:** Story 3

---

## Story 7: Milestone audit logging

**Size:** XS (1 pt) | **Priority:** P2 — Major | **Sprint:** 7
**Labels:** `backend`, `phase-2`, `sprint-7`

## Context (read before starting)

* `fsd/FSD.md` §13 — Milestone tracked fields: status, planned_date, actual_date, amount

**As a** system, **I want** milestone changes logged **so that** lifecycle transitions are traceable.

## Acceptance Criteria

- [ ] Status transitions logged: old_value → new_value
- [ ] Amount changes logged
- [ ] Planned date changes logged
- [ ] Actual delivery date changes logged
- [ ] changed_by from session

## Out of Scope

* Audit viewer

**Depends On:** Story 2, EP-9
