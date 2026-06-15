# EP-9: Audit Logging & System Config

Immutable audit log service for all tracked entities, plus system configuration key-value store.

**Sprint:** 1 | **Stories:** 3 | **SP:** 5
**Spec refs:** `fsd/FSD.md` §2.12, §2.14, §13

---

## Story 1: AuditLog database schema

**Size:** XS (1 pt) | **Priority:** P0 — Blocker | **Sprint:** 1
**Labels:** `database`, `phase-1`, `sprint-1`, `must-have`

## Context (read before starting)

* `fsd/FSD.md` §2.12 — AuditLog entity: 9 fields, immutable append-only
* `fsd/FSD.md` §13 — Tracked entities list

**As a** developer, **I want** the AuditLog table created **so that** all entity changes can be recorded.

## Acceptance Criteria

- [ ] Migration creates `audit_log` table: id (BIGINT PK auto-increment), entity_type (STRING 50), entity_id (UUID), action (ENUM: CREATE/UPDATE/DELETE), field_name (STRING 100, nullable), old_value (TEXT, nullable), new_value (TEXT, nullable), changed_by (FK → User), changed_at (TIMESTAMP)
- [ ] Indexes on entity_type, entity_id, changed_by, changed_at
- [ ] No UPDATE or DELETE permissions on this table (append-only by design)
- [ ] Migration is reversible (drops table)

## Out of Scope

* Audit log viewer UI (Phase 3)
* Point-in-time reconstruction (Phase 3)

**Depends On:** None (first migration)

---

## Story 2: Audit logging service — Generic logger for all tracked entities

**Size:** M (3 pts) | **Priority:** P0 — Blocker | **Sprint:** 1
**Labels:** `backend`, `phase-1`, `sprint-1`, `must-have`

## Context (read before starting)

* `fsd/FSD.md` §2.12 — AuditLog entity
* `fsd/FSD.md` §13 — Tracked entities and fields

**As a** developer, **I want** a reusable audit logging service **so that** all modules can log changes consistently.

## Acceptance Criteria

- [ ] Service/utility function: logAudit(entity_type, entity_id, action, changes, user_id)
- [ ] For CREATE: logs all field values as new_value entries
- [ ] For UPDATE: logs each changed field with old_value and new_value (one row per field)
- [ ] For DELETE: logs the deletion event
- [ ] Serializes complex values (dates, enums, decimals) to TEXT consistently
- [ ] Can be called from any module's service layer
- [ ] changed_by defaults to current session user, accepts "SYSTEM" for automated jobs
- [ ] Handles null values gracefully (stores as "null" string or empty)
- [ ] Non-blocking: audit log failures should not prevent the primary operation

## Out of Scope

* Audit log querying/viewing
* Real-time audit streaming

**Depends On:** Story 1

---

## Story 3: SystemConfig database schema and seed data

**Size:** XS (1 pt) | **Priority:** P0 — Blocker | **Sprint:** 1
**Labels:** `database`, `phase-1`, `sprint-1`, `must-have`

## Context (read before starting)

* `fsd/FSD.md` §2.14 — SystemConfig key-value store with 7 default keys

**As a** developer, **I want** the SystemConfig table created and seeded **so that** configurable thresholds are available.

## Acceptance Criteria

- [ ] Migration creates `system_config` table: key (STRING PK), value (STRING), description (TEXT)
- [ ] Seed data for Phase 1 keys:
  - system.working_days_per_month = 22
  - system.working_hours_per_day = 8
  - system.default_currency = INR
- [ ] Seed data for Phase 3 keys (values ready, features in Phase 3):
  - alert.contract_expiry_days = 30
  - alert.contract_expiry_urgent_days = 7
  - alert.bench_threshold_days = 7
  - alert.utilization_threshold_pct = 70
- [ ] GET /api/config — returns all config values (admin only)
- [ ] GET /api/config/:key — returns single config value
- [ ] Seed is idempotent

## Out of Scope

* Admin UI for editing config (Phase 3)
* Dynamic config reload

**Depends On:** None
