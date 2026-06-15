# Jira Tickets — Resource Intelligence & Project Economics Platform

## Overview

| Metric | Value |
|---|---|
| **Total Epics** | 19 |
| **Total Stories** | 109 |
| **Total Story Points** | 281 |
| **Phases** | 3 |
| **Sprints (2-week, ~20pts/dev)** | 12 |

## Sprint Plan

| Sprint | Theme | Epics | Stories | Points |
|---|---|---|---|---|
| Sprint 1 | Infrastructure & Auth | EP-1 Auth & Roles, EP-9 Audit Logging | 9 | 20 |
| Sprint 2 | Core Entities — Client & Resource | EP-2 Client Management, EP-4 Resource Management (partial) | 11 | 24 |
| Sprint 3 | Core Entities — Project & Resource | EP-3 Project Management, EP-4 Resource Management (remainder) | 13 | 30 |
| Sprint 4 | Allocation & Assignments | EP-5 Allocation & Assignment Tracking | 10 | 27 |
| Sprint 5 | Dashboards & Worklog | EP-6 Utilization Dashboards, EP-7 Resource Availability, EP-8 Employee Worklog | 13 | 38 |
| Sprint 6 | Financial Foundation | EP-10 Resource Costing, EP-11 Milestone Management (partial) | 8 | 18 |
| Sprint 7 | Milestones & Invoicing | EP-11 Milestone (remainder), EP-12 Invoice Management | 11 | 25 |
| Sprint 8 | Non-Human Costs & Revenue | EP-13 Non-Human Costs, EP-14 Revenue & Margin (partial) | 10 | 22 |
| Sprint 9 | Financial Aggregation & Dashboards | EP-14 Revenue & Margin (remainder), EP-15 Financial Dashboards | 7 | 22 |
| Sprint 10 | Alert Engine | EP-16 Alert Engine | 8 | 18 |
| Sprint 11 | Bench, Forecasting & Access | EP-17 Bench & Forecasting, EP-18 Configurable Access | 7 | 19 |
| Sprint 12 | Historical Queries & Polish | EP-19 Historical Queries & Audit Viewer | 3 | 11 |

## Epic Index

| # | Epic | Phase | Stories | Points | Sprint |
|---|---|---|---|---|---|
| EP-1 | Auth & Roles | 1 | 6 | 15 | 1 |
| EP-2 | Client Management | 1 | 7 | 15 | 2 |
| EP-3 | Project Management | 1 | 9 | 26 | 3 |
| EP-4 | Resource Management | 1 | 8 | 19 | 2–3 |
| EP-5 | Allocation & Assignment Tracking | 1 | 10 | 27 | 4 |
| EP-6 | Utilization Dashboards | 1 | 5 | 16 | 5 |
| EP-7 | Resource Availability | 1 | 3 | 10 | 5 |
| EP-8 | Employee Worklog | 1 | 5 | 12 | 5 |
| EP-9 | Audit Logging & System Config | 1 | 3 | 5 | 1 |
| EP-10 | Resource Costing & Billing Rates | 2 | 5 | 11 | 6 |
| EP-11 | Milestone Management | 2 | 7 | 16 | 6–7 |
| EP-12 | Invoice Management | 2 | 7 | 18 | 7 |
| EP-13 | Non-Human Cost Management | 2 | 6 | 13 | 8 |
| EP-14 | Revenue & Margin Calculations | 2 | 6 | 16 | 8–9 |
| EP-15 | Financial Dashboards | 2 | 4 | 14 | 9 |
| EP-16 | Alert Engine | 3 | 8 | 18 | 10 |
| EP-17 | Bench & Availability Forecasting | 3 | 3 | 8 | 11 |
| EP-18 | Configurable Access & Admin | 3 | 4 | 11 | 11 |
| EP-19 | Historical Queries & Audit Viewer | 3 | 3 | 11 | 12 |

## Dependency Chain

```
EP-9 (Audit) ──┐
               ├──→ EP-1 (Auth) ──→ EP-2 (Client) ──→ EP-3 (Project) ──┐
               │                    EP-4 (Resource) ──────────────────────┤
               │                                                          ▼
               │                                              EP-5 (Assignment) ──→ EP-6 (Utilization)
               │                                                    │               EP-7 (Availability)
               │                                                    │               EP-8 (Worklog)
               │                                                    ▼
               │                                              EP-10 (Costing) ──→ EP-11 (Milestone) ──→ EP-12 (Invoice)
               │                                                                  EP-13 (Non-Human Cost)
               │                                                                        │
               │                                                                        ▼
               │                                                                  EP-14 (Revenue/Margin) ──→ EP-15 (Financial Dashboards)
               │                                                                        │
               │                                                                        ▼
               └─────────────────────────────────────────────────────────────────→ EP-16 (Alerts)
                                                                                  EP-17 (Bench/Forecast)
                                                                                  EP-18 (Access Config)
                                                                                  EP-19 (Historical)
```
