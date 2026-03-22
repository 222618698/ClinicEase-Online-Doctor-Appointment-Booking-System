# SRD.md – System Requirements Document (SRD)
## ClinicEase Online Doctor Appointment Booking System

---

## 1. Introduction

### 1.1 Purpose
This System Requirements Document (SRD) defines the functional and non-functional requirements for **ClinicEase** — a web-based clinic appointment booking system. It is intended to guide development and ensure the system meets the needs of all identified stakeholders.

### 1.2 Scope
ClinicEase enables patients to book doctor appointments online, receive medication and procedure reminders, and access paperless medical records. Doctors, receptionists, and administrators manage appointments and clinic operations through dedicated dashboards.

### 1.3 Stakeholders Referenced
Patient · Doctor · Receptionist · Clinic Administrator · IT Support Staff · Family Member/Caregiver · Medical Aid Provider (future)

---

## 2. Functional Requirements

Functional requirements describe what the system **must do**. Each requirement is traceable to one or more stakeholders.

---

### FR-01: User Registration and Login
**Statement:** The system shall allow patients, doctors, receptionists, and administrators to register and log in using a unique email address and password.

**Stakeholder(s):** Patient, Doctor, Receptionist, Clinic Administrator

**Acceptance Criteria:**
- Registration form validates email format and enforces a minimum password length of 8 characters
- Login fails with a clear error message if credentials are incorrect
- Successful login redirects the user to their role-specific dashboard within 2 seconds

---

### FR-02: Doctor Search and Availability Browsing
**Statement:** The system shall allow patients to search for doctors by name, specialisation, or available date, and view open time slots.

**Stakeholder(s):** Patient, Family Member/Caregiver

**Acceptance Criteria:**
- Search results display within 2 seconds of query submission
- Each doctor profile shows name, specialisation, qualifications, and next available slot
- Fully booked doctors are clearly marked as unavailable

---

### FR-03: Online Appointment Booking
**Statement:** The system shall allow patients or caregivers to book an appointment by selecting a doctor, date, and available time slot.

**Stakeholder(s):** Patient, Family Member/Caregiver, Receptionist

**Acceptance Criteria:**
- Booking is confirmed only if the selected time slot is still available at the moment of submission
- The system prevents double-booking of the same time slot using a database uniqueness constraint
- A booking confirmation message is displayed immediately and an email is sent within 60 seconds

---

### FR-04: Appointment Cancellation and Rescheduling
**Statement:** The system shall allow patients, caregivers, and receptionists to cancel or reschedule an existing appointment.

**Stakeholder(s):** Patient, Receptionist, Family Member/Caregiver

**Acceptance Criteria:**
- Cancellations and reschedules are processed within 2 seconds
- The cancelled time slot is immediately released and made available to other patients
- The patient receives an email notification confirming the cancellation or new appointment time

---

### FR-05: Automated Appointment Reminder Notifications
**Statement:** The system shall automatically send a reminder notification to the patient 24 hours and 1 hour before their scheduled appointment.

**Stakeholder(s):** Patient, Family Member/Caregiver

**Acceptance Criteria:**
- Reminders are delivered via email and in-app notification at exactly 24 hours and 1 hour before the appointment
- If the patient has a registered caregiver, the reminder is sent to both contacts
- Reminders are not sent for cancelled appointments

---

### FR-06: Medication Reminder System
**Statement:** The system shall allow doctors or patients to set up a medication schedule, and the system shall send dose reminders at the configured times each day.

**Stakeholder(s):** Patient, Doctor, Family Member/Caregiver

**Acceptance Criteria:**
- Patients or doctors can add a medication name, dosage, and daily reminder time
- Reminders are delivered via in-app notification and email at the scheduled time
- When a chronic medication is within 7 days of running out, the system sends a refill alert

---

### FR-07: Blood Test and Procedure Reminders
**Statement:** The system shall allow doctors to schedule follow-up procedures (e.g., blood tests, injections) for a patient, and automatically notify the patient when the procedure date is approaching.

**Stakeholder(s):** Patient, Doctor

**Acceptance Criteria:**
- Doctors can schedule a procedure with a date, time, and preparation instructions (e.g., "fast from midnight")
- The patient receives a notification 48 hours before the procedure
- The notification includes the procedure name, date, time, and any preparation notes

---

### FR-08: Doctor Dashboard — Daily Schedule View
**Statement:** The system shall provide doctors with a dashboard displaying their full appointment schedule for the current day and upcoming week.

**Stakeholder(s):** Doctor

**Acceptance Criteria:**
- Dashboard loads within 2 seconds of login
- Appointments are listed in chronological order with patient name, time, and appointment status
- Doctors can click an appointment to view the patient's medical history and previous visit notes

---

### FR-09: Receptionist Appointment Management
**Statement:** The system shall provide receptionists with an interface to create, reschedule, and cancel appointments on behalf of patients, and to add walk-in patients to the queue.

**Stakeholder(s):** Receptionist

**Acceptance Criteria:**
- Receptionists can search for a patient by name or ID number
- Booking, rescheduling, and cancellation actions complete within 2 seconds
- Walk-in patients can be added to the current day's queue within 1 minute

---

### FR-10: Paperless Patient Records
**Statement:** The system shall store each patient's medical history, consultation notes, prescriptions, and test results digitally, accessible to the treating doctor during a consultation.

**Stakeholder(s):** Doctor, Patient, Clinic Administrator

**Acceptance Criteria:**
- All consultation notes saved by the doctor are stored and retrievable within 1 second
- Patients can view their own records from the patient portal
- Records are never deleted — only archived — to maintain a complete history

---

### FR-11: Admin Panel — User and Clinic Management
**Statement:** The system shall provide administrators with a panel to add, edit, and deactivate doctor and staff accounts, manage clinic settings, and generate operational reports.

**Stakeholder(s):** Clinic Administrator

**Acceptance Criteria:**
- Administrators can activate or deactivate any user account within 2 clicks
- Reports for appointment volumes, no-show rates, and peak booking times are generated on demand
- All admin actions are logged with a timestamp and the admin's user ID for audit purposes

---

### FR-12: Role-Based Access Control
**Statement:** The system shall enforce role-based access so that patients, doctors, receptionists, and administrators can only access features relevant to their role.

**Stakeholder(s):** IT Support Staff, Clinic Administrator

**Acceptance Criteria:**
- A patient cannot access the doctor dashboard or admin panel
- Attempting to access an unauthorised route returns a 403 Forbidden response
- Role assignments can only be changed by an administrator

---

## 3. Non-Functional Requirements

Non-functional requirements define **how well** the system must perform. They are categorised by quality attribute.

---

### 3.1 Usability

**NFR-U1:** The system interface shall be responsive and fully functional on desktop browsers (Chrome, Firefox, Edge) and mobile browsers (Safari, Chrome for Android) without requiring a native app installation.

*Acceptance Criteria: All pages render correctly at screen widths from 360px (mobile) to 1920px (desktop) with no overlapping or clipped content.*

**NFR-U2:** All forms shall display inline validation messages in plain language when a user submits invalid input, without requiring a page reload.

*Acceptance Criteria: Validation messages appear within 300ms of a form submission attempt. Messages use clear language (e.g., "Please enter a valid email address") not error codes.*

---

### 3.2 Deployability

**NFR-D1:** The system shall be deployable on both Linux (Ubuntu 22.04+) and Windows Server 2019+ environments using standard Node.js and PostgreSQL installations.

*Acceptance Criteria: A new instance of the system can be fully deployed from scratch using the provided setup guide in under 30 minutes.*

**NFR-D2:** The system shall support containerised deployment using Docker, with a `docker-compose.yml` file provided for local and cloud environments.

*Acceptance Criteria: Running `docker-compose up` starts all services (frontend, API, database) with no manual configuration required.*

---

### 3.3 Maintainability

**NFR-M1:** All REST API endpoints shall be documented in a developer API guide (API.md) including endpoint paths, HTTP methods, request parameters, and example responses.

*Acceptance Criteria: A developer unfamiliar with the codebase can integrate with any API endpoint using only the API.md documentation, without reading source code.*

**NFR-M2:** The codebase shall follow a modular folder structure separating routes, controllers, services, and models so that individual modules can be updated without affecting unrelated components.

*Acceptance Criteria: Updating the Appointment module requires changes only within the `/appointment` module folder — no changes to Auth, Medication, or Records modules.*

---

### 3.4 Scalability

**NFR-S1:** The system shall support a minimum of 500 concurrent users without degradation in response time, and shall be architected to scale horizontally to support up to 2,000 concurrent users by adding additional server instances.

*Acceptance Criteria: Load testing with 500 simultaneous users produces an average API response time of under 2 seconds with no server errors.*

**NFR-S2:** The PostgreSQL database shall use indexed queries on all frequently searched fields (patient ID, doctor ID, appointment date) to maintain fast query performance as data volume grows.

*Acceptance Criteria: Database queries on indexed fields return results in under 100ms for a dataset of 100,000 appointment records.*

---

### 3.5 Security

**NFR-SEC1:** All user passwords shall be hashed using bcrypt with a minimum cost factor of 12 before being stored in the database. Plaintext passwords shall never be stored or logged.

*Acceptance Criteria: A database inspection of the users table reveals only bcrypt hashes in the password field. No password appears in any application log.*

**NFR-SEC2:** All data transmitted between the client and the server shall be encrypted using TLS 1.2 or higher (HTTPS). Plain HTTP connections shall be automatically redirected to HTTPS.

*Acceptance Criteria: All HTTP requests to the system return a 301 redirect to the HTTPS equivalent. TLS version confirmed as 1.2 or 1.3 via SSL audit tool.*

**NFR-SEC3:** The system shall comply with the Protection of Personal Information Act (POPIA, South Africa) by obtaining explicit patient consent before storing personal data, and providing patients with the ability to request deletion of their data.

*Acceptance Criteria: A consent checkbox is present and required on the patient registration form. Patients can submit a data deletion request from their profile settings.*

---

### 3.6 Performance

**NFR-P1:** All page loads and dashboard views shall complete within 3 seconds on a standard broadband connection (10 Mbps or faster).

*Acceptance Criteria: Lighthouse performance audit scores 80 or above for all key pages. No page load exceeds 3 seconds in testing.*

**NFR-P2:** Appointment booking and cancellation operations shall be processed and confirmed within 2 seconds from the moment the patient submits the request.

*Acceptance Criteria: API response time for POST /appointments and DELETE /appointments endpoints is under 2 seconds in 95% of test cases under normal load.*

**NFR-P3:** The automated reminder cron job (daily 8AM run) shall complete processing and dispatch all due reminders within 5 minutes, regardless of the number of appointments scheduled for that day.

*Acceptance Criteria: In a test environment with 1,000 appointments scheduled for the following day, all reminder emails are dispatched within 5 minutes of the cron job starting.*

---

## 4. Requirements Traceability Matrix

| Requirement ID | Description | Stakeholder(s) | Priority |
|---|---|---|---|
| FR-01 | User registration and login | All | High |
| FR-02 | Doctor search and availability | Patient, Caregiver | High |
| FR-03 | Online appointment booking | Patient, Caregiver, Receptionist | High |
| FR-04 | Cancellation and rescheduling | Patient, Receptionist | High |
| FR-05 | Appointment reminder notifications | Patient, Caregiver | High |
| FR-06 | Medication reminder system | Patient, Doctor, Caregiver | High |
| FR-07 | Blood test / procedure reminders | Patient, Doctor | High |
| FR-08 | Doctor dashboard | Doctor | High |
| FR-09 | Receptionist management interface | Receptionist | High |
| FR-10 | Paperless patient records | Doctor, Patient, Admin | High |
| FR-11 | Admin panel | Clinic Administrator | Medium |
| FR-12 | Role-based access control | IT Staff, Admin | High |
| NFR-U1 | Responsive UI | Patient, Caregiver | High |
| NFR-U2 | Inline form validation | Patient, Receptionist | Medium |
| NFR-D1 | Linux/Windows deployability | IT Staff | Medium |
| NFR-D2 | Docker support | IT Staff | Medium |
| NFR-M1 | API documentation | IT Staff | Medium |
| NFR-M2 | Modular codebase | IT Staff | Medium |
| NFR-S1 | 500 concurrent users | IT Staff, Admin | High |
| NFR-S2 | Indexed database queries | IT Staff | Medium |
| NFR-SEC1 | bcrypt password hashing | IT Staff, Admin | High |
| NFR-SEC2 | HTTPS / TLS encryption | IT Staff | High |
| NFR-SEC3 | POPIA compliance | Admin, Patient | High |
| NFR-P1 | Page load under 3 seconds | Patient, Doctor | High |
| NFR-P2 | Booking response under 2 seconds | Patient, Receptionist | High |
| NFR-P3 | Cron job completes in 5 minutes | IT Staff | Medium |

---

*Document prepared by: [Sithembiso] | [222618698] | CPUT | March 2026*