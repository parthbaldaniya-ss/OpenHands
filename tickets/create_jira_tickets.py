#!/usr/bin/env python3
"""
Create all Jira tickets (Epics + Stories) for the Resource Intelligence & Project Economics Platform.

Usage:
    python3 create_jira_tickets.py

Environment variables (set in .env or export):
    JIRA_BASE_URL  - e.g. https://yourcompany.atlassian.net
    JIRA_EMAIL     - e.g. user@company.com
    API_TOKEN      - Jira API token
    JIRA_KEY       - Project key, e.g. OHRIPA
"""

import json
import os
import sys
import time
import requests
from dataclasses import dataclass, field

JIRA_BASE_URL = os.environ.get("JIRA_BASE_URL", "https://sspl-organisation.atlassian.net").rstrip("/")
JIRA_EMAIL = os.environ.get("JIRA_EMAIL", "").strip()
API_TOKEN = os.environ.get("API_TOKEN", "").strip().strip("'\"")
PROJECT_KEY = os.environ.get("JIRA_KEY", "OHRIPA").strip()

# Jira custom field IDs (discovered from /rest/api/3/field)
STORY_POINTS_FIELD = "customfield_10016"  # "Story point estimate"

API_URL = f"{JIRA_BASE_URL}/rest/api/3"


@dataclass
class Story:
    title: str
    description: str
    story_points: int
    priority: str  # Highest, High, Medium, Low, Lowest
    labels: list = field(default_factory=list)
    depends_on: list = field(default_factory=list)
    epic_key: str = ""
    jira_key: str = ""


@dataclass
class Epic:
    title: str
    description: str
    labels: list = field(default_factory=list)
    priority: str = "Medium"
    stories: list = field(default_factory=list)
    jira_key: str = ""


def make_request(method, endpoint, data=None, retries=5):
    url = f"{API_URL}/{endpoint}"
    auth = (JIRA_EMAIL, API_TOKEN)
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    for attempt in range(retries):
        try:
            resp = requests.request(method, url, json=data, auth=auth, headers=headers, timeout=60)
            if resp.status_code >= 400:
                print(f"  ERROR {resp.status_code}: {resp.text[:500]}")
                return None
            return resp.json() if resp.text else {}
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
            wait = 2 ** attempt
            print(f"  Network error (attempt {attempt+1}/{retries}): {type(e).__name__}. Retrying in {wait}s...")
            time.sleep(wait)
    print(f"  FATAL: All {retries} attempts failed.")
    return None


def create_issue(issue_type, summary, description, priority="Medium", labels=None,
                 story_points=None, epic_key=None):
    # Build ADF description from plain text (split paragraphs on double newline)
    paragraphs = description.split("\n\n") if description else [""]
    adf_content = []
    for para in paragraphs:
        text = para.strip()
        if text:
            adf_content.append({
                "type": "paragraph",
                "content": [{"type": "text", "text": text[:10000]}]
            })
    if not adf_content:
        adf_content = [{"type": "paragraph", "content": [{"type": "text", "text": " "}]}]

    payload = {
        "fields": {
            "project": {"key": PROJECT_KEY},
            "summary": summary[:255],
            "issuetype": {"name": issue_type},
            "priority": {"name": priority},
            "description": {
                "type": "doc",
                "version": 1,
                "content": adf_content
            },
        }
    }
    if labels:
        payload["fields"]["labels"] = labels
    if story_points is not None:
        payload["fields"][STORY_POINTS_FIELD] = story_points
    if epic_key:
        payload["fields"]["parent"] = {"key": epic_key}
    result = make_request("POST", "issue", payload)
    if result and "key" in result:
        return result["key"]
    return None


def create_link(inward_key, outward_key, link_type="Blocks"):
    payload = {
        "type": {"name": link_type},
        "inwardIssue": {"key": inward_key},
        "outwardIssue": {"key": outward_key},
    }
    make_request("POST", "issueLink", payload)


def build_all_epics():
    """Define all 19 epics with their stories."""
    epics = []

    # ── EP-1: Auth & Roles ──
    ep1 = Epic(
        title="Auth & Roles",
        description="Authentication, authorization, role-based access control middleware, and user management.\n\n**Sprint:** 1 | **Stories:** 6 | **SP:** 15\n**Spec refs:** fsd/FSD.md §2.1–2.3, §10, prd/PRD.md §3, §6",
        labels=["phase-1"],
        priority="Highest",
        stories=[
            Story("Database schema — Role, RolePermission, User tables",
                  "Create migration for Role, RolePermission, and User tables with all fields from FSD §2.1-2.3. Includes ENUM types for access_level and scope, unique constraints, and FK indexes.",
                  1, "Highest", ["database", "phase-1", "sprint-1", "must-have"]),
            Story("Seed data — Default roles, permissions, and admin user",
                  "Seed 7 default roles (CEO/CTO/DM/PM/Finance/HR/Engineer), full role-permission matrix (15 data types × 7 roles), SystemConfig defaults, and admin user. Idempotent script.",
                  2, "Highest", ["database", "infrastructure", "phase-1", "sprint-1", "must-have"]),
            Story("User authentication — Login, session management, logout",
                  "POST /api/auth/login with JWT, GET /api/auth/me for current user, POST /api/auth/logout. Password hashing with bcrypt. Protected route middleware. Login page UI.",
                  3, "Highest", ["backend", "frontend", "infrastructure", "phase-1", "sprint-1", "must-have"]),
            Story("Access control middleware — Role-based route protection",
                  "Middleware reads role from session, looks up RolePermission, enforces NONE/VIEW/EDIT access levels with ALL/OWN_PORTFOLIO/SELF_ONLY scope. Field-level restrictions (loaded_cost, billing_rate, etc. return null for unauthorized roles).",
                  3, "Highest", ["backend", "phase-1", "sprint-1", "must-have"]),
            Story("User CRUD API — Create, list, update, deactivate users",
                  "GET/POST/PUT /api/users endpoints. Paginated list with search/filter. Email uniqueness. Soft delete. CEO/CTO only access.",
                  3, "High", ["backend", "phase-1", "sprint-1", "must-have"]),
            Story("User management UI — List, create, edit user views",
                  "User list table with search/filter. Create/edit forms with role dropdown. Deactivate with confirmation. CEO/CTO only navigation.",
                  3, "High", ["frontend", "phase-1", "sprint-1", "must-have"]),
        ]
    )
    epics.append(ep1)

    # ── EP-2: Client Management ──
    ep2 = Epic(
        title="Client Management",
        description="Full client profiles with CRUD, multi-project support, deactivation logic, and client dashboard.\n\n**Sprint:** 2 | **Stories:** 7 | **SP:** 15\n**Spec refs:** fsd/FSD.md §2.4, §14, prd/PRD.md §4.1",
        labels=["phase-1"],
        priority="High",
        stories=[
            Story("Client database schema",
                  "Migration creates client table: id, name (unique), industry, contact_name/email/phone, engagement_start_date, notes, is_active, created_at.",
                  1, "Highest", ["database", "phase-1", "sprint-2", "must-have"]),
            Story("Client CRUD API with validations and access control",
                  "GET/POST/PUT /api/clients. Paginated list with search/filter. Name uniqueness. Role-based access: CEO/CTO edit, DM/PM portfolio view, Finance/HR view only.",
                  3, "High", ["backend", "phase-1", "sprint-2", "must-have"]),
            Story("Client deactivation handling — Block if active projects exist",
                  "PATCH /api/clients/:id/deactivate. Block if ACTIVE/ON_HOLD projects exist with error message. Audit logged.",
                  2, "High", ["backend", "phase-1", "sprint-2", "must-have"]),
            Story("Client list view — Filterable, sortable table",
                  "Table: Name, Industry, Contact, Engagement Date, Active Projects Count, Status. Search, filter, sort, pagination. Row click → detail.",
                  3, "High", ["frontend", "phase-1", "sprint-2", "must-have"]),
            Story("Client detail view — Profile with projects summary",
                  "Header with client info. Projects table. Project count by type cards. Total active resources. Edit button for authorized roles.",
                  3, "High", ["frontend", "phase-1", "sprint-2", "must-have"]),
            Story("Client create/edit form",
                  "Form: Name (required), Industry, Contact fields, Engagement Date, Notes. Duplicate name check. Edit mode pre-populates.",
                  2, "High", ["frontend", "phase-1", "sprint-2", "must-have"]),
            Story("Client audit logging",
                  "Log CREATE/UPDATE/DELETE actions for client entity. Per-field change tracking. changed_by from session.",
                  1, "Medium", ["backend", "phase-1", "sprint-2"]),
        ]
    )
    epics.append(ep2)

    # ── EP-3: Project Management ──
    ep3 = Epic(
        title="Project Management",
        description="Project CRUD for all three types (FP, T&M, Onboarding), status lifecycle, portfolio-scoped access, and type-specific views.\n\n**Sprint:** 3 | **Stories:** 9 | **SP:** 26\n**Spec refs:** fsd/FSD.md §2.6, §6.4, prd/PRD.md §4.2",
        labels=["phase-1"],
        priority="High",
        stories=[
            Story("Project database schema",
                  "Migration: project table with 14 fields. ENUMs for type (FP/T&M/Onboarding) and status (ACTIVE/COMPLETED/ON_HOLD/CANCELLED). FKs to client, dm, pm.",
                  2, "Highest", ["database", "phase-1", "sprint-3", "must-have"]),
            Story("Project CRUD API — All three project types with validations",
                  "GET/POST/PUT /api/projects. Type-specific validations: FP requires contract_value, T&M/Onboarding require contract_end_date. billing_currency ISO 4217.",
                  5, "High", ["backend", "phase-1", "sprint-3", "must-have"]),
            Story("Project status transitions — ACTIVE/COMPLETED/ON_HOLD/CANCELLED",
                  "PATCH /api/projects/:id/status. Valid transitions enforced. COMPLETED/CANCELLED auto-releases all ACTIVE assignments. Audit logged.",
                  3, "High", ["backend", "phase-1", "sprint-3", "must-have"]),
            Story("Project access control — DM/PM portfolio scoping",
                  "CEO/CTO all, DM sees dm_id=self, PM sees pm_id=self, Engineer sees own assignments only. Scope on list and detail endpoints.",
                  2, "High", ["backend", "phase-1", "sprint-3", "must-have"]),
            Story("Project list view — Filterable by type, status, client",
                  "Table: Name, Client, Type badge, Status badge, DM, PM, Currency, Resource Count. Type/status/client filters. Search, sort, pagination.",
                  3, "High", ["frontend", "phase-1", "sprint-3", "must-have"]),
            Story("Project detail view — Type-specific sections",
                  "Header with project info. Resource Assignments table. Type-specific sections (milestones placeholder for FP, contract end date for T&M/Onboarding). Worklog tab if enabled.",
                  5, "High", ["frontend", "phase-1", "sprint-3", "must-have"]),
            Story("Project create/edit form — Type-specific fields",
                  "Form adapts to project type. Client/DM/PM dropdowns. Type-specific fields show/hide. Client-side validations.",
                  3, "High", ["frontend", "phase-1", "sprint-3", "must-have"]),
            Story("Project status transition UI",
                  "Status badges. Action buttons for valid transitions. Confirmation dialogs for destructive transitions with warning about assignment releases.",
                  2, "High", ["frontend", "phase-1", "sprint-3", "must-have"]),
            Story("Project audit logging",
                  "Track status, contract_end_date, contract_value, dm_id, pm_id changes. changed_by from session.",
                  1, "Medium", ["backend", "phase-1", "sprint-3"]),
        ]
    )
    epics.append(ep3)

    # ── EP-4: Resource Management ──
    ep4 = Epic(
        title="Resource Management",
        description="Resource profiles with designations, technical expertise, tags, self-referencing hierarchy, and access-controlled views.\n\n**Sprint:** 2–3 | **Stories:** 8 | **SP:** 19\n**Spec refs:** fsd/FSD.md §2.5, §14, prd/PRD.md §4.3",
        labels=["phase-1"],
        priority="High",
        stories=[
            Story("Resource & ResourceTag database schema",
                  "Migration: resource table (10 fields, self-ref FK for reporting_manager_id) + resource_tag join table (composite PK on resource_id, tag).",
                  2, "Highest", ["database", "phase-1", "sprint-2", "must-have"]),
            Story("Resource CRUD API with tags management",
                  "GET/POST/PUT /api/resources. Search by name/employee_id, filter by designation/tags. Tag add/remove endpoints. employee_id uniqueness.",
                  3, "High", ["backend", "phase-1", "sprint-2", "must-have"]),
            Story("Resource access control and field-level restrictions",
                  "CEO/CTO full access. HR edit profiles. DM/PM view project resources. Finance view with cost. Engineer view own + availability. loaded_cost returns null for unauthorized.",
                  2, "High", ["backend", "phase-1", "sprint-2", "must-have"]),
            Story("Resource deactivation — Release all active assignments",
                  "PATCH /api/resources/:id/deactivate. All ACTIVE assignments released. Cannot receive new assignments. Each release audit logged.",
                  2, "High", ["backend", "phase-1", "sprint-3", "must-have"]),
            Story("Resource list view — Search, filter by designation/tags",
                  "Table: Employee ID, Name, Designation, Expertise, Tags chips, Allocation %, Status. Color-coded allocation. Search, filter, sort.",
                  3, "High", ["frontend", "phase-1", "sprint-3", "must-have"]),
            Story("Resource detail/profile view — Assignments, tags, availability",
                  "Header with profile info. Tags section. Assignments table. Allocation summary. Availability indicator. Edit/deactivate buttons.",
                  3, "High", ["frontend", "phase-1", "sprint-3", "must-have"]),
            Story("Resource create/edit form with tag management",
                  "Form: Employee ID, Name, Designation, Expertise, DOJ, Reporting Manager dropdown. Tags input with suggestions. Uniqueness validation.",
                  3, "High", ["frontend", "phase-1", "sprint-3", "must-have"]),
            Story("Resource audit logging",
                  "Track designation, technical_expertise, reporting_manager_id, is_active, tag changes. changed_by from session.",
                  1, "Medium", ["backend", "phase-1", "sprint-3"]),
        ]
    )
    epics.append(ep4)

    # ── EP-5: Allocation & Assignment Tracking ──
    ep5 = Epic(
        title="Allocation & Assignment Tracking",
        description="Core assignment entity with allocation/billability model, shadow resources, auto-release job, designation resolution, and over-allocation warnings.\n\n**Sprint:** 4 | **Stories:** 10 | **SP:** 27\n**Spec refs:** fsd/FSD.md §2.7, §6.1, §8, §11, prd/PRD.md §4.3, §5",
        labels=["phase-1"],
        priority="High",
        stories=[
            Story("Assignment database schema",
                  "Migration: assignment table (15 fields). ENUM status (ACTIVE/RELEASED/AUTO_RELEASED). FKs to project and resource. billing_rate column present but nullable for Phase 2.",
                  2, "Highest", ["database", "phase-1", "sprint-4", "must-have"]),
            Story("Assignment CRUD API with all validations",
                  "GET/POST/PUT /api/assignments. 7 validation rules: billability≤allocation, shadow=0 billability, end>start, no duplicate active, project must be active, allocation 1-100, over-allocation warning (not blocking).",
                  5, "High", ["backend", "phase-1", "sprint-4", "must-have"]),
            Story("Assignment lifecycle — RELEASED/AUTO_RELEASED transitions",
                  "PATCH /api/assignments/:id/release. Set released_at, recalculate total allocation. Cannot modify released assignments. Re-assignment after release allowed.",
                  3, "High", ["backend", "phase-1", "sprint-4", "must-have"]),
            Story("Auto-release scheduled job",
                  "Daily midnight IST job. Processes ACTIVE assignments with end_date ≤ today. Sets AUTO_RELEASED, creates alert, audit logs. Idempotent. Handles extension edge case.",
                  3, "High", ["backend", "infrastructure", "phase-1", "sprint-4", "must-have"]),
            Story("Assignment access control with portfolio scoping",
                  "CEO/CTO all, DM/PM own projects, Finance view, HR view (no billability/shadow), Engineer own only. Field restrictions on billability and shadow.",
                  2, "High", ["backend", "phase-1", "sprint-4", "must-have"]),
            Story("Designation resolution logic — Fallback from assignment to resource",
                  "All APIs return resolved designation: assignment.project_designation ?? resource.designation. Same for expertise. Search/filter use resolved values.",
                  2, "High", ["backend", "phase-1", "sprint-4", "must-have"]),
            Story("Assignment list view — Per project with all columns",
                  "Table: Resource, Designation (resolved), Allocation %, Billability %, Shadow, Dates, Status. Filter by status. Over-allocation warning icons. Row actions.",
                  3, "High", ["frontend", "phase-1", "sprint-4", "must-have"]),
            Story("Assignment create/edit form — Allocation, billability, shadow toggle",
                  "Resource dropdown, allocation/billability inputs, shadow toggle (auto-zeros billability), designation/expertise overrides, dates. Client-side validations.",
                  3, "High", ["frontend", "phase-1", "sprint-4", "must-have"]),
            Story("Over-allocation warning UI",
                  "Warning in assignment form when total >100%. Red allocation in resource list. Warning state in resource detail. Non-blocking.",
                  2, "Medium", ["frontend", "phase-1", "sprint-4"]),
            Story("Assignment audit logging",
                  "Track ALL assignment fields. Status transitions logged. changed_by from session or SYSTEM for auto-release.",
                  1, "Medium", ["backend", "phase-1", "sprint-4"]),
        ]
    )
    epics.append(ep5)

    # ── EP-6: Utilization Dashboards ──
    ep6 = Epic(
        title="Utilization Dashboards",
        description="Company-wide, per-DM, per-client, per-project, and per-resource utilization views.\n\n**Sprint:** 5 | **Stories:** 5 | **SP:** 16\n**Spec refs:** fsd/FSD.md §7.1, §9, prd/PRD.md §4.3",
        labels=["phase-1"],
        priority="Medium",
        stories=[
            Story("Utilization calculation engine — Company and per-resource",
                  "Formulas: Total Allocation = SUM(allocation_pct), Billable Allocation = SUM(billability_pct where !shadow), Utilization Rate, Company Utilization. Edge cases: no resources, no assignments.",
                  3, "High", ["backend", "phase-1", "sprint-5", "must-have"]),
            Story("Company dashboard — Data API with role scoping",
                  "GET /api/dashboard/company. Billable utilization, bench count/names, shadow allocation, active projects by type, upcoming releases (30d), overdue milestones.",
                  3, "Medium", ["backend", "phase-1", "sprint-5", "must-have"]),
            Story("Company dashboard — UI with KPI cards and widgets",
                  "KPI cards for utilization/bench/shadow/projects. Upcoming releases table. Drill-down links. Responsive layout. Loading states.",
                  5, "Medium", ["frontend", "phase-1", "sprint-5", "must-have"]),
            Story("Project-level utilization view",
                  "Utilization section on project detail: total allocation, billable allocation, resource count, per-resource breakdown with visual bars.",
                  3, "Medium", ["frontend", "phase-1", "sprint-5"]),
            Story("Per-DM portfolio utilization view",
                  "DM portfolio dashboard: avg utilization across portfolio, per-project table, bench resources in portfolio.",
                  2, "Medium", ["frontend", "phase-1", "sprint-5"]),
        ]
    )
    epics.append(ep6)

    # ── EP-7: Resource Availability ──
    ep7 = Epic(
        title="Resource Availability",
        description="Public availability view: bench, partial, releasing soon, fully allocated — visible to ALL users.\n\n**Sprint:** 5 | **Stories:** 3 | **SP:** 10\n**Spec refs:** fsd/FSD.md §9, prd/PRD.md §4.3",
        labels=["phase-1"],
        priority="High",
        stories=[
            Story("Resource availability API — Bench, partial, releasing soon",
                  "GET /api/resources/availability. Four categories: Bench (0%), Partially Available, Releasing Soon (30/60/90d filter), Fully Allocated. Accessible to ALL roles. No financial data.",
                  3, "High", ["backend", "phase-1", "sprint-5", "must-have"]),
            Story("Resource availability view — All four sections",
                  "Bench section, Partially Available section, Releasing Soon with 30/60/90 toggle, Fully Allocated. Count badges. Drill-down links. No CTC/billing/shadow.",
                  5, "High", ["frontend", "phase-1", "sprint-5", "must-have"]),
            Story("Bench detection and tracking",
                  "Bench = 0% total allocation. Bench start = max(released_at) or DOJ. Days on bench calculated. Recalculated on assignment changes.",
                  2, "High", ["backend", "phase-1", "sprint-5", "must-have"]),
        ]
    )
    epics.append(ep7)

    # ── EP-8: Employee Worklog ──
    ep8 = Epic(
        title="Employee Worklog",
        description="Optional per-project daily hour logging, decoupled from billing, with engineer self-service view.\n\n**Sprint:** 5 | **Stories:** 5 | **SP:** 12\n**Spec refs:** fsd/FSD.md §2.11, §11, prd/PRD.md §4.3",
        labels=["phase-1"],
        priority="Medium",
        stories=[
            Story("Worklog database schema",
                  "Migration: worklog table (7 fields). Unique constraint on (resource_id, project_id, log_date). Indexes.",
                  1, "Highest", ["database", "phase-1", "sprint-5", "must-have"]),
            Story("Worklog CRUD API with validations",
                  "GET/POST/PUT/DELETE /api/worklogs. 5 validations: worklog_enabled, active assignment, no future dates, hours 0.5-24, no duplicates. Backfill allowed.",
                  3, "Medium", ["backend", "phase-1", "sprint-5", "must-have"]),
            Story("Worklog access control — SELF_ONLY for engineers",
                  "Engineer: EDIT own only. PM/DM: view project worklogs. CEO/CTO: view all. Finance/HR: no access.",
                  2, "Medium", ["backend", "phase-1", "sprint-5", "must-have"]),
            Story("My Assignments — Engineer view",
                  "Personal dashboard: active assignments table with project, client, allocation, dates. No financial data. Navigation for Engineer role.",
                  3, "Medium", ["frontend", "phase-1", "sprint-5", "must-have"]),
            Story("Worklog entry and history UI",
                  "Entry form: project dropdown, date picker, hours (half-hour steps), note. History table (30 days). Edit/delete own entries. Cross-project daily total warning.",
                  3, "Medium", ["frontend", "phase-1", "sprint-5", "must-have"]),
        ]
    )
    epics.append(ep8)

    # ── EP-9: Audit Logging & System Config ──
    ep9 = Epic(
        title="Audit Logging & System Config",
        description="Immutable audit log service and system configuration key-value store.\n\n**Sprint:** 1 | **Stories:** 3 | **SP:** 5\n**Spec refs:** fsd/FSD.md §2.12, §2.14, §13",
        labels=["phase-1"],
        priority="Highest",
        stories=[
            Story("AuditLog database schema",
                  "Migration: audit_log table (9 fields, BIGINT PK auto-increment). Append-only. Indexes on entity_type, entity_id, changed_by, changed_at.",
                  1, "Highest", ["database", "phase-1", "sprint-1", "must-have"]),
            Story("Audit logging service — Generic logger for all tracked entities",
                  "Reusable service: logAudit(entity_type, entity_id, action, changes, user_id). Handles CREATE/UPDATE/DELETE. Per-field change tracking. Non-blocking.",
                  3, "Highest", ["backend", "phase-1", "sprint-1", "must-have"]),
            Story("SystemConfig database schema and seed data",
                  "Migration: system_config table (key PK, value, description). Seed 7 keys: working_days=22, working_hours=8, default_currency=INR, alert thresholds. GET /api/config endpoints.",
                  1, "Highest", ["database", "phase-1", "sprint-1", "must-have"]),
        ]
    )
    epics.append(ep9)

    # ── EP-10: Resource Costing & Billing Rates ──
    ep10 = Epic(
        title="Resource Costing & Billing Rates",
        description="Financial fields for Resource (loaded_cost_monthly) and Assignment (billing_rate), with cost calculation engine.\n\n**Sprint:** 6 | **Stories:** 5 | **SP:** 11\n**Spec refs:** fsd/FSD.md §2.5, §2.7, §7.2, prd/PRD.md §4.3",
        labels=["phase-2"],
        priority="High",
        stories=[
            Story("Add loaded_cost_monthly to Resource — Migration and API",
                  "Add DECIMAL(15,2) column. Visible/editable only to CEO/CTO/Finance. Validation: must be > 0. Audit logged.",
                  2, "High", ["backend", "database", "phase-2", "sprint-6", "must-have"]),
            Story("Add billing_rate to Assignment — Migration and API",
                  "Add DECIMAL(10,2) column. Per-hour in project billing_currency. Shadow = must be null. Visible to CEO/CTO/Finance, configurable for DM.",
                  2, "High", ["backend", "database", "phase-2", "sprint-6", "must-have"]),
            Story("Cost calculation engine — Resource cost per project",
                  "Resource Cost = SUM(loaded_cost_monthly × allocation_pct/100). Shadow resources count toward cost. GET /api/projects/:id/financials.",
                  3, "High", ["backend", "phase-2", "sprint-6", "must-have"]),
            Story("Resource costing UI — Cost fields in resource profile",
                  "Loaded Cost visible in resource detail (CEO/CTO/Finance). Editable in form (Finance). Formatted ₹X,XX,XXX.XX/month. Hidden for unauthorized.",
                  2, "High", ["frontend", "phase-2", "sprint-6", "must-have"]),
            Story("Billing rate UI — Rate column in assignment table",
                  "Billing Rate column in assignment table. Editable in form. Rate in project currency. Shadow disabled. Hidden for Engineer/HR.",
                  2, "High", ["frontend", "phase-2", "sprint-6", "must-have"]),
        ]
    )
    epics.append(ep10)

    # ── EP-11: Milestone Management ──
    ep11 = Epic(
        title="Milestone Management",
        description="Full milestone lifecycle for Fixed Price projects — PLANNED through PAID with delivery delay detection.\n\n**Sprint:** 6–7 | **Stories:** 7 | **SP:** 16\n**Spec refs:** fsd/FSD.md §2.8, §6.2, prd/PRD.md §4.2.1",
        labels=["phase-2"],
        priority="High",
        stories=[
            Story("Milestone database schema",
                  "Migration: milestone table (9 fields). ENUM status (PLANNED/DELIVERED/APPROVED/INVOICED/PAID). FK to project (must be FIXED_PRICE).",
                  2, "Highest", ["database", "phase-2", "sprint-6", "must-have"]),
            Story("Milestone CRUD API with FP project validation",
                  "GET/POST/PUT/DELETE /api/projects/:id/milestones. FP validation. Amount > 0. Ordered by sort_order. Delete only PLANNED.",
                  3, "High", ["backend", "phase-2", "sprint-7", "must-have"]),
            Story("Milestone lifecycle — PLANNED→DELIVERED→APPROVED→INVOICED→PAID",
                  "PATCH /api/milestones/:id/transition. Side effects: DELIVERED sets actual_date, APPROVED→INVOICED creates Invoice. Audit logged.",
                  3, "High", ["backend", "phase-2", "sprint-7", "must-have"]),
            Story("Milestone backward transitions with guards",
                  "DELIVERED→PLANNED (rejection, clears actual_date). APPROVED→DELIVERED (withdrawal). INVOICED/PAID terminal. Audit logged.",
                  2, "High", ["backend", "phase-2", "sprint-7", "must-have"]),
            Story("Milestone list and transition UI",
                  "Table in project detail (FP only). Columns: order, name, amount, planned/actual date, status badge. Transition buttons. Add/edit/delete. Delay indicator.",
                  3, "High", ["frontend", "phase-2", "sprint-7", "must-have"]),
            Story("Milestone delivery delay detection",
                  "Flag when actual_date > planned_date. API returns delayed flag and delay_days. Red indicator in UI.",
                  2, "Medium", ["backend", "phase-2", "sprint-7"]),
            Story("Milestone audit logging",
                  "Track status, planned_date, actual_date, amount changes. changed_by from session.",
                  1, "Medium", ["backend", "phase-2", "sprint-7"]),
        ]
    )
    epics.append(ep11)

    # ── EP-12: Invoice Management ──
    ep12 = Epic(
        title="Invoice Management",
        description="Invoice CRUD with lifecycle, multi-currency with manual exchange rates, milestone linking for FP, billing period for T&M/Onboarding.\n\n**Sprint:** 7–8 | **Stories:** 7 | **SP:** 18\n**Spec refs:** fsd/FSD.md §2.9, §6.3, §7.4, §7.7, §11",
        labels=["phase-2"],
        priority="High",
        stories=[
            Story("Invoice database schema",
                  "Migration: invoice table (13 fields). ENUM status (DRAFT/SUBMITTED/APPROVED/PAID). FKs to project and milestone (nullable). amount_inr computed.",
                  2, "Highest", ["database", "phase-2", "sprint-7", "must-have"]),
            Story("Invoice CRUD API with validations",
                  "GET/POST/PUT /api/invoices. 5 validations: amount>0, exchange_rate>0, INR auto-rate, FP requires milestone, milestone must be APPROVED. amount_inr auto-computed.",
                  3, "High", ["backend", "phase-2", "sprint-7", "must-have"]),
            Story("Invoice lifecycle — DRAFT→SUBMITTED→APPROVED→PAID",
                  "PATCH /api/invoices/:id/transition. FP: APPROVED updates milestone to INVOICED, PAID updates milestone to PAID. Finance only. Audit logged.",
                  3, "High", ["backend", "phase-2", "sprint-8", "must-have"]),
            Story("Multi-currency support — Exchange rate, INR conversion",
                  "Currency from project (read-only). Manual exchange rate (4 decimals). INR auto 1.0. amount_inr auto-calculated. UI shows 3 values side by side.",
                  3, "High", ["backend", "frontend", "phase-2", "sprint-8", "must-have"]),
            Story("Invoice list and management UI",
                  "Invoice table in project detail. Columns: date, amount, rate, INR, status badge, milestone/period. Transition buttons (Finance). Filter, sort, totals.",
                  3, "High", ["frontend", "phase-2", "sprint-8", "must-have"]),
            Story("Invoice create form — Milestone linking for FP",
                  "Form adapts by project type. FP: milestone dropdown (APPROVED only), amount pre-filled. T&M: billing period + manual amount. Currency/rate/INR display.",
                  3, "High", ["frontend", "phase-2", "sprint-8", "must-have"]),
            Story("Invoice audit logging",
                  "Track status, amount, exchange_rate changes. changed_by from session.",
                  1, "Medium", ["backend", "phase-2", "sprint-8"]),
        ]
    )
    epics.append(ep12)

    # ── EP-13: Non-Human Cost Management ──
    ep13 = Epic(
        title="Non-Human Cost Management",
        description="Project expenses for tools, cloud, devices, licenses — with currency, exchange rate, INR, one-time and recurring.\n\n**Sprint:** 8 | **Stories:** 6 | **SP:** 13\n**Spec refs:** fsd/FSD.md §2.10, §7.2, §11",
        labels=["phase-2"],
        priority="High",
        stories=[
            Story("NonHumanCost database schema",
                  "Migration: non_human_cost table (13 fields). ENUM category (AI_TOOLS/CLOUD_INFRA/DEVICES/THIRD_PARTY_LICENSE/OTHER). FKs to project and user.",
                  2, "Highest", ["database", "phase-2", "sprint-8", "must-have"]),
            Story("NonHumanCost CRUD API with validations",
                  "GET/POST/PUT/DELETE /api/costs. 5 validations: amount>0, exchange_rate>0, INR auto-rate, recurring needs end date, end>start. amount_inr auto-computed.",
                  3, "High", ["backend", "phase-2", "sprint-8", "must-have"]),
            Story("Recurring cost handling — End date enforcement",
                  "Validation: recurring must have end_date. Recurring costs count in each month from cost_date to recurring_end_date for aggregations.",
                  2, "High", ["backend", "phase-2", "sprint-8", "must-have"]),
            Story("Multi-currency support for non-human costs",
                  "Currency selector, exchange rate input, INR auto-calculation. UI shows Amount + Rate + INR. INR auto-set 1.0.",
                  2, "High", ["backend", "frontend", "phase-2", "sprint-8", "must-have"]),
            Story("Non-human cost list and management UI",
                  "Cost table in project detail. Columns: date, description, category badge, amount, currency, rate, INR, recurring icon. Add/edit/delete. Category filter. Totals row.",
                  3, "High", ["frontend", "phase-2", "sprint-8", "must-have"]),
            Story("Non-human cost audit logging",
                  "Track ALL field changes. CREATE/UPDATE/DELETE. changed_by from session.",
                  1, "Medium", ["backend", "phase-2", "sprint-8"]),
        ]
    )
    epics.append(ep13)

    # ── EP-14: Revenue & Margin Calculations ──
    ep14 = Epic(
        title="Revenue & Margin Calculations",
        description="Projected revenue, actual revenue, margin calculations at project/client/company levels, and bench cost.\n\n**Sprint:** 8–9 | **Stories:** 6 | **SP:** 16\n**Spec refs:** fsd/FSD.md §7.2–7.7, prd/PRD.md §5",
        labels=["phase-2"],
        priority="High",
        stories=[
            Story("Projected revenue calculation engine",
                  "Per-assignment: billability_pct/100 × working_days × 8 × billing_rate. Shadow excluded. INR conversion. Null rate excluded. SystemConfig for working_days/hours.",
                  3, "High", ["backend", "phase-2", "sprint-8", "must-have"]),
            Story("Actual revenue from invoices",
                  "SUM(amount_inr) where status ∈ {APPROVED, PAID}. Period filtering (monthly/quarterly/yearly). Source of truth for reporting.",
                  2, "High", ["backend", "phase-2", "sprint-9", "must-have"]),
            Story("Margin calculation — Projected and actual",
                  "Total Cost = Resource Cost + Non-Human Cost. Projected Margin = Projected Revenue - Total Cost. Actual Margin = Actual Revenue - Total Cost. Margin % with zero-revenue handling.",
                  3, "High", ["backend", "phase-2", "sprint-9", "must-have"]),
            Story("Bench cost calculation",
                  "Daily = loaded_cost_monthly/22. Total = daily × days_on_bench. Company total. GET /api/dashboard/bench-costs. Per-resource in availability.",
                  2, "Medium", ["backend", "phase-2", "sprint-9"]),
            Story("Client-level financial aggregation",
                  "GET /api/clients/:id/financials. SUM revenue, cost, margin across all client projects. Resource count. CEO/CTO/Finance restricted.",
                  3, "Medium", ["backend", "phase-2", "sprint-9"]),
            Story("Company-level financial aggregation",
                  "GET /api/dashboard/financials. Total projected/actual revenue, resource cost, non-human cost, bench cost, margins. Breakdown by project type. CEO/CTO/Finance.",
                  3, "Medium", ["backend", "phase-2", "sprint-9"]),
        ]
    )
    epics.append(ep14)

    # ── EP-15: Financial Dashboards ──
    ep15 = Epic(
        title="Financial Dashboards",
        description="Revenue, cost, and margin visual dashboards for Finance, CEO, CTO.\n\n**Sprint:** 9 | **Stories:** 4 | **SP:** 14\n**Spec refs:** fsd/FSD.md §9, prd/PRD.md §7",
        labels=["phase-2"],
        priority="Medium",
        stories=[
            Story("Financial dashboard data API — Revenue, cost, margin",
                  "GET /api/dashboard/financial. Revenue summary, cost summary, margin summary, top projects/clients, monthly trends (6 months). CEO/CTO/Finance. <2s response.",
                  3, "Medium", ["backend", "phase-2", "sprint-9", "must-have"]),
            Story("Financial dashboard UI — Revenue vs cost widgets",
                  "Revenue/cost/margin KPI cards. Revenue vs cost bar chart. Revenue by type pie chart. Monthly trend line chart. Top projects table. Drill-down links. Responsive.",
                  5, "Medium", ["frontend", "phase-2", "sprint-9", "must-have"]),
            Story("Project financial summary — Projected vs actual",
                  "Financial section on project detail (CEO/CTO/Finance, configurable DM). Projected/actual revenue, resource/non-human cost, margins. Hidden for unauthorized.",
                  3, "Medium", ["frontend", "phase-2", "sprint-9"]),
            Story("Client financial summary view",
                  "Financial section on client detail (CEO/CTO/Finance). Total billing, revenue, cost, margin. Revenue by project breakdown.",
                  3, "Medium", ["frontend", "phase-2", "sprint-9"]),
        ]
    )
    epics.append(ep15)

    # ── EP-16: Alert Engine ──
    ep16 = Epic(
        title="Alert Engine",
        description="In-app alert system with 6 alert types, scheduled jobs, notification panel with deep-linking.\n\n**Sprint:** 10 | **Stories:** 8 | **SP:** 18\n**Spec refs:** fsd/FSD.md §2.13, §12, prd/PRD.md §7",
        labels=["phase-3"],
        priority="Medium",
        stories=[
            Story("Alert database schema",
                  "Migration: alert table (10 fields). ENUM severity (INFO/WARNING/CRITICAL). FK to user. Indexes on recipient, type, is_read.",
                  2, "Highest", ["database", "phase-3", "sprint-10", "must-have"]),
            Story("Alert engine — Contract expiry alerts",
                  "Daily job: T&M/Onboarding with contract_end_date. Fires at 30d (WARNING) and 7d (CRITICAL). Recipients: DM/CTO/CEO. No duplicates. Deep-link to project.",
                  3, "Medium", ["backend", "infrastructure", "phase-3", "sprint-10", "must-have"]),
            Story("Alert engine — Bench duration alerts",
                  "Daily job: bench resources > 7d (configurable). Recipients: DM/CTO/HR. WARNING (7-14d), CRITICAL (>14d). Deep-link to resource.",
                  2, "Medium", ["backend", "infrastructure", "phase-3", "sprint-10", "must-have"]),
            Story("Alert engine — Over-allocation alerts",
                  "Event-driven: on assignment create/update when total >100%. Recipients: PM/DM. WARNING. Deep-link to resource.",
                  2, "Medium", ["backend", "phase-3", "sprint-10", "must-have"]),
            Story("Alert engine — Milestone overdue alerts",
                  "Daily job: FP milestones where planned_date < today AND status = PLANNED. Recipients: PM/DM. WARNING/CRITICAL. Deep-link to milestone.",
                  2, "Medium", ["backend", "infrastructure", "phase-3", "sprint-10", "must-have"]),
            Story("Alert engine — Utilization drop alerts",
                  "Weekly Monday job: company utilization < 70% (configurable). Recipients: CTO/CEO. WARNING. Deep-link to dashboard.",
                  2, "Medium", ["backend", "infrastructure", "phase-3", "sprint-10", "must-have"]),
            Story("Alert engine — Assignment auto-released alerts",
                  "Triggered by auto-release job. Per released assignment. Recipients: PM/DM. INFO. Deep-link to assignment.",
                  2, "Medium", ["backend", "phase-3", "sprint-10", "must-have"]),
            Story("Alert notification UI — Bell icon, panel, mark read, dismiss",
                  "Bell with unread badge. Dropdown panel (50 alerts). Severity colors. Mark read, dismiss, mark all read. Deep-link on click. Type filter. Poll every 60s.",
                  3, "Medium", ["frontend", "phase-3", "sprint-10", "must-have"]),
        ]
    )
    epics.append(ep16)

    # ── EP-17: Bench & Availability Forecasting ──
    ep17 = Epic(
        title="Bench & Availability Forecasting",
        description="Bench management dashboard, 30/60/90-day availability forecasting, partial availability identification.\n\n**Sprint:** 11 | **Stories:** 3 | **SP:** 8\n**Spec refs:** fsd/FSD.md §7.6, §9, prd/PRD.md §7",
        labels=["phase-3"],
        priority="Medium",
        stories=[
            Story("Bench management dashboard — Cost, duration, list",
                  "Bench page: resource list with designation, days on bench, daily/total cost. Summary cards. Sort/filter. Cost columns restricted. Color-coded duration.",
                  3, "Medium", ["backend", "frontend", "phase-3", "sprint-11", "must-have"]),
            Story("Availability forecasting — 30/60/90 day release view",
                  "Forecasting page: time horizon toggles. Upcoming releases table with resource, project, allocation, release date. Auto-release aware. Summary counts.",
                  3, "Medium", ["backend", "frontend", "phase-3", "sprint-11", "must-have"]),
            Story("Partial availability identification",
                  "API/filter: resources with 0 < allocation < 100%. Shows spare capacity, projects, skills. Sortable by spare capacity. Integrated into forecasting.",
                  2, "Medium", ["backend", "phase-3", "sprint-11"]),
        ]
    )
    epics.append(ep17)

    # ── EP-18: Configurable Access & Admin ──
    ep18 = Epic(
        title="Configurable Access & Admin",
        description="Per-user permission overrides, admin UI for role permissions, system configuration management.\n\n**Sprint:** 11–12 | **Stories:** 4 | **SP:** 11\n**Spec refs:** fsd/FSD.md §2.2, §2.14, prd/PRD.md §7",
        labels=["phase-3"],
        priority="Low",
        stories=[
            Story("UserPermissionOverride schema and API",
                  "Migration: user_permission_override table. Unique (user_id, data_type). Only for is_configurable data types. CRUD API. Middleware updated to check overrides first.",
                  3, "Low", ["backend", "database", "phase-3", "sprint-11"]),
            Story("Configurable access admin UI",
                  "Admin page: roles × data types grid. Configurable cells highlighted. Click to change. User overrides section. Visual diff from role default.",
                  3, "Low", ["frontend", "phase-3", "sprint-11"]),
            Story("SystemConfig admin UI — All threshold settings",
                  "Admin page: all config keys grouped by category. Inline edit. Validation. Reset to default. Changes immediate. Audit logged.",
                  3, "Low", ["frontend", "phase-3", "sprint-12"]),
            Story("SystemConfig API — Get/update all configurable settings",
                  "GET/PUT /api/config/:key. CEO/CTO only. Validation per key type. Audit logged. Services use API not hardcoded values.",
                  2, "Low", ["backend", "phase-3", "sprint-12"]),
        ]
    )
    epics.append(ep18)

    # ── EP-19: Historical Queries & Audit Viewer ──
    ep19 = Epic(
        title="Historical Queries & Audit Viewer",
        description="Point-in-time state reconstruction, historical query API, and audit log browser.\n\n**Sprint:** 12 | **Stories:** 3 | **SP:** 11\n**Spec refs:** fsd/FSD.md §13, prd/PRD.md §7",
        labels=["phase-3"],
        priority="Low",
        stories=[
            Story("Point-in-time reconstruction engine",
                  "Replay audit log backwards from current state. Supports all tracked entities. Handles CREATE/DELETE. <5s for 1000 audit entries. Reusable service.",
                  5, "Low", ["backend", "phase-3", "sprint-12"]),
            Story("Historical query API — View system state at any past date",
                  "GET /api/history/:entityType/:entityId?date=YYYY-MM-DD. Returns reconstructed state. Change timeline endpoint. CEO/CTO only.",
                  3, "Low", ["backend", "phase-3", "sprint-12"]),
            Story("Audit log viewer UI — Browse by entity, user, date range",
                  "Audit page: table with timestamp, entity, action, field, old/new value, user. Filters: entity type, date range, user, action. Search. Pagination. Point-in-time query.",
                  3, "Low", ["frontend", "phase-3", "sprint-12"]),
        ]
    )
    epics.append(ep19)

    return epics


def fetch_existing_tickets():
    """Fetch all existing tickets in the project to enable resume."""
    existing = {}  # summary -> key
    start = 0
    while True:
        result = make_request("GET", f"search/jql?jql=project%20%3D%20{PROJECT_KEY}&startAt={start}&maxResults=100&fields=summary,issuetype")
        if not result:
            break
        issues = result.get("issues", [])
        if not issues:
            break
        for issue in issues:
            existing[issue["fields"]["summary"]] = issue["key"]
        start += len(issues)
        if start >= result.get("total", 0):
            break
    return existing


def main():
    if not all([JIRA_BASE_URL, JIRA_EMAIL, API_TOKEN]):
        print("ERROR: Set JIRA_BASE_URL, JIRA_EMAIL, and API_TOKEN environment variables.")
        sys.exit(1)

    print(f"Jira: {JIRA_BASE_URL}")
    print(f"Project: {PROJECT_KEY}")
    print(f"User: {JIRA_EMAIL}")
    print()

    # Verify connectivity
    print("Verifying Jira connectivity...")
    result = make_request("GET", "myself")
    if not result:
        print("FATAL: Cannot connect to Jira. Check JIRA_BASE_URL and credentials.")
        sys.exit(1)
    print(f"Authenticated as: {result.get('displayName', 'unknown')}")

    # Fetch existing tickets for resume
    print("Checking for existing tickets (resume mode)...")
    existing = fetch_existing_tickets()
    if existing:
        print(f"  Found {len(existing)} existing tickets — will skip duplicates.")
    print()

    epics = build_all_epics()
    total_stories = sum(len(e.stories) for e in epics)
    total_points = sum(sum(s.story_points for s in e.stories) for e in epics)
    print(f"Creating {len(epics)} Epics with {total_stories} Stories ({total_points} story points)")
    print("=" * 60)

    created_epics = 0
    created_stories = 0
    skipped = 0
    failed = []

    for i, epic in enumerate(epics, 1):
        print(f"\n[{i}/{len(epics)}] Epic: {epic.title}")

        # Check if epic already exists
        if epic.title in existing:
            epic.jira_key = existing[epic.title]
            print(f"  ↩ SKIP (exists: {epic.jira_key})")
            skipped += 1
        else:
            epic_key = create_issue("Epic", epic.title, epic.description, epic.priority, epic.labels)
            if epic_key:
                epic.jira_key = epic_key
                created_epics += 1
                print(f"  ✓ {epic_key}: {epic.title}")
            else:
                failed.append(f"Epic: {epic.title}")
                print(f"  ✗ FAILED: {epic.title}")
                continue

        for j, story in enumerate(epic.stories, 1):
            # Check if story already exists
            if story.title in existing:
                story.jira_key = existing[story.title]
                print(f"  [{j}/{len(epic.stories)}] ↩ SKIP {story.jira_key}: {story.title[:55]}...")
                skipped += 1
                continue

            print(f"  [{j}/{len(epic.stories)}] {story.title[:60]}...")
            story_key = create_issue(
                "Story", story.title, story.description, story.priority,
                story.labels, story.story_points, epic.jira_key
            )
            if story_key:
                story.jira_key = story_key
                created_stories += 1
                print(f"    ✓ {story_key} ({story.story_points} pts)")
            else:
                failed.append(f"Story: {story.title} (under {epic.title})")
                print(f"    ✗ FAILED")
            time.sleep(0.5)  # Rate limit

    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Epics created:   {created_epics}")
    print(f"Stories created:  {created_stories}")
    print(f"Skipped (exist):  {skipped}")
    print(f"Total in Jira:    {created_epics + created_stories + skipped}")
    if failed:
        print(f"\nFailed ({len(failed)}):")
        for f in failed:
            print(f"  - {f}")
    else:
        print("\nAll tickets created successfully!")

    # Output key mapping
    print("\n--- Jira Key Mapping ---")
    for epic in epics:
        if epic.jira_key:
            print(f"\n{epic.jira_key} [Epic] {epic.title}")
            for story in epic.stories:
                if story.jira_key:
                    print(f"  {story.jira_key} [{story.story_points}pt] {story.title}")


if __name__ == "__main__":
    main()
