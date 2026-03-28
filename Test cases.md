# TEST_CASES.md – Test Case Development

## ClinicEase Online Doctor Appointment Booking System

---

## Functional Test Cases

| Test Case ID | Requirement ID | Description | Steps | Expected Result | Actual Result | Status |
|---|---|---|---|---|---|---|
| TC-001 | FR-01 | Patient registers with valid details | 1. Navigate to /register. 2. Enter valid name, email, password, tick consent. 3. Click Register. | Account is created, welcome email sent, user redirected to login page. | — | — |
| TC-002 | FR-01 | Login fails with incorrect password | 1. Navigate to /login. 2. Enter registered email and wrong password. 3. Click Login. | System displays "Incorrect email or password." No dashboard access granted. | — | — |
| TC-003 | FR-01 | Account locks after 5 failed login attempts | 1. Attempt login with wrong password 5 times in a row. | After the 5th attempt, account is locked for 15 minutes. User receives a lock notification email. | — | — |
| TC-004 | FR-02 | Patient searches for a doctor by specialisation | 1. Log in as patient. 2. Navigate to Find a Doctor. 3. Enter "General Practitioner" in search field. 4. Click Search. | List of matching doctors displayed within 2 seconds, each showing name, specialisation, and next available slot. | — | — |
| TC-005 | FR-03 | Patient successfully books an appointment | 1. Log in as patient. 2. Search for a doctor. 3. Select an available time slot. 4. Click Book Appointment. | Appointment created with status "Confirmed." Slot marked as booked. Confirmation email sent within 60 seconds. | — | — |
| TC-006 | FR-03 | System prevents double-booking of same slot | 1. Two users attempt to book the same doctor slot simultaneously. | First booking succeeds. Second user receives: "Sorry, this slot was just booked. Please select a different time." | — | — |
| TC-007 | FR-04 | Patient cancels a confirmed appointment | 1. Log in as patient. 2. Navigate to My Appointments. 3. Select a confirmed appointment. 4. Click Cancel. | Appointment status updated to "Cancelled." Slot released. Cancellation email sent to patient. | — | — |
| TC-008 | FR-04 | Receptionist reschedules appointment to new slot | 1. Log in as receptionist. 2. Search for patient by name. 3. Select appointment. 4. Click Reschedule. 5. Select new slot. 6. Confirm. | Appointment updated with new time. Old slot released. New slot marked booked. Patient receives rescheduling email. | — | — |
| TC-009 | FR-05 | System sends appointment reminder 24 hours before | 1. Create a confirmed appointment for tomorrow. 2. Wait for cron job to run (or trigger manually in test). | Reminder email delivered to patient exactly 24 hours before appointment. Notification logged in database. | — | — |
| TC-010 | FR-06 | Doctor adds medication schedule for patient | 1. Log in as doctor. 2. Open patient profile. 3. Navigate to Medication. 4. Add medication name, dosage, and reminder time. 5. Click Save. | Medication record saved. Daily reminder scheduled at specified time. Confirmation message displayed. | — | — |
| TC-011 | FR-07 | Doctor schedules a blood test for patient | 1. Log in as doctor. 2. Open patient profile. 3. Navigate to Procedures. 4. Add blood test with date and preparation notes. 5. Save. | Procedure saved. Patient receives a reminder 48 hours before the test including preparation instructions. | — | — |
| TC-012 | FR-10 | Doctor views patient medical history | 1. Log in as doctor. 2. Open today's appointment. 3. Click on patient name to view records. | Full medical history displayed including past consultations, prescriptions, and test results in chronological order. | — | — |
| TC-013 | FR-10 | Unauthorised user cannot view another patient's records | 1. Log in as patient A. 2. Attempt to access the records URL of patient B directly via the browser address bar. | System returns 403 Forbidden. Access denied message displayed. Attempt logged. | — | — |
| TC-014 | FR-11 | Admin generates monthly appointments report | 1. Log in as administrator. 2. Navigate to Reports. 3. Select "Monthly Appointments." 4. Choose current month. 5. Click Generate. | Report displays total appointments, no-shows, and appointments per doctor. Available to download as CSV or PDF. | — | — |
| TC-015 | FR-12 | Patient cannot access the admin panel | 1. Log in as patient. 2. Manually navigate to /admin in the browser. | System returns 403 Forbidden. Patient is not granted admin access. | — | — |

---

## Non-Functional Test Cases

### NFR Test 1 — Performance: Booking Response Time Under Load

| Field | Details |
|---|---|
| **Test Case ID** | TC-NFR-001 |
| **Requirement ID** | NFR-P2 |
| **Category** | Performance |
| **Description** | Verify that appointment booking and cancellation operations complete within 2 seconds under normal and peak load conditions. |
| **Test Tool** | Apache JMeter / k6 |
| **Steps** | 1. Configure a load test with 500 virtual users. 2. Each user sends a POST /appointments request simultaneously. 3. Record the API response times. 4. Repeat with DELETE /appointments for cancellation. |
| **Expected Result** | 95% of POST /appointments and DELETE /appointments requests return a response within 2 seconds. No 500 server errors occur. |
| **Actual Result** | — |
| **Status** | — |

---

### NFR Test 2 — Security: Password Storage and HTTPS Enforcement

| Field | Details |
|---|---|
| **Test Case ID** | TC-NFR-002 |
| **Requirement ID** | NFR-SEC1, NFR-SEC2 |
| **Category** | Security |
| **Description** | Verify that all passwords are stored as bcrypt hashes (never plaintext) and that all HTTP connections are automatically redirected to HTTPS. |
| **Test Tool** | Manual database inspection + Browser / curl |
| **Steps** | 1. Register a new user account with password "TestPass123!". 2. Inspect the users table in PostgreSQL directly. 3. Confirm the password field contains a bcrypt hash (starts with $2b$). 4. Open a browser and navigate to http://clinicease.example.com. 5. Confirm the browser is automatically redirected to https://clinicease.example.com. 6. Run `curl -I http://clinicease.example.com` and check the response header. |
| **Expected Result** | The password column contains a bcrypt hash beginning with `$2b$12$`. No plaintext password appears anywhere. The HTTP request returns a 301 redirect to HTTPS. |
| **Actual Result** | — |
| **Status** | — |

---

### NFR Test 3 — Scalability: Concurrent User Load Test

| Field | Details |
|---|---|
| **Test Case ID** | TC-NFR-003 |
| **Requirement ID** | NFR-S1 |
| **Category** | Scalability |
| **Description** | Verify the system supports 500 concurrent users without performance degradation or server errors. |
| **Test Tool** | k6 / Apache JMeter |
| **Steps** | 1. Configure k6 with 500 virtual users ramping up over 60 seconds. 2. Each virtual user performs: login → search doctor → view slots. 3. Run the test for 5 minutes. 4. Record average response time, error rate, and throughput. |
| **Expected Result** | Average API response time remains under 2 seconds. Error rate is below 1%. No database connection errors or server crashes occur. |
| **Actual Result** | — |
| **Status** | — |

---

## Test Summary Table

| Test Case ID | Type | Requirement | Priority | Status |
|---|---|---|---|---|
| TC-001 | Functional | FR-01 | High | — |
| TC-002 | Functional | FR-01 | High | — |
| TC-003 | Functional | FR-01 | High | — |
| TC-004 | Functional | FR-02 | High | — |
| TC-005 | Functional | FR-03 | High | — |
| TC-006 | Functional | FR-03 | High | — |
| TC-007 | Functional | FR-04 | High | — |
| TC-008 | Functional | FR-04 | High | — |
| TC-009 | Functional | FR-05 | High | — |
| TC-010 | Functional | FR-06 | High | — |
| TC-011 | Functional | FR-07 | High | — |
| TC-012 | Functional | FR-10 | High | — |
| TC-013 | Functional | FR-10 | High | — |
| TC-014 | Functional | FR-11 | Medium | — |
| TC-015 | Functional | FR-12 | High | — |
| TC-NFR-001 | Performance | NFR-P2 | High | — |
| TC-NFR-002 | Security | NFR-SEC1, NFR-SEC2 | High | — |
| TC-NFR-003 | Scalability | NFR-S1 | High | — |

> **Note:** "Actual Result" and "Status" columns are left blank to be completed during implementation and testing phases of development.

---

*Document prepared by: [sithembiso ] | [222618698 ] | CPUT | March 2026*