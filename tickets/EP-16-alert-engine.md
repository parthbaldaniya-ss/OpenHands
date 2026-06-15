# EP-16: Alert Engine

In-app alert system with 6 alert types, scheduled jobs, notification panel with deep-linking, and configurable thresholds.

**Sprint:** 10 | **Stories:** 8 | **SP:** 18
**Spec refs:** `fsd/FSD.md` §2.13, §12, `prd/PRD.md` §7 (Phase 3)

---

## Story 1: Alert database schema

**Size:** S (2 pts) | **Priority:** P0 — Blocker | **Sprint:** 10
**Labels:** `database`, `phase-3`, `sprint-10`, `must-have`

## Context (read before starting)

* `fsd/FSD.md` §2.13 — Alert entity: 10 fields, one row per recipient per event

**As a** developer, **I want** the Alert table created **so that** notification data can be stored.

## Acceptance Criteria

- [ ] Migration creates `alert` table: id (UUID PK), type (STRING 50), severity (ENUM: INFO/WARNING/CRITICAL), title (STRING 255), message (TEXT), recipient_user_id (FK → User), entity_type (STRING 50, nullable), entity_id (UUID, nullable), is_read (BOOLEAN, default false), is_dismissed (BOOLEAN, default false), created_at
- [ ] Indexes on recipient_user_id, type, is_read, created_at
- [ ] FK constraint: recipient_user_id → user
- [ ] Migration is reversible

## Out of Scope

* Email notifications
* Push notifications

**Depends On:** EP-1 Story 1 (User schema)

---

## Story 2: Alert engine — Contract expiry alerts

**Size:** M (3 pts) | **Priority:** P2 — Major | **Sprint:** 10
**Labels:** `backend`, `infrastructure`, `phase-3`, `sprint-10`, `must-have`

## Context (read before starting)

* `fsd/FSD.md` §12 — CONTRACT_EXPIRY: fires at 30d and 7d before contract end, daily, recipients: DM/CTO/CEO

**As a** CTO, **I want** to be alerted before contracts expire **so that** renewals are planned proactively.

## Acceptance Criteria

- [ ] Daily scheduled job checks T&M and Onboarding projects with contract_end_date
- [ ] Fires at 30 days (configurable: alert.contract_expiry_days)
- [ ] Fires at 7 days (configurable: alert.contract_expiry_urgent_days)
- [ ] 30d alert: severity=WARNING, 7d alert: severity=CRITICAL
- [ ] Recipients: DM of the project, CTO, CEO
- [ ] One alert per recipient per event (no duplicates for same project/threshold)
- [ ] Alert includes: project name, client name, days remaining, contract end date
- [ ] Deep-link: entity_type=Project, entity_id=project.id

## Out of Scope

* Email notifications
* Custom alert recipients

**Depends On:** Story 1, EP-3 (Projects)

---

## Story 3: Alert engine — Bench duration alerts

**Size:** S (2 pts) | **Priority:** P2 — Major | **Sprint:** 10
**Labels:** `backend`, `infrastructure`, `phase-3`, `sprint-10`, `must-have`

## Context (read before starting)

* `fsd/FSD.md` §12 — BENCH_DURATION: resource on bench > 7d (configurable), daily, recipients: DM/CTO/HR

**As a** DM, **I want** to be alerted when resources are on bench too long **so that** they can be allocated.

## Acceptance Criteria

- [ ] Daily scheduled job checks bench resources
- [ ] Fires when days_on_bench > alert.bench_threshold_days (default 7)
- [ ] Recipients: DM (reporting manager's DM), CTO, HR
- [ ] Severity: WARNING (7-14 days), CRITICAL (>14 days)
- [ ] No duplicate alerts for same resource if already alerted and not dismissed
- [ ] Alert includes: resource name, designation, days on bench, last project
- [ ] Deep-link: entity_type=Resource, entity_id=resource.id

## Out of Scope

* Bench cost in alert message

**Depends On:** Story 1, EP-7 Story 3

---

## Story 4: Alert engine — Over-allocation alerts

**Size:** S (2 pts) | **Priority:** P2 — Major | **Sprint:** 10
**Labels:** `backend`, `phase-3`, `sprint-10`, `must-have`

## Context (read before starting)

* `fsd/FSD.md` §12 — OVER_ALLOCATION: total allocation > 100%, on change, recipients: DM/PM

**As a** DM/PM, **I want** to be alerted when a resource becomes over-allocated **so that** capacity conflicts are resolved.

## Acceptance Criteria

- [ ] Triggered on assignment create or update (not scheduled — event-driven)
- [ ] Fires when resource total allocation exceeds 100%
- [ ] Recipients: PM of the project, DM of the project
- [ ] Severity: WARNING
- [ ] Alert includes: resource name, total allocation %, list of projects with allocations
- [ ] Clears/resolves if allocation drops back below 100% (no automatic dismissal, but new alert not created)
- [ ] Deep-link: entity_type=Resource, entity_id=resource.id

## Out of Scope

* Auto-resolution of over-allocation

**Depends On:** Story 1, EP-5 (Assignments)

---

## Story 5: Alert engine — Milestone overdue alerts

**Size:** S (2 pts) | **Priority:** P2 — Major | **Sprint:** 10
**Labels:** `backend`, `infrastructure`, `phase-3`, `sprint-10`, `must-have`

## Context (read before starting)

* `fsd/FSD.md` §12 — MILESTONE_OVERDUE: planned date passed AND status = PLANNED, daily, recipients: PM/DM

**As a** PM/DM, **I want** to be alerted about overdue milestones **so that** delivery delays are addressed.

## Acceptance Criteria

- [ ] Daily scheduled job checks FP project milestones
- [ ] Fires when: planned_delivery_date < today AND status = PLANNED
- [ ] Recipients: PM of the project, DM of the project
- [ ] Severity: WARNING (1-7 days overdue), CRITICAL (>7 days overdue)
- [ ] No duplicate alerts for same milestone if already alerted
- [ ] Alert includes: milestone name, project name, days overdue, planned date
- [ ] Deep-link: entity_type=Milestone, entity_id=milestone.id

## Out of Scope

* Automated escalation
* Milestone delivery forecasting

**Depends On:** Story 1, EP-11 (Milestones)

---

## Story 6: Alert engine — Utilization drop alerts

**Size:** S (2 pts) | **Priority:** P2 — Major | **Sprint:** 10
**Labels:** `backend`, `infrastructure`, `phase-3`, `sprint-10`, `must-have`

## Context (read before starting)

* `fsd/FSD.md` §12 — UTILIZATION_DROP: company util < 70% (configurable), weekly Monday, recipients: CTO/CEO

**As a** CTO/CEO, **I want** weekly alerts if company utilization drops **so that** capacity issues are caught early.

## Acceptance Criteria

- [ ] Weekly scheduled job runs every Monday
- [ ] Fires when company billable utilization < alert.utilization_threshold_pct (default 70%)
- [ ] Recipients: CTO, CEO
- [ ] Severity: WARNING
- [ ] Alert includes: current utilization %, threshold %, bench count, total resource count
- [ ] One alert per week (not daily)
- [ ] Deep-link: entity_type=Dashboard

## Out of Scope

* Utilization forecasting
* Per-team utilization alerts

**Depends On:** Story 1, EP-6 Story 1

---

## Story 7: Alert engine — Assignment auto-released alerts

**Size:** S (2 pts) | **Priority:** P2 — Major | **Sprint:** 10
**Labels:** `backend`, `phase-3`, `sprint-10`, `must-have`

## Context (read before starting)

* `fsd/FSD.md` §12 — ASSIGNMENT_AUTO_RELEASED: on release, recipients: PM/DM

**As a** PM/DM, **I want** to be notified when assignments are auto-released **so that** I can plan replacement or re-allocation.

## Acceptance Criteria

- [ ] Triggered by auto-release job (event-driven, not scheduled separately)
- [ ] Fires for each auto-released assignment
- [ ] Recipients: PM of the project, DM of the project
- [ ] Severity: INFO
- [ ] Alert includes: resource name, project name, allocation %, end date
- [ ] Deep-link: entity_type=Assignment, entity_id=assignment.id

## Out of Scope

* Replacement suggestions
* Auto-reallocation

**Depends On:** Story 1, EP-5 Story 4

---

## Story 8: Alert notification UI — Bell icon, panel, mark read, dismiss

**Size:** M (3 pts) | **Priority:** P2 — Major | **Sprint:** 10
**Labels:** `frontend`, `phase-3`, `sprint-10`, `must-have`

## Context (read before starting)

* `fsd/FSD.md` §2.13 — Alert entity with is_read, is_dismissed
* `fsd/FSD.md` §12 — All alerts in-app, dismissible

**As a** user, **I want** a notification panel showing my alerts **so that** I stay informed of important system events.

## Acceptance Criteria

- [ ] Bell icon in header/navbar with unread count badge
- [ ] Click bell → dropdown/panel with recent alerts (last 50)
- [ ] Each alert shows: severity icon, title, message preview, time ago
- [ ] Click alert → navigates to related entity (deep-link using entity_type/entity_id)
- [ ] Mark as read (click or explicit action)
- [ ] Dismiss button (removes from list, is_dismissed = true)
- [ ] "Mark all as read" button
- [ ] Filter by type (dropdown)
- [ ] Severity color coding: INFO (blue), WARNING (yellow), CRITICAL (red)
- [ ] Empty state: "No new notifications"
- [ ] Real-time update: poll every 60 seconds for new alerts

## Out of Scope

* Push notifications
* Email notifications
* Alert preferences/muting

**Depends On:** Story 1, Stories 2-7 (alert generators)
