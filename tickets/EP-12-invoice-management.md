# EP-12: Invoice Management

Invoice CRUD with lifecycle, multi-currency with manual exchange rates, INR conversion, milestone linking for FP, and billing period for T&M/Onboarding.

**Sprint:** 7–8 | **Stories:** 7 | **SP:** 18
**Spec refs:** `fsd/FSD.md` §2.9, §6.3, §7.4, §7.7, §11, `prd/PRD.md` §4.2

---

## Story 1: Invoice database schema

**Size:** S (2 pts) | **Priority:** P0 — Blocker | **Sprint:** 7
**Labels:** `database`, `phase-2`, `sprint-7`, `must-have`

## Context (read before starting)

* `fsd/FSD.md` §2.9 — Invoice entity: 13 fields, amount_inr computed

**As a** developer, **I want** the Invoice table created **so that** billing records can be stored.

## Acceptance Criteria

- [ ] Migration creates `invoice` table: id (UUID PK), project_id (FK), milestone_id (nullable FK), invoice_date, billing_period_start (nullable), billing_period_end (nullable), amount (DECIMAL 15,2), currency (STRING 3), exchange_rate (DECIMAL 10,4, default 1.0), amount_inr (DECIMAL 15,2), status (ENUM: DRAFT/SUBMITTED/APPROVED/PAID), notes (TEXT), created_at
- [ ] FK constraints: project_id → project, milestone_id → milestone (nullable)
- [ ] Indexes on project_id, milestone_id, status, invoice_date
- [ ] Migration is reversible

## Out of Scope

* Credit notes
* Payment tracking beyond PAID status

**Depends On:** EP-3 Story 1, EP-11 Story 1

---

## Story 2: Invoice CRUD API with validations

**Size:** M (3 pts) | **Priority:** P1 — Critical | **Sprint:** 7
**Labels:** `backend`, `phase-2`, `sprint-7`, `must-have`

## Context (read before starting)

* `fsd/FSD.md` §2.9 — Invoice entity
* `fsd/FSD.md` §11 — 5 invoice validation rules

**As a** finance user, **I want** to create and manage invoices **so that** billing is tracked accurately.

## Acceptance Criteria

- [ ] GET /api/projects/:projectId/invoices — list invoices for a project
- [ ] GET /api/invoices/:id — single invoice with project and milestone details
- [ ] POST /api/invoices — create with project_id, invoice_date, amount, currency, exchange_rate, notes
  - For FP: milestone_id required
  - For T&M/Onboarding: billing_period_start and billing_period_end
- [ ] PUT /api/invoices/:id — update (only DRAFT status)
- [ ] Validation: amount > 0 → "Invoice amount must be positive"
- [ ] Validation: exchange_rate > 0 → "Exchange rate must be positive"
- [ ] Validation: currency = 'INR' → auto-set exchange_rate = 1.0
- [ ] Validation: FIXED_PRICE and no milestone_id → "Fixed price invoices must be linked to a milestone"
- [ ] Validation: linked milestone status ≠ APPROVED → "Milestone must be approved before invoicing"
- [ ] amount_inr auto-computed: amount × exchange_rate
- [ ] Currency copied from project at invoice time
- [ ] Only Finance can create/edit invoices

## Out of Scope

* Status transitions (separate story)
* PDF generation

**Depends On:** Story 1, EP-11 (Milestones exist)

---

## Story 3: Invoice lifecycle — DRAFT→SUBMITTED→APPROVED→PAID

**Size:** M (3 pts) | **Priority:** P1 — Critical | **Sprint:** 8
**Labels:** `backend`, `phase-2`, `sprint-8`, `must-have`

## Context (read before starting)

* `fsd/FSD.md` §6.3 — Invoice lifecycle state machine
* `fsd/FSD.md` §6.2 — APPROVED→INVOICED milestone link

**As a** finance user, **I want** to track invoice status through submission, approval, and payment **so that** billing lifecycle is managed.

## Acceptance Criteria

- [ ] PATCH /api/invoices/:id/transition — accepts target_status
- [ ] DRAFT → SUBMITTED: invoice sent to client (Finance)
- [ ] SUBMITTED → APPROVED: client confirmed (Finance)
- [ ] APPROVED → PAID: payment received (Finance)
- [ ] Invalid transitions return 400
- [ ] For FP invoices: when invoice reaches APPROVED, linked milestone transitions to INVOICED
- [ ] For FP invoices: when invoice reaches PAID, linked milestone transitions to PAID
- [ ] Only Finance can transition invoice status
- [ ] Audit logged

## Out of Scope

* Backward transitions
* Partial payments
* Credit notes

**Depends On:** Story 2

---

## Story 4: Multi-currency support — Exchange rate, INR conversion

**Size:** M (3 pts) | **Priority:** P1 — Critical | **Sprint:** 8
**Labels:** `backend`, `frontend`, `phase-2`, `sprint-8`, `must-have`

## Context (read before starting)

* `fsd/FSD.md` §7.7 — Exchange rate conversion: amount_inr = amount × exchange_rate
* `prd/PRD.md` §4.2 — Multi-currency invoicing, manual exchange rate

**As a** finance user, **I want** to enter invoices in the project's billing currency with a manual exchange rate **so that** INR equivalents are calculated accurately.

## Acceptance Criteria

- [ ] Currency field defaults to project's billing_currency (read-only on invoice)
- [ ] Exchange rate input: manual entry, 4 decimal places (DECIMAL 10,4)
- [ ] When currency = INR: exchange_rate auto-set to 1.0, field disabled
- [ ] amount_inr = amount × exchange_rate (auto-calculated, displayed)
- [ ] UI shows three values side by side: Original Amount, Exchange Rate, INR Equivalent
- [ ] Validation: exchange_rate > 0
- [ ] Existing invoices show both original and INR amounts

## Out of Scope

* Auto-fetching exchange rates from external APIs
* Exchange rate history

**Depends On:** Story 2

---

## Story 5: Invoice list and management UI

**Size:** M (3 pts) | **Priority:** P1 — Critical | **Sprint:** 8
**Labels:** `frontend`, `phase-2`, `sprint-8`, `must-have`

## Context (read before starting)

* `fsd/FSD.md` §9 — Project Detail View → Invoices section

**As a** finance user, **I want** to view and manage invoices on a project **so that** billing status is clear.

## Acceptance Criteria

- [ ] Invoice table in project detail view
- [ ] Columns: Invoice Date, Amount (billing currency), Exchange Rate, Amount (INR), Status, Milestone (if FP), Billing Period (if T&M/Onboarding), Notes
- [ ] Status badges: DRAFT (gray), SUBMITTED (blue), APPROVED (green), PAID (purple)
- [ ] Transition buttons based on current status (Finance role only)
- [ ] Sortable by date, amount, status
- [ ] Filter by status
- [ ] Total amounts row: sum of amount_inr by status
- [ ] Click invoice → detail view or edit (if DRAFT)

## Out of Scope

* Invoice PDF generation
* Email notifications

**Depends On:** Story 2, Story 3, EP-3 Story 6

---

## Story 6: Invoice create form — Milestone linking for FP

**Size:** M (3 pts) | **Priority:** P1 — Critical | **Sprint:** 8
**Labels:** `frontend`, `phase-2`, `sprint-8`, `must-have`

## Context (read before starting)

* `fsd/FSD.md` §2.9 — Invoice entity: milestone_id for FP, billing period for T&M
* `fsd/FSD.md` §11 — Invoice validations

**As a** finance user, **I want** an invoice creation form that adapts to project type **so that** the correct billing information is captured.

## Acceptance Criteria

- [ ] Form adapts based on project type:
  - **FP**: Milestone dropdown (only APPROVED milestones), amount pre-filled from milestone
  - **T&M/Onboarding**: Billing Period Start/End date pickers, amount entered manually
- [ ] Invoice Date (required)
- [ ] Amount (required, positive)
- [ ] Currency (read-only, from project)
- [ ] Exchange Rate (manual, disabled if INR)
- [ ] INR Equivalent (auto-calculated, read-only)
- [ ] Notes (optional)
- [ ] Client-side validations matching server rules
- [ ] FP: only shows APPROVED milestones not already INVOICED
- [ ] Success toast, redirects to invoice list

## Out of Scope

* Recurring invoice setup
* Invoice templates

**Depends On:** Story 2, EP-11 Story 5

---

## Story 7: Invoice audit logging

**Size:** XS (1 pt) | **Priority:** P2 — Major | **Sprint:** 8
**Labels:** `backend`, `phase-2`, `sprint-8`

## Context (read before starting)

* `fsd/FSD.md` §13 — Invoice tracked: amount, exchange_rate, status

**As a** system, **I want** invoice changes logged **so that** billing modifications are traceable.

## Acceptance Criteria

- [ ] Status transitions logged
- [ ] Amount changes logged (DRAFT only)
- [ ] Exchange rate changes logged
- [ ] changed_by from session

## Out of Scope

* Audit viewer

**Depends On:** Story 2, EP-9
