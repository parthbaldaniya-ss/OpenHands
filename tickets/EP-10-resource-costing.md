# EP-10: Resource Costing & Billing Rates

Add financial fields to Resource (loaded_cost_monthly) and Assignment (billing_rate), with cost calculation engine.

**Sprint:** 6 | **Stories:** 5 | **SP:** 11
**Spec refs:** `fsd/FSD.md` §2.5, §2.7, §7.2, `prd/PRD.md` §4.3 (Phase 2)

---

## Story 1: Add loaded_cost_monthly to Resource — Migration and API

**Size:** S (2 pts) | **Priority:** P1 — Critical | **Sprint:** 6
**Labels:** `backend`, `database`, `phase-2`, `sprint-6`, `must-have`

## Context (read before starting)

* `fsd/FSD.md` §2.5 — loaded_cost_monthly: DECIMAL(15,2), nullable, restricted to CEO/CTO/Finance
* `fsd/FSD.md` §10 — Field-level restriction rules

**As a** finance user, **I want** to record the loaded cost (CTC + overhead) for each resource **so that** cost calculations are accurate.

## Acceptance Criteria

- [ ] Migration adds loaded_cost_monthly column to resource table (DECIMAL 15,2, nullable)
- [ ] PUT /api/resources/:id — accepts loaded_cost_monthly in update payload
- [ ] Field visible only to CEO, CTO, Finance roles (returns null for others)
- [ ] Field editable only by CEO, CTO, Finance roles
- [ ] Validation: if provided, must be > 0
- [ ] Audit logged when changed
- [ ] Existing resource records unaffected (nullable, no default needed)

## Out of Scope

* Historical cost tracking (use audit log)
* Bulk cost update

**Depends On:** EP-4 (Resource CRUD exists)

---

## Story 2: Add billing_rate to Assignment — Migration and API

**Size:** S (2 pts) | **Priority:** P1 — Critical | **Sprint:** 6
**Labels:** `backend`, `database`, `phase-2`, `sprint-6`, `must-have`

## Context (read before starting)

* `fsd/FSD.md` §2.7 — billing_rate: DECIMAL(10,2), nullable, per-hour in project billing_currency
* `fsd/FSD.md` §10 — billing_rate visible to CEO/CTO/Finance, configurable for DM

**As a** finance user, **I want** to set per-resource billing rates on project assignments **so that** revenue projections are calculated.

## Acceptance Criteria

- [ ] Migration adds billing_rate column to assignment table (DECIMAL 10,2, nullable)
- [ ] PUT /api/assignments/:id — accepts billing_rate in update payload
- [ ] billing_rate is per-hour in the project's billing_currency
- [ ] Shadow assignments: billing_rate must be null (validation)
- [ ] Visible to CEO, CTO, Finance; configurable for DM
- [ ] Returns null for unauthorized roles
- [ ] Audit logged when changed

## Out of Scope

* Rate card management
* Historical rate tracking

**Depends On:** EP-5 (Assignment CRUD exists)

---

## Story 3: Cost calculation engine — Resource cost per project

**Size:** M (3 pts) | **Priority:** P1 — Critical | **Sprint:** 6
**Labels:** `backend`, `phase-2`, `sprint-6`, `must-have`

## Context (read before starting)

* `fsd/FSD.md` §7.2 — Project Cost formula: Resource Cost = SUM(loaded_cost_monthly × allocation_pct / 100)

**As a** system, **I want** accurate project cost calculations **so that** margin analysis is possible.

## Acceptance Criteria

- [ ] Resource Cost (project, monthly) = SUM(loaded_cost_monthly × allocation_pct / 100) for all ACTIVE assignments
- [ ] Shadow resources contribute to cost (their loaded_cost × allocation counts)
- [ ] Resources without loaded_cost_monthly: excluded from calculation (not zero)
- [ ] Handles partial months: pro-rate based on assignment start/end within month
- [ ] Exposed as GET /api/projects/:id/financials (restricted to CEO/CTO/Finance)
- [ ] Calculation service reusable for aggregations
- [ ] All amounts in INR

## Out of Scope

* Non-human cost (EP-13)
* Revenue calculations (EP-14)

**Depends On:** Story 1, Story 2

---

## Story 4: Resource costing UI — Cost fields in resource profile

**Size:** S (2 pts) | **Priority:** P1 — Critical | **Sprint:** 6
**Labels:** `frontend`, `phase-2`, `sprint-6`, `must-have`

## Context (read before starting)

* `fsd/FSD.md` §2.5 — loaded_cost_monthly field
* `prd/PRD.md` §4.3 — Loaded Cost restricted to CEO/CTO/Finance

**As a** finance user, **I want** to view and edit resource loaded costs in the profile **so that** cost data is managed alongside resource data.

## Acceptance Criteria

- [ ] Loaded Cost field visible in resource detail view (CEO/CTO/Finance only)
- [ ] Editable in resource edit form (Finance only)
- [ ] Formatted as currency: ₹X,XX,XXX.XX per month
- [ ] Hidden entirely for non-authorized roles (not grayed out — absent)
- [ ] Validation: positive number, up to 15 digits

## Out of Scope

* Cost history view
* Bulk cost update UI

**Depends On:** Story 1, EP-4 Story 6

---

## Story 5: Billing rate UI — Rate column in assignment table

**Size:** S (2 pts) | **Priority:** P1 — Critical | **Sprint:** 6
**Labels:** `frontend`, `phase-2`, `sprint-6`, `must-have`

## Context (read before starting)

* `fsd/FSD.md` §2.7 — billing_rate per assignment
* `fsd/FSD.md` §10 — Field restrictions

**As a** finance user, **I want** to set and view billing rates on assignments **so that** revenue calculations are driven by actual rates.

## Acceptance Criteria

- [ ] Billing Rate column in assignment table (project detail view) — visible to authorized roles only
- [ ] Billing Rate field in assignment create/edit form — editable by Finance/CEO/CTO
- [ ] Rate shown in project billing currency (e.g., "$/hr", "€/hr")
- [ ] Shadow assignments: rate field disabled with tooltip "Shadow resources cannot have billing rates"
- [ ] Hidden for Engineer and HR roles

## Out of Scope

* Rate comparison tools
* Rate change history

**Depends On:** Story 2, EP-5 Story 7
