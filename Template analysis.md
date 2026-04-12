# template_analysis.md – GitHub Project Template Analysis and Selection

## ClinicEase Online Doctor Appointment Booking System

---

## 1. GitHub Project Templates — Comparison Table

| Feature | Basic Kanban | Automated Kanban | Bug Triage | Team Planning |
|---|---|---|---|---|
| **Default Columns** | To Do, In Progress, Done | To Do, In Progress, Done | Needs Triage, High Priority, Low Priority, Closed | Backlog, Ready, In Progress, In Review, Done |
| **Number of Columns** | 3 | 3 | 4 | 5 |
| **Automation Features** | None — all movement is manual | Auto-moves issues to "In Progress" when a PR is opened. Auto-moves to "Done" when PR is merged or issue is closed. | Auto-moves issues to "Closed" when an issue is closed. Supports triage labelling. | Auto-moves issues based on status updates. Supports iteration (sprint) tracking. |
| **Supports Sprints / Milestones** | No built-in sprint support | Partial — can be linked to milestones manually | No — focused on bug tracking only | Yes — built-in iteration fields for sprint planning |
| **WIP Limiting** | Not built-in | Not built-in | Not built-in | Supported via iteration capacity settings |
| **Issue Linking** | Manual | Automatic via PR events | Manual with label filtering | Automatic with full issue and PR linking |
| **Best For** | Small solo projects with simple workflows | Teams doing continuous delivery with frequent PRs | Projects with many bugs needing triage and prioritisation | Scrum/Agile teams running formal sprints with planning sessions |
| **Custom Fields** | Limited | Limited | Limited | Yes — supports custom fields (priority, story points, status) |
| **Agile Suitability** | Low — no sprint or backlog support | Medium — automation helps but lacks sprint structure | Low — not designed for feature development | High — designed specifically for Agile/Scrum workflows |
| **Ease of Setup** | Very easy | Easy | Easy | Moderate — requires configuration of iterations and fields |
| **Suitable for ClinicEase** | No | Partially | No | Yes ✅ |

---

## 2. Template Justification — Why Team Planning Was Selected

After evaluating all four templates, **Team Planning** was selected as the most suitable template for ClinicEase for the following reasons:

### Reason 1: Built-in Sprint / Iteration Support
ClinicEase follows an Agile methodology with clearly defined sprints established in Assignment 6. The Team Planning template supports **iteration fields** that map directly to the Sprint 1, Sprint 2, and Sprint 3 milestones already created. Basic Kanban and Automated Kanban have no sprint concept, making them unsuitable for a project with a defined sprint backlog.

### Reason 2: Five-Column Workflow Matches Development Reality
The default five columns — **Backlog, Ready, In Progress, In Review, Done** — reflect the actual lifecycle of a ClinicEase task more accurately than the basic three-column layout. For example, a user story like US-004 (Book an Appointment) must go through development, code review, and testing before it can be marked Done. The "In Review" column captures this intermediate state that Basic and Automated Kanban miss entirely.

### Reason 3: Custom Fields for Story Points and Priority
Team Planning supports **custom fields** such as story points (Fibonacci: 1, 2, 3, 5, 8) and MoSCoW priority labels. These fields were already defined in the AGILE_PLANNING.md from Assignment 6 and can be mapped directly into the GitHub Project without duplication of effort.

### Reason 4: Full Issue and PR Linking
Team Planning automatically links GitHub Issues (the 18 user stories created in Assignment 6) and pull requests to board cards. This provides **end-to-end traceability** from stakeholder requirement → user story → task → code commit → done — which directly satisfies the assignment's traceability requirement.

### Reason 5: Automation Reduces Manual Overhead
As a solo developer playing multiple Scrum roles, automation is essential. Team Planning auto-moves issues when their status changes, reducing the time spent manually dragging cards between columns.

### Why Bug Triage Was Rejected
Bug Triage is designed for reactive defect management, not proactive feature development. ClinicEase is in active development — the primary need is to track feature delivery, not triage reported bugs. Bug Triage columns (Needs Triage, High Priority, Low Priority) do not represent a development workflow.

### Why Basic Kanban Was Rejected
Basic Kanban requires all movement to be manual and has no automation, no sprint support, and no custom fields. For a project with 18 user stories across 4 planned sprints, this would create significant manual overhead with no traceability benefit.

### Why Automated Kanban Was Partially Considered
Automated Kanban's PR-triggered automation is useful but it only has three columns and no sprint/iteration support. It would require heavy customisation to reach the same functionality that Team Planning provides out of the box.

---

## 3. Customisation Plan for ClinicEase

After selecting Team Planning, the following customisations were made to adapt it to ClinicEase's specific workflow:

| Customisation | Reason |
|---|---|
| Added **"Testing"** column between "In Review" and "Done" | ClinicEase has 18 test cases (TEST_CASES.md). A dedicated testing column ensures no feature is marked Done before its test cases pass. |
| Added **"Blocked"** column | Some tasks depend on others (e.g., booking UI depends on the API endpoint). A Blocked column makes dependencies visible without polluting the In Progress column. |
| Added **"Story Points"** custom field (Fibonacci) | Enables sprint velocity tracking as defined in AGILE_PLANNING.md |
| Added **"MoSCoW Priority"** custom field | Maps to the Must-have / Should-have / Could-have labels from the product backlog |
| Added **"Sprint"** iteration field | Links each issue to Sprint 1, Sprint 2, or Sprint 3 milestones |
| Applied labels: `must-have`, `should-have`, `could-have`, `user-story`, `non-functional`, `sprint-1` | Provides visual filtering and traceability to Assignment 4 requirements |

---

*Document prepared by: [Sithembiso LUngisani Mthembu] | [222618698] | CPUT | March 2026*