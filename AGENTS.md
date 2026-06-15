# AGENTS.md — Repository Knowledge

## Project
**Resource Intelligence & Project Economics Platform** — IT services operational visibility for resources, projects, clients, and financials.

## Key Files
- `prd/PRD.md` — Product Requirements Document (v1.1)
- `fsd/FSD.md` — Functional Specification Document (v1.0, 797 lines, 14 entities)
- `tickets/` — Generated Jira ticket markdown files (19 epics) + creation script

## Jira Configuration
- **Site:** `https://sspl-organisation.atlassian.net`
- **Project Key:** `OHRIPA`
- **Email:** `nitesh.vaishnav@sculptsoft.com`
- **Custom Fields:** `customfield_10016` = Story Point Estimate
- **Issue Types:** Epic, Story, Task, Bug, Subtask
- **Search API:** Use `/rest/api/3/search/jql` (old `/rest/api/3/search` is deprecated)

## Jira Tickets Created
- **19 Epics**, **109 Stories** = **128 total tickets** (OHRIPA-3 through OHRIPA-130)
- **280 story points** across **3 phases**, **12 sprints**
- Phase 1 (Foundation): Sprints 1–5 — Auth, Client, Project, Resource, Assignment, Dashboards, Worklog
- Phase 2 (Financial): Sprints 6–9 — Costing, Milestones, Invoices, Non-Human Costs, Revenue/Margin
- Phase 3 (Intelligence): Sprints 10–12 — Alerts, Bench/Forecasting, Access Config, Historical Queries

## Entity Model (14 entities)
Role, RolePermission, User, Client, Resource (+ ResourceTag), Project, Assignment, Milestone, Invoice, NonHumanCost, Worklog, AuditLog, Alert, SystemConfig
