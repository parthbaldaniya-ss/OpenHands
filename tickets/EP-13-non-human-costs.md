# EP-13: Non-Human Cost Management

Project expenses for tools, cloud, devices, and licenses — with currency, exchange rate, INR conversion, one-time and recurring support.

**Sprint:** 8 | **Stories:** 6 | **SP:** 13
**Spec refs:** `fsd/FSD.md` §2.10, §7.2, §11, `prd/PRD.md` §4.2

---

## Story 1: NonHumanCost database schema

**Size:** S (2 pts) | **Priority:** P0 — Blocker | **Sprint:** 8
**Labels:** `database`, `phase-2`, `sprint-8`, `must-have`

## Context (read before starting)

* `fsd/FSD.md` §2.10 — NonHumanCost entity: 13 fields, 5 categories

**As a** developer, **I want** the NonHumanCost table created **so that** project expenses beyond resource costs can be tracked.

## Acceptance Criteria

- [ ] Migration creates `non_human_cost` table: id (UUID PK), project_id (FK), description (STRING 500), category (ENUM: AI_TOOLS/CLOUD_INFRA/DEVICES/THIRD_PARTY_LICENSE/OTHER), amount (DECIMAL 15,2), currency (STRING 3, default INR), exchange_rate (DECIMAL 10,4, default 1.0), amount_inr (DECIMAL 15,2), cost_date (DATE), is_recurring (BOOLEAN, default false), recurring_end_date (DATE, nullable), created_by (FK → User), created_at
- [ ] FK constraint: project_id → project
- [ ] Indexes on project_id, category, cost_date
- [ ] Migration is reversible

## Out of Scope

* Vendor management
* Receipt/attachment storage

**Depends On:** EP-3 Story 1 (Project schema)

---

## Story 2: NonHumanCost CRUD API with validations

**Size:** M (3 pts) | **Priority:** P1 — Critical | **Sprint:** 8
**Labels:** `backend`, `phase-2`, `sprint-8`, `must-have`

## Context (read before starting)

* `fsd/FSD.md` §2.10 — NonHumanCost entity
* `fsd/FSD.md` §11 — 5 non-human cost validation rules

**As a** project manager, **I want** to log non-human project costs **so that** total project cost is accurately captured.

## Acceptance Criteria

- [ ] GET /api/projects/:projectId/costs — list non-human costs, filter by category, date range
- [ ] GET /api/costs/:id — single cost entry
- [ ] POST /api/costs — create with project_id, description, category, amount, currency, exchange_rate, cost_date, is_recurring, recurring_end_date
- [ ] PUT /api/costs/:id — update
- [ ] DELETE /api/costs/:id — hard delete (with confirmation)
- [ ] Validation: amount > 0 → "Cost amount must be positive"
- [ ] Validation: exchange_rate > 0 → "Exchange rate must be positive"
- [ ] Validation: currency = 'INR' → auto-set exchange_rate = 1.0
- [ ] amount_inr = amount × exchange_rate (auto-computed)
- [ ] Access: PM/DM for own projects, CEO/CTO for all, Finance for all
- [ ] created_by auto-set from session

## Out of Scope

* Recurring cost expansion/projection
* Vendor tracking
* Approval workflow

**Depends On:** Story 1, EP-3 (Project CRUD)

---

## Story 3: Recurring cost handling — End date enforcement

**Size:** S (2 pts) | **Priority:** P1 — Critical | **Sprint:** 8
**Labels:** `backend`, `phase-2`, `sprint-8`, `must-have`

## Context (read before starting)

* `fsd/FSD.md` §11 — "Recurring costs must have an end date"
* `fsd/FSD.md` §7.2 — Non-Human Cost monthly: SUM(amount_inr for active recurring)

**As a** system, **I want** recurring costs enforced with end dates **so that** cost projections are bounded.

## Acceptance Criteria

- [ ] Validation: is_recurring = true AND recurring_end_date is null → "Recurring costs must have an end date"
- [ ] Validation: recurring_end_date ≤ cost_date → "Recurring end date must be after cost date"
- [ ] For cost calculations: recurring costs count in each month from cost_date to recurring_end_date
- [ ] API returns is_recurring flag and recurring_end_date for display
- [ ] Monthly cost aggregation includes: one-time costs in that month + active recurring costs

## Out of Scope

* Recurring cost auto-generation (just calculation, not separate records)
* Frequency variations (all recurring = monthly)

**Depends On:** Story 2

---

## Story 4: Multi-currency support — Currency, exchange rate, INR

**Size:** S (2 pts) | **Priority:** P1 — Critical | **Sprint:** 8
**Labels:** `backend`, `frontend`, `phase-2`, `sprint-8`, `must-have`

## Context (read before starting)

* `fsd/FSD.md` §7.7 — Exchange rate conversion pattern
* `fsd/FSD.md` §2.10 — Currency and exchange_rate fields

**As a** project manager, **I want** to log costs in any currency with manual exchange rate **so that** international tool/cloud expenses are tracked.

## Acceptance Criteria

- [ ] Currency selector: dropdown of ISO 4217 codes
- [ ] Exchange rate input: manual, 4 decimal places
- [ ] When currency = INR: exchange_rate auto-set to 1.0, field disabled
- [ ] INR equivalent auto-calculated and displayed
- [ ] UI shows: Amount, Currency, Exchange Rate, INR Equivalent side by side
- [ ] Validation on both client and server

## Out of Scope

* Auto exchange rate fetching

**Depends On:** Story 2

---

## Story 5: Non-human cost list and management UI

**Size:** M (3 pts) | **Priority:** P1 — Critical | **Sprint:** 8
**Labels:** `frontend`, `phase-2`, `sprint-8`, `must-have`

## Context (read before starting)

* `fsd/FSD.md` §9 — Project Detail View → Non-Human Costs section

**As a** project manager, **I want** to view and manage non-human costs on my project **so that** all project expenses are visible.

## Acceptance Criteria

- [ ] Non-Human Costs section in project detail view
- [ ] Table columns: Date, Description, Category (badge), Amount, Currency, Rate, INR, Recurring (icon), End Date
- [ ] Filter by category
- [ ] Sort by date, amount
- [ ] Add cost button → form
- [ ] Form: description, category dropdown, amount, currency, exchange rate, date, recurring toggle, end date (if recurring)
- [ ] Edit/delete existing costs
- [ ] Total INR summary row
- [ ] Recurring costs visually distinct (icon or badge)

## Out of Scope

* Monthly cost projection view
* Category-level aggregation chart

**Depends On:** Story 2, EP-3 Story 6

---

## Story 6: Non-human cost audit logging

**Size:** XS (1 pt) | **Priority:** P2 — Major | **Sprint:** 8
**Labels:** `backend`, `phase-2`, `sprint-8`

## Context (read before starting)

* `fsd/FSD.md` §13 — NonHumanCost: ALL fields tracked

**As a** system, **I want** non-human cost changes logged **so that** expense modifications are traceable.

## Acceptance Criteria

- [ ] CREATE logged with all field values
- [ ] UPDATE logged per changed field
- [ ] DELETE logged
- [ ] changed_by from session

## Out of Scope

* Audit viewer

**Depends On:** Story 2, EP-9
