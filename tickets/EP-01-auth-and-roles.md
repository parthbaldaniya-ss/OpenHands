# EP-1: Auth & Roles

Authentication, authorization, role-based access control middleware, and user management.

**Sprint:** 1 | **Stories:** 6 | **SP:** 15
**Spec refs:** `fsd/FSD.md` §2.1–2.3, §10, `prd/PRD.md` §3, §6

---

## Story 1: Database schema — Role, RolePermission, User tables

**Size:** XS (1 pt) | **Priority:** P0 — Blocker | **Sprint:** 1
**Labels:** `database`, `phase-1`, `sprint-1`, `must-have`

## Context (read before starting)

* `fsd/FSD.md` §2.1–2.3 — Role, RolePermission, User entity definitions
* `fsd/FSD.md` §10 — Access control rules and scope definitions

**As a** developer, **I want** the database schema for Role, RolePermission, and User entities created **so that** all authentication and authorization features have a data foundation.

## Acceptance Criteria

- [ ] Migration creates `role` table with fields: id (UUID PK), name (unique), code (unique), permission_level, is_active, created_at
- [ ] Migration creates `role_permission` table with fields: id (UUID PK), role_id (FK), data_type, access_level (ENUM: NONE/VIEW/EDIT), scope (ENUM: ALL/OWN_PORTFOLIO/SELF_ONLY), is_configurable
- [ ] Unique constraint on (role_id, data_type) in role_permission
- [ ] Migration creates `user` table with fields: id (UUID PK), email (unique), name, role_id (FK), resource_id (nullable FK), is_active, created_at, updated_at
- [ ] Indexes on all FK columns and status fields
- [ ] Migration is reversible

## Out of Scope

* Seed data (separate story)
* API endpoints
* Password hashing or auth token management

**Depends On:** None

---

## Story 2: Seed data — Default roles, permissions, and admin user

**Size:** S (2 pts) | **Priority:** P0 — Blocker | **Sprint:** 1
**Labels:** `database`, `infrastructure`, `phase-1`, `sprint-1`, `must-have`

## Context (read before starting)

* `fsd/FSD.md` §2.1 — 7 default roles with permission_level values
* `fsd/FSD.md` §2.2 — Full role-permission matrix (15 data types × 7 roles)
* `prd/PRD.md` §6 — Role-based access matrix

**As a** system administrator, **I want** the system pre-populated with default roles, permissions, and an admin user **so that** the platform is functional on first launch.

## Acceptance Criteria

- [ ] Creates 7 roles: CEO (100), CTO (90), DM (70), PM (60), Finance (70), HR (50), Engineer (10)
- [ ] Creates all role_permission entries for 15 data types per PRD §6 access matrix
- [ ] Creates SystemConfig defaults: working_days=22, working_hours=8, default_currency=INR
- [ ] Creates admin user (CEO role)
- [ ] Script is idempotent — safe to re-run without duplicates
- [ ] Seed script can be run independently of application startup

## Out of Scope

* User self-registration
* Custom role creation

**Depends On:** Story 1 (database schema)

---

## Story 3: User authentication — Login, session management, logout

**Size:** M (3 pts) | **Priority:** P0 — Blocker | **Sprint:** 1
**Labels:** `backend`, `frontend`, `infrastructure`, `phase-1`, `sprint-1`, `must-have`

## Context (read before starting)

* `fsd/FSD.md` §2.3 — User entity with email as login identifier
* `fsd/FSD.md` §10 — Endpoint-level auth enforcement

**As a** user, **I want** to log in with my email and password and maintain a session **so that** I can access the platform securely.

## Acceptance Criteria

- [ ] POST /api/auth/login — accepts email + password, returns JWT/session token
- [ ] GET /api/auth/me — returns current user with role and permissions
- [ ] POST /api/auth/logout — invalidates session
- [ ] Password stored with bcrypt/argon2 hashing
- [ ] Protected route middleware rejects unauthenticated requests with 401
- [ ] Login page UI with email/password form
- [ ] Session persists across page refreshes
- [ ] Failed login shows appropriate error message

## Out of Scope

* OAuth/SSO integration
* Password reset flow
* Multi-factor authentication

**Depends On:** Story 1, Story 2

---

## Story 4: Access control middleware — Role-based route protection

**Size:** M (3 pts) | **Priority:** P0 — Blocker | **Sprint:** 1
**Labels:** `backend`, `phase-1`, `sprint-1`, `must-have`

## Context (read before starting)

* `fsd/FSD.md` §2.2 — RolePermission runtime access check algorithm (5-step process)
* `fsd/FSD.md` §10 — Scope rules per role, field-level restrictions
* `prd/PRD.md` §6 — Complete role-based access matrix

**As a** developer, **I want** a middleware that enforces role-based access on every API endpoint **so that** data security is consistent and automatic.

## Acceptance Criteria

- [ ] Middleware reads user's role_id from session/token
- [ ] Looks up RolePermission for role + data_type
- [ ] NONE → returns 403 or omits field from response
- [ ] VIEW → read-only access enforced
- [ ] EDIT → full access granted
- [ ] Scope applied: ALL = no filter, OWN_PORTFOLIO = filter by DM/PM assignment, SELF_ONLY = filter by own resource_id
- [ ] Field-level restrictions: loaded_cost_monthly, billing_rate, billability_pct, is_shadow return null for unauthorized roles
- [ ] Middleware is reusable — applied via decorator/annotation pattern
- [ ] 403 responses include descriptive message

## Out of Scope

* Per-user permission overrides (Phase 3)
* is_configurable flag handling (Phase 3)

**Depends On:** Story 1, Story 2, Story 3

---

## Story 5: User CRUD API — Create, list, update, deactivate users

**Size:** M (3 pts) | **Priority:** P1 — Critical | **Sprint:** 1
**Labels:** `backend`, `phase-1`, `sprint-1`, `must-have`

## Context (read before starting)

* `fsd/FSD.md` §2.3 — User entity definition
* `fsd/FSD.md` §10 — Only CEO/CTO can manage users

**As a** CEO/CTO, **I want** to manage platform users — create, list, update roles, and deactivate **so that** I control who has access and what they can see.

## Acceptance Criteria

- [ ] GET /api/users — paginated list with search by name/email, filter by role
- [ ] GET /api/users/:id — single user with role details
- [ ] POST /api/users — create user with email, name, role_id, optional resource_id
- [ ] PUT /api/users/:id — update user details and role
- [ ] PATCH /api/users/:id/deactivate — soft delete (is_active = false)
- [ ] Email uniqueness validated on create/update
- [ ] Only CEO/CTO roles can access user management endpoints
- [ ] Cannot deactivate own account
- [ ] Response format consistent across all endpoints

## Out of Scope

* User self-service profile editing
* Bulk user import

**Depends On:** Story 3, Story 4

---

## Story 6: User management UI — List, create, edit user views

**Size:** M (3 pts) | **Priority:** P1 — Critical | **Sprint:** 1
**Labels:** `frontend`, `phase-1`, `sprint-1`, `must-have`

## Context (read before starting)

* `fsd/FSD.md` §2.3 — User entity fields
* `prd/PRD.md` §3 — User roles and personas

**As a** CEO/CTO, **I want** a user management interface **so that** I can view all users, create new accounts, and manage roles visually.

## Acceptance Criteria

- [ ] User list page: table with name, email, role, status, created date
- [ ] Search by name/email
- [ ] Filter by role and status
- [ ] Create user form: email, name, role dropdown, resource link dropdown
- [ ] Edit user form: update name, role, resource link
- [ ] Deactivate user with confirmation dialog
- [ ] Only visible to CEO/CTO roles in navigation
- [ ] Success/error toast notifications

## Out of Scope

* Password reset from admin UI
* Bulk operations

**Depends On:** Story 5
