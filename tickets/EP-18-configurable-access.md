# EP-18: Configurable Access & Admin

Per-user permission overrides for configurable data types, admin UI for role permissions, and system configuration management.

**Sprint:** 11–12 | **Stories:** 4 | **SP:** 11
**Spec refs:** `fsd/FSD.md` §2.2, §2.14, `prd/PRD.md` §7 (Phase 3)

---

## Story 1: UserPermissionOverride schema and API

**Size:** M (3 pts) | **Priority:** P3 — Minor | **Sprint:** 11
**Labels:** `backend`, `database`, `phase-3`, `sprint-11`

## Context (read before starting)

* `fsd/FSD.md` §2.2 — is_configurable flag on RolePermission, user-level override mentioned for Phase 3

**As a** CEO/CTO, **I want** to override default role permissions for specific users **so that** access is customized without changing role definitions.

## Acceptance Criteria

- [ ] Migration creates `user_permission_override` table: id (UUID PK), user_id (FK → User), data_type (STRING 50), access_level (ENUM: NONE/VIEW/EDIT), scope (ENUM: ALL/OWN_PORTFOLIO/SELF_ONLY), created_at, created_by (FK → User)
- [ ] Unique constraint on (user_id, data_type)
- [ ] Only applies to data_types where role_permission.is_configurable = true
- [ ] GET /api/users/:id/permissions — returns effective permissions (role defaults + overrides)
- [ ] POST /api/users/:id/permissions — create/update override for a data_type
- [ ] DELETE /api/users/:id/permissions/:dataType — remove override (revert to role default)
- [ ] Access control middleware updated: check user override before role default
- [ ] Only CEO/CTO can manage overrides
- [ ] Audit logged

## Out of Scope

* Bulk permission management
* Permission templates

**Depends On:** EP-1 (Auth, RolePermission)

---

## Story 2: Configurable access admin UI

**Size:** M (3 pts) | **Priority:** P3 — Minor | **Sprint:** 11
**Labels:** `frontend`, `phase-3`, `sprint-11`

## Context (read before starting)

* `prd/PRD.md` §7 — Phase 3: Configurable data sensitivity per role
* `fsd/FSD.md` §2.2 — RolePermission with is_configurable flag

**As a** CEO/CTO, **I want** an admin interface to manage access permissions **so that** data sensitivity can be configured without code changes.

## Acceptance Criteria

- [ ] Admin page: "Access Control" (CEO/CTO only)
- [ ] Role permissions matrix: grid showing roles × data types with current access levels
- [ ] Configurable cells highlighted (is_configurable = true)
- [ ] Click configurable cell → dropdown to change access level
- [ ] User overrides section: select user → see effective permissions → add/remove overrides
- [ ] Visual diff: show where user differs from role default
- [ ] Save changes with confirmation
- [ ] Changes take effect immediately (no restart needed)

## Out of Scope

* Creating new roles
* Creating new data types
* Permission audit history

**Depends On:** Story 1

---

## Story 3: SystemConfig admin UI — All threshold settings

**Size:** M (3 pts) | **Priority:** P3 — Minor | **Sprint:** 12
**Labels:** `frontend`, `phase-3`, `sprint-12`

## Context (read before starting)

* `fsd/FSD.md` §2.14 — SystemConfig: 7 configurable keys
* `prd/PRD.md` §7 — Phase 3: Admin settings UI

**As a** CEO/CTO, **I want** to manage system thresholds through a UI **so that** alert triggers and calculations can be adjusted.

## Acceptance Criteria

- [ ] Admin page: "System Settings" (CEO/CTO only)
- [ ] Display all SystemConfig keys with current values and descriptions
- [ ] Grouped by category: System (working_days, working_hours, default_currency), Alerts (all threshold keys)
- [ ] Inline edit: click value → edit → save
- [ ] Validation: numeric values must be positive integers/decimals
- [ ] Current vs default indication (show if value differs from original seed)
- [ ] Reset to default button per setting
- [ ] Changes take effect immediately
- [ ] Audit logged

## Out of Scope

* Custom config keys
* Config import/export

**Depends On:** EP-9 Story 3

---

## Story 4: SystemConfig API — Get/update all configurable settings

**Size:** S (2 pts) | **Priority:** P3 — Minor | **Sprint:** 12
**Labels:** `backend`, `phase-3`, `sprint-12`

## Context (read before starting)

* `fsd/FSD.md` §2.14 — SystemConfig key-value store

**As a** system, **I want** a full CRUD API for system configuration **so that** the admin UI can manage settings.

## Acceptance Criteria

- [ ] GET /api/config — returns all config entries with key, value, description
- [ ] GET /api/config/:key — returns single config entry
- [ ] PUT /api/config/:key — update value (CEO/CTO only)
- [ ] Validation per key type (numeric keys must be valid numbers)
- [ ] Returns 404 for unknown keys
- [ ] Audit logged for changes
- [ ] All services that read config values use the API/service (not hardcoded)

## Out of Scope

* Adding new config keys via API
* Config versioning

**Depends On:** EP-9 Story 3
