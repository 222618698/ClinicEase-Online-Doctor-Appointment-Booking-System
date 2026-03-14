# SPECIFICATION.md – ClinicEase Online Doctor Appointment Booking System

---

## 1. Project Title

**ClinicEase – Online Doctor Appointment Booking System**

---

## 2. Domain

**Domain:** Healthcare / Medical Services

### Domain Description

Healthcare is one of the most critical service domains in any country. In South Africa, both public and private clinics serve millions of patients daily. The process of booking a medical appointment remains largely manual — patients call the clinic, wait on hold, or physically visit just to secure a time slot. This leads to overcrowded waiting rooms, missed appointments, and poor patient experience.

The healthcare domain involves patients, medical practitioners (doctors, nurses, specialists), administrative staff (receptionists), and clinic management. Digital transformation in this domain improves efficiency, reduces waiting times, and enhances the overall quality of care. ClinicEase targets small-to-medium private clinics and community health centres that do not yet have an online booking system.

---

## 3. Problem Statement

Patients at local clinics in South Africa face the following challenges:

- No way to book appointments online — all bookings are done by phone or walk-in
- Long waiting times at clinics due to poor scheduling management
- Doctors have no digital overview of their daily appointments
- Patients forget appointments because there are no automated reminders
- Receptionists manually manage paper-based or spreadsheet appointment books
- Overbooking and double-booking of time slots is a frequent problem

**ClinicEase** solves these problems by providing a digital appointment booking platform where patients can search for available doctors, select time slots, and receive automatic reminders — while doctors and receptionists manage their schedules through a real-time dashboard.

---

## 4. Individual Scope & Feasibility Justification

This project is scoped for individual development over one semester and is feasible because:

- It uses well-known intermediate technologies (React, Node.js, PostgreSQL)
- The booking/scheduling logic is well-documented and implementable within the timeframe
- No physical hardware or medical device integration is required
- Free-tier cloud hosting (Render, Railway, Supabase) is available for deployment
- The developer has JavaScript and web development experience at intermediate level

**In Scope:**
- Patient registration, login, and profile management
- Doctor profile listing with specialisation and availability
- Appointment booking, rescheduling, and cancellation
- Doctor dashboard showing daily appointment schedule
- Receptionist interface for manual appointment management
- Email notifications for booking confirmation and reminders
- Admin panel for managing doctors and users

**Out of Scope:**
- Online payment / medical aid billing
- Video/telemedicine consultations
- Integration with hospital ERP systems (e.g., MEDITECH)
- Mobile app (iOS/Android)
- Medical records or prescription management

---

## 5. Functional Requirements

| ID | Requirement |
|---|---|
| FR-01 | Patients shall be able to register and log in using email and password |
| FR-02 | Patients shall be able to search for doctors by name, specialisation, or availability |
| FR-03 | Patients shall be able to view a doctor's available time slots and book an appointment |
| FR-04 | Patients shall be able to reschedule or cancel an existing appointment |
| FR-05 | The system shall send an email confirmation when an appointment is booked |
| FR-06 | The system shall send a reminder email 24 hours before a scheduled appointment |
| FR-07 | Doctors shall be able to log in and view their daily/weekly appointment schedule |
| FR-08 | Doctors shall be able to mark appointments as completed, missed, or cancelled |
| FR-09 | Receptionists shall be able to create, reschedule, or cancel appointments on behalf of patients |
| FR-10 | Administrators shall be able to add, edit, or deactivate doctor accounts and manage clinic settings |

---

## 6. Non-Functional Requirements

| ID | Requirement |
|---|---|
| NFR-01 | The system shall load any page within 3 seconds on a standard broadband connection |
| NFR-02 | The system shall be available 99% of the time excluding planned maintenance |
| NFR-03 | All user passwords shall be hashed using bcrypt before being stored in the database |
| NFR-04 | The system shall prevent double-booking of the same doctor time slot using database constraints |
| NFR-05 | The system shall be responsive and usable on both desktop and mobile web browsers |
| NFR-06 | All patient data shall be handled in compliance with POPIA (Protection of Personal Information Act, South Africa) |
| NFR-07 | The system shall support at least 200 concurrent users without performance degradation |

---

## 7. Use Cases

### UC-01: Patient Books an Appointment
- **Actor:** Patient
- **Precondition:** Patient is registered and logged in
- **Flow:** Patient searches for a doctor by specialisation → views available slots → selects date and time → confirms booking → system saves appointment and sends confirmation email
- **Postcondition:** Appointment is created with status "Confirmed"

### UC-02: Doctor Views Daily Schedule
- **Actor:** Doctor
- **Precondition:** Doctor is logged in
- **Flow:** Doctor navigates to dashboard → system retrieves all appointments for today → displays list with patient names, times, and status
- **Postcondition:** Doctor has a clear view of their daily workload

### UC-03: Receptionist Reschedules an Appointment
- **Actor:** Receptionist
- **Precondition:** Receptionist is logged in; appointment exists
- **Flow:** Receptionist searches for patient by name → views their appointments → selects appointment → chooses new time slot → confirms change → system updates record and notifies patient by email
- **Postcondition:** Appointment is updated with new time; patient receives email notification

### UC-04: System Sends Reminder Notification
- **Actor:** System (automated)
- **Precondition:** An appointment is scheduled for the next day
- **Flow:** Scheduled cron job runs at 8:00 AM daily → queries all appointments scheduled for tomorrow → sends reminder email to each patient
- **Postcondition:** Patients are reminded of upcoming appointments

---

## 8. System Constraints

- The system is web-based only; no native mobile app will be developed
- Development tools must be free and open-source
- The PostgreSQL database will be hosted on a free-tier cloud provider (e.g., Supabase)
- The project must be fully completed within one academic semester
- Email notifications will use a free SMTP service (e.g., Gmail SMTP or SendGrid free tier)

---

*Document prepared by: [Sithembiso] | [Mthembu] | CPUT | March 2026*