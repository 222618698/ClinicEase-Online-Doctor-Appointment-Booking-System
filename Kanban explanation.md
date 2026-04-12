# kanban_explanation.md – Kanban Board Definition and Purpose

## ClinicEase Online Doctor Appointment Booking System

---

## 1. What is a Kanban Board?

A **Kanban board** is a visual project management tool that represents the flow of work through a series of stages, displayed as columns on a board. Each task or work item is shown as a card that moves from left to right across the columns as it progresses — from "not started" all the way to "done."

The word *Kanban* comes from Japanese and means "visual signal" or "signboard." It was originally developed by Toyota in the 1940s to improve manufacturing efficiency by making the status of every task visible to the entire team at a glance.

In software development, a Kanban board typically includes columns such as **Backlog, Ready, In Progress, In Review, Testing,** and **Done**. Each card on the board represents a task, user story, or bug, and contains key information like who is responsible for it, how much effort it requires, and what its current status is.

---

## 2. ClinicEase Kanban Board — Column Structure

The ClinicEase Kanban board uses the following custom column structure, adapted from the GitHub Team Planning template:

| Column | Purpose | WIP Limit |
|---|---|---|
| **📋 Backlog** | All user stories and tasks that have been identified but not yet scheduled for the current sprint. Contains US-005 to US-018 not in Sprint 1. | No limit |
| **🎯 Ready** | Stories that have been fully defined, have acceptance criteria confirmed, and are ready to be picked up by the developer. | 5 cards |
| **🔨 In Progress** | Work that is actively being developed right now. Keeping this column small ensures focused, quality work. | 3 cards |
| **🚧 Blocked** | Tasks that cannot proceed due to an unresolved dependency, missing information, or external blocker. | 3 cards |
| **👀 In Review** | Completed code awaiting peer review or pull request approval before moving to testing. | 3 cards |
| **🧪 Testing** | Features that have passed code review and are being validated against the test cases defined in TEST_CASES.md. | 3 cards |
| **✅ Done** | Fully completed, tested, and deployed features. A card only reaches Done when all acceptance criteria are met and all test cases pass. | No limit |

---

## 3. How the Board Visualises Workflow

The ClinicEase Kanban board visualises workflow in the following ways:

**Left-to-right flow:** Every user story starts in the Backlog column and moves rightward through Ready → In Progress → Blocked (if needed) → In Review → Testing → Done. This makes the journey of every feature immediately visible without reading any documentation.

**Sprint filtering:** The board can be filtered by the Sprint iteration field to show only Sprint 1 cards (US-001 to US-004, US-015 to US-017). This gives a clear picture of what must be completed within the current two-week window.

**MoSCoW priority labels:** Cards are colour-coded with `must-have` (red), `should-have` (orange), and `could-have` (yellow) labels. At a glance, anyone looking at the board can see which tasks are critical to the MVP.

**Story point field:** Each card displays its story point value, making it easy to see the total effort currently In Progress and compare it against the sprint's planned velocity of 19 points.

---

## 4. How the Board Limits Work-In-Progress (WIP)

WIP limits are one of the most important features of a Kanban board. Without WIP limits, a developer can start many tasks simultaneously, leading to context-switching, half-finished work, and slower overall delivery.

For ClinicEase, WIP limits are set as follows:

- **In Progress:** Maximum 3 cards. As a solo developer, having more than 3 tasks in active development simultaneously leads to context-switching and lower code quality. Keeping this at 3 forces completion before starting something new.
- **In Review:** Maximum 3 cards. If too many items are waiting for review, it signals that the review process has become a bottleneck and needs to be addressed before more work is started.
- **Testing:** Maximum 3 cards. This ensures the testing phase does not pile up with untested features, which would delay the sprint's Definition of Done.
- **Blocked:** Maximum 3 cards. If more than 3 items are blocked simultaneously, it is a signal that there is a systemic problem (e.g., a missing API, an unresolved design decision) that must be resolved before development continues.

When any column hits its WIP limit, work stops flowing into that column until a card moves out. This creates a "pull" system rather than a "push" system — new work is only started when there is capacity, not just because a new requirement arrives.

---

## 5. How the Board Supports Agile Principles

| Agile Principle | How the ClinicEase Board Supports It |
|---|---|
| **Continuous delivery of working software** | The Testing and Done columns ensure only fully verified features are marked complete. Each sprint ends with deployable, tested code. |
| **Responding to change** | Cards can be moved between sprints or re-prioritised in the Backlog at any time. The board makes the impact of reprioritisation immediately visible. |
| **Simplicity — maximising work not done** | The WIP limits and Backlog column prevent over-engineering. Only cards in the Ready column are actively worked on — not everything at once. |
| **Sustainable pace** | The In Progress WIP limit of 3 prevents a developer from overloading themselves, which is especially important for a solo project. |
| **Transparency** | Every stakeholder can view the GitHub Project board and see exactly what is being worked on, what is blocked, and what is done — without needing a status meeting. |
| **Iterative improvement** | At the end of each sprint, the board is reviewed. Cards still in Blocked or In Review at sprint end are analysed to understand what caused the delay and how to prevent it next sprint. |

---


*Document prepared by: [Sithembiso Lungisani Mthebu] | [222618698] | CPUT | March 2026*