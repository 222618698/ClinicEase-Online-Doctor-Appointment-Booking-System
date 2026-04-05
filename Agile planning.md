# AGILE_PLANNING.md – Agile User Stories, Backlog, and Sprint Planning

## ClinicEase Online Doctor Appointment Booking System

---

## 1. User Stories

> Format: *"As a [role], I want [action] so that [benefit]."*
> All stories follow INVEST criteria and are traceable to Assignment 4 requirements and Assignment 5 use cases.

### User Stories Table

| Story ID | User Story | Acceptance Criteria | Priority | Linked Requirement | Linked Use Case |
|---|---|---|---|---|---|
| US-001 | As a **patient**, I want to register an account so that I can access the booking system securely. | Registration validates email format, enforces 8-char min password, shows POPIA consent checkbox. Account created within 3 seconds. Welcome email sent. | High | FR-01 | UC-01 |
| US-002 | As a **patient**, I want to log in with my email and password so that I can access my personal dashboard. | Login succeeds with correct credentials within 2 seconds. Failed login shows clear error. Account locks after 5 failed attempts. | High | FR-01 | UC-01 |
| US-003 | As a **patient**, I want to search for a doctor by name or specialisation so that I can find the right doctor for my condition. | Search results appear within 2 seconds. Each result shows doctor name, specialisation, and next available slot. Fully booked doctors are clearly marked. | High | FR-02 | UC-02 |
| US-004 | As a **patient**, I want to book an available appointment slot so that I can secure a consultation without visiting the clinic. | Booking confirmed only if slot is available. Confirmation email sent within 60 seconds. Double-booking prevented by database constraint. | High | FR-03 | UC-03 |
| US-005 | As a **patient**, I want to cancel or reschedule my appointment so that I can adjust my plans without losing my place. | Cancellation releases the slot immediately. Rescheduling assigns new slot and releases old one. Patient receives email notification within 60 seconds. | High | FR-04 | UC-04 |
| US-006 | As a **patient**, I want to receive an automatic reminder 24 hours and 1 hour before my appointment so that I never miss a consultation. | Reminders delivered via email at exactly 24h and 1h before the appointment. No reminder sent for cancelled appointments. Caregiver also notified if linked. | High | FR-05 | UC-05 |
| US-007 | As a **patient**, I want to set up a medication reminder schedule so that I never forget to take my daily medication. | Medication name, dosage, and reminder time saved successfully. Daily reminder sent at configured time. Refill alert sent 7 days before medication runs out. | High | FR-06 | UC-06 |
| US-008 | As a **doctor**, I want to view my full daily and weekly appointment schedule so that I can prepare for each consultation. | Dashboard loads within 2 seconds. Appointments listed in chronological order with patient name, time, and status. Clicking an appointment shows patient history. | High | FR-08 | UC-07 |
| US-009 | As a **doctor**, I want to schedule a follow-up blood test or procedure for a patient so that they are automatically reminded when it is due. | Procedure saved with date, time, and preparation notes. Patient receives a reminder 48 hours before. Reminder includes procedure name and preparation instructions. | High | FR-07 | UC-05 |
| US-010 | As a **doctor**, I want to view and update a patient's medical records after a consultation so that their history is always accurate and complete. | Full patient history loaded within 1 second. Consultation notes saved successfully. Records never deleted, only archived. | High | FR-10 | UC-07 |
| US-011 | As a **receptionist**, I want to create, reschedule, and cancel appointments on behalf of patients so that I can assist patients who cannot use the online system. | All booking actions complete within 2 seconds. Walk-in patient added to queue within 1 minute. Patient receives email notification of any changes. | High | FR-09 | UC-04 |
| US-012 | As a **clinic administrator**, I want to manage doctor and staff accounts so that only authorised users have system access. | Admin can activate or deactivate any account within 2 clicks. All admin actions logged with timestamp and admin user ID. | Medium | FR-11 | UC-08 |
| US-013 | As a **clinic administrator**, I want to generate operational reports so that I can monitor clinic performance and identify improvement areas. | Reports generated on demand. Include total appointments, no-show rate, and appointments per doctor. Downloadable as CSV or PDF. | Medium | FR-11 | UC-08 |
| US-014 | As a **caregiver**, I want to book and manage appointments on behalf of a dependent family member so that they receive proper care even if they cannot manage it themselves. | Caregiver can search, book, and cancel on behalf of a linked patient. Caregiver receives appointment and medication reminders. Access limited to booking and reminders only. | Medium | FR-03, FR-05 | UC-03, UC-05 |
| US-015 | As an **IT staff member**, I want all user passwords stored as bcrypt hashes so that patient data is protected against data breaches. | Password column in database contains only bcrypt hashes starting with `$2b$12$`. No plaintext passwords in logs or database. | High | NFR-SEC1 | — |
| US-016 | As an **IT staff member**, I want all connections encrypted with HTTPS/TLS so that patient data cannot be intercepted in transit. | All HTTP requests redirect to HTTPS with a 301 response. TLS version confirmed as 1.2 or higher via SSL audit. | High | NFR-SEC2 | — |
| US-017 | As a **patient**, I want the system to load any page within 3 seconds so that I am not frustrated by slow performance. | Lighthouse performance score ≥ 80 for all key pages. No page load exceeds 3 seconds on a 10 Mbps connection. | High | NFR-P1 | — |
| US-018 | As a **system administrator**, I want the platform to support 500 concurrent users so that the system remains stable during peak hours. | Load test with 500 virtual users produces average API response time under 2 seconds. Error rate below 1%. | Medium | NFR-S1 | — |

---

## 2. Product Backlog

### MoSCoW Prioritisation

> Story points follow Fibonacci sequence: 1, 2, 3, 5, 8, 13

| Story ID | User Story Summary | MoSCoW | Story Points | Dependencies |
|---|---|---|---|---|
| US-001 | Patient registers an account | Must-have | 2 | None |
| US-002 | Patient logs in securely | Must-have | 2 | US-001 |
| US-003 | Patient searches for a doctor | Must-have | 3 | US-002 |
| US-004 | Patient books an appointment | Must-have | 5 | US-003 |
| US-005 | Patient cancels or reschedules | Must-have | 3 | US-004 |
| US-006 | Automatic appointment reminders | Must-have | 5 | US-004 |
| US-007 | Medication reminder schedule | Must-have | 5 | US-001 |
| US-008 | Doctor views daily schedule | Must-have | 3 | US-002 |
| US-009 | Doctor schedules blood test/procedure | Must-have | 3 | US-008 |
| US-010 | Doctor views and updates patient records | Must-have | 5 | US-008 |
| US-011 | Receptionist manages appointments | Must-have | 5 | US-004 |
| US-015 | bcrypt password hashing | Must-have | 2 | US-001 |
| US-016 | HTTPS/TLS encryption | Must-have | 2 | None |
| US-017 | Page load under 3 seconds | Must-have | 3 | US-003, US-004 |
| US-012 | Admin manages user accounts | Should-have | 3 | US-001 |
| US-013 | Admin generates reports | Should-have | 5 | US-004 |
| US-014 | Caregiver manages dependent's appointments | Should-have | 5 | US-004 |
| US-018 | Support 500 concurrent users | Could-have | 8 | US-004, US-006 |

### Prioritisation Justification

**Must-have stories (US-001 to US-011, US-015 to US-017)** form the core of the MVP. They directly address the highest-priority stakeholder concerns identified in Assignment 4 — patients needing to book without visiting the clinic, doctors needing a digital schedule, and the security requirements mandated by POPIA and IT staff. Without these, the system cannot function at all.

**Should-have stories (US-012, US-013, US-014)** add significant value but the system can operate without them in the first sprint. Admin reporting and caregiver access improve the system for administrators and family members but are not essential to the core patient-doctor booking flow.

**Could-have stories (US-018)** address scalability under high load. This is important for the long term but can be addressed after the core system is stable. Load testing and horizontal scaling are post-MVP concerns.

**Won't-have (this semester):** Medical aid API integration, native mobile app (iOS/Android), video consultation features, and online payment processing. These were identified as out of scope in the Assignment 3 SPECIFICATION.md and remain so.

---

## 3. Sprint Planning

### Sprint 1 Goal

> **"Deliver a working patient registration, login, doctor search, and appointment booking flow so that a patient can book a clinic appointment end-to-end without visiting the clinic."**

This sprint establishes the MVP core. By the end of Sprint 1, a patient should be able to register, log in, find a doctor, and book a confirmed appointment — with a confirmation email sent automatically. This directly addresses the most critical pain point identified in the stakeholder analysis: patients having no way to book online.

**Sprint Duration:** 2 weeks
**Sprint Velocity:** 18 story points

### Sprint 1 — Selected User Stories

| Story ID | User Story Summary | Story Points | Priority |
|---|---|---|---|
| US-001 | Patient registers an account | 2 | Must-have |
| US-002 | Patient logs in securely | 2 | Must-have |
| US-003 | Patient searches for a doctor | 3 | Must-have |
| US-004 | Patient books an appointment | 5 | Must-have |
| US-015 | bcrypt password hashing | 2 | Must-have |
| US-016 | HTTPS/TLS encryption | 2 | Must-have |
| US-017 | Page load under 3 seconds | 3 | Must-have |

**Total Story Points: 19**

---

### Sprint 1 — Task Breakdown

| Task ID | Story ID | Task Description | Assigned To | Estimated Hours | Status |
|---|---|---|---|---|---|
| T-001 | US-001 | Design and build patient registration form (React) | Dev Team | 4 | To Do |
| T-002 | US-001 | Develop POST /auth/register API endpoint with validation | Dev Team | 4 | To Do |
| T-003 | US-001 | Implement POPIA consent checkbox on registration form | Dev Team | 2 | To Do |
| T-004 | US-001 | Send welcome email on successful registration (Nodemailer) | Dev Team | 3 | To Do |
| T-005 | US-002 | Build login form UI with error messaging (React) | Dev Team | 3 | To Do |
| T-006 | US-002 | Develop POST /auth/login endpoint with JWT token issuance | Dev Team | 4 | To Do |
| T-007 | US-002 | Implement account lockout after 5 failed login attempts | Dev Team | 3 | To Do |
| T-008 | US-002 | Implement role-based dashboard redirect after login | Dev Team | 2 | To Do |
| T-009 | US-003 | Build doctor search UI with name and specialisation filters | Dev Team | 4 | To Do |
| T-010 | US-003 | Develop GET /doctors endpoint with query parameters | Dev Team | 4 | To Do |
| T-011 | US-003 | Display doctor cards with name, specialisation, and next slot | Dev Team | 3 | To Do |
| T-012 | US-004 | Build appointment booking form and slot selection UI | Dev Team | 5 | To Do |
| T-013 | US-004 | Develop POST /appointments endpoint with slot availability check | Dev Team | 5 | To Do |
| T-014 | US-004 | Implement database uniqueness constraint on time slots | Dev Team | 2 | To Do |
| T-015 | US-004 | Send booking confirmation email on successful booking | Dev Team | 3 | To Do |
| T-016 | US-015 | Configure bcrypt with cost factor 12 in auth service | Dev Team | 2 | To Do |
| T-017 | US-016 | Configure HTTPS and HTTP-to-HTTPS redirect on server | Dev Team | 2 | To Do |
| T-018 | US-017 | Run Lighthouse audit on all Sprint 1 pages and fix issues | Dev Team | 4 | To Do |
| T-019 | — | Set up PostgreSQL database schema (users, doctors, appointments, slots tables) | Dev Team | 4 | To Do |
| T-020 | — | Set up Node.js + Express project structure with modular folders | Dev Team | 3 | To Do |
| T-021 | — | Set up React project with routing and role-based protected routes | Dev Team | 3 | To Do |
| T-022 | — | Write unit tests for registration and login endpoints | Dev Team | 4 | To Do |
| T-023 | — | Write integration test for full booking flow (TC-005 from TEST_CASES.md) | Dev Team | 3 | To Do |
| T-024 | — | Deploy to staging environment and verify end-to-end flow | Dev Team | 3 | To Do |

**Total Estimated Hours: 80 hours**

---

### Sprint 1 — Definition of Done

A user story is considered **Done** when:
- All acceptance criteria from the User Stories table are met
- Code is reviewed and merged to the `main` branch via a pull request
- Relevant test cases from TEST_CASES.md pass successfully
- No critical bugs remain open
- The feature is deployed and working on the staging environment

---

### GitHub Project Setup Instructions

To manage this sprint using GitHub's built-in Agile tools:

1. **GitHub Issues:** Create one issue per user story (US-001 to US-018). Label each with its MoSCoW priority (`must-have`, `should-have`, `could-have`). Add the story point estimate in the issue description.
2. **GitHub Project Board:** Create a Project with columns: `Backlog` | `Sprint 1` | `In Progress` | `In Review` | `Done`. Move Sprint 1 stories (US-001 to US-004, US-015 to US-017) into the `Sprint 1` column.
3. **GitHub Milestones:** Create a milestone called `Sprint 1 – MVP Core Booking Flow` with a 2-week deadline. Link all Sprint 1 issues to this milestone.
4. **Task Issues:** Create sub-issues or use GitHub's task list (checklist) inside each user story issue for the tasks (T-001 to T-024).
5. **Commit Traceability:** Reference issue numbers in commit messages. Example: `feat: implement POST /auth/register endpoint (closes #1)`

---

*Document prepared by: [Your Full Name] | [Your Student Number] | CPUT | March 2026*