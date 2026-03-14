# ARCHITECTURE.md – ClinicEase Online Doctor Appointment Booking System

---

## Project Title
**ClinicEase – Online Doctor Appointment Booking System**

## Domain
**Healthcare / Medical Services**

## Problem Statement
Patients cannot book doctor appointments online, leading to long queues, overbooking, and missed appointments. ClinicEase provides a digital booking platform for patients, doctors, receptionists, and admins.

## Individual Scope
A web-based booking system built with React, Node.js, and PostgreSQL — fully feasible for individual development within one semester.

---

## C4 Architectural Diagrams

> All diagrams are written using [Mermaid](https://mermaid.js.org/) and render natively on GitHub.

---

## Level 1 – System Context Diagram

> Shows the key users and external systems that interact with ClinicEase.

```mermaid
C4Context
    title System Context Diagram – ClinicEase

    Person(patient, "Patient", "A registered patient who searches for doctors, books appointments, and receives reminders.")
    Person(doctor, "Doctor", "A medical practitioner who views their schedule and updates appointment statuses.")
    Person(receptionist, "Receptionist", "Clinic staff who manage appointments on behalf of patients.")
    Person(admin, "Administrator", "Manages doctors, users, and clinic system settings.")

    System(clinicease, "ClinicEase Portal", "A web-based appointment booking system connecting patients, doctors, and clinic staff.")

    System_Ext(emailService, "Email Service (SMTP)", "Sends booking confirmations and 24-hour reminder emails to patients.")
    System_Ext(calendarService, "Calendar Integration (Optional)", "Allows patients to add appointments to Google Calendar or Outlook.")

    Rel(patient, clinicease, "Searches doctors, books/cancels appointments, views history")
    Rel(doctor, clinicease, "Views daily schedule, updates appointment status")
    Rel(receptionist, clinicease, "Creates, reschedules, and cancels appointments")
    Rel(admin, clinicease, "Manages doctors, users, and clinic settings")
    Rel(clinicease, emailService, "Sends confirmation and reminder emails", "SMTP")
    Rel(clinicease, calendarService, "Exports appointment events", "API")
```

---

## Level 2 – Container Diagram

> Shows the major containers (applications and data stores) that make up ClinicEase.

```mermaid
C4Container
    title Container Diagram – ClinicEase

    Person(patient, "Patient", "Uses a web browser to access ClinicEase")
    Person(doctor, "Doctor", "Uses a web browser to manage their schedule")
    Person(receptionist, "Receptionist", "Uses a web browser to manage appointments")

    System_Boundary(clinicease, "ClinicEase System") {
        Container(webApp, "React Web App", "React.js", "Provides all user interfaces: patient booking portal, doctor dashboard, receptionist panel, and admin console.")
        Container(apiServer, "REST API Server", "Node.js + Express", "Processes all business logic: authentication, appointment scheduling, availability checks, and status updates.")
        Container(database, "PostgreSQL Database", "PostgreSQL", "Stores all data: users, doctors, appointments, time slots, clinics, and notification logs.")
        Container(schedulerService, "Scheduler Service", "Node-cron", "Runs daily at 8AM to find appointments scheduled for tomorrow and triggers reminder emails.")
        Container(notificationService, "Notification Service", "Nodemailer", "Composes and dispatches confirmation and reminder emails to patients.")
    }

    System_Ext(emailService, "Email Service (SMTP)", "External email delivery service (e.g. SendGrid, Gmail SMTP)")

    Rel(patient, webApp, "Books and manages appointments", "HTTPS")
    Rel(doctor, webApp, "Views and manages schedule", "HTTPS")
    Rel(receptionist, webApp, "Manages appointments for patients", "HTTPS")
    Rel(webApp, apiServer, "Makes REST API calls", "HTTPS / JSON")
    Rel(apiServer, database, "Reads and writes data", "SQL / TCP")
    Rel(schedulerService, database, "Queries upcoming appointments", "SQL")
    Rel(schedulerService, notificationService, "Triggers reminder emails")
    Rel(apiServer, notificationService, "Triggers confirmation emails")
    Rel(notificationService, emailService, "Sends emails", "SMTP / TLS")
```

---

## Level 3 – Component Diagram (API Server)

> Shows the internal components of the Node.js REST API Server.

```mermaid
C4Component
    title Component Diagram – REST API Server (Node.js + Express)

    Container_Boundary(apiServer, "REST API Server") {
        Component(authComponent, "Auth Component", "Express Router + JWT", "Handles patient, doctor, receptionist, and admin login. Issues and validates JWT tokens.")
        Component(doctorComponent, "Doctor Component", "Express Router", "Manages doctor profiles, specialisations, and availability slot configuration.")
        Component(appointmentComponent, "Appointment Component", "Express Router", "Core booking logic: creates, updates, cancels appointments and checks slot availability.")
        Component(scheduleComponent, "Schedule Component", "Express Router", "Returns daily/weekly appointment views for doctors and receptionists.")
        Component(notificationComponent, "Notification Component", "Express Router + Nodemailer", "Sends booking confirmations and reminder emails.")
        Component(adminComponent, "Admin Component", "Express Router", "CRUD operations for managing doctors, users, and clinic configuration.")
        Component(dbLayer, "Database Access Layer", "Sequelize ORM", "Abstracts all database queries. Enforces unique slot constraints to prevent double-booking.")
    }

    ContainerDb(database, "PostgreSQL Database", "PostgreSQL", "Persistent data store")
    Container(webApp, "React Web App", "React.js", "Frontend client")

    Rel(webApp, authComponent, "POST /auth/login, /auth/register", "HTTPS/JSON")
    Rel(webApp, doctorComponent, "GET /doctors, GET /doctors/:id/slots", "HTTPS/JSON")
    Rel(webApp, appointmentComponent, "POST/GET/PUT/DELETE /appointments", "HTTPS/JSON")
    Rel(webApp, scheduleComponent, "GET /schedule/today, /schedule/week", "HTTPS/JSON")
    Rel(webApp, adminComponent, "GET/POST/PUT /admin/doctors", "HTTPS/JSON")
    Rel(appointmentComponent, notificationComponent, "Triggers confirmation on booking")
    Rel(appointmentComponent, dbLayer, "Reads/writes appointment records")
    Rel(doctorComponent, dbLayer, "Reads/writes doctor and slot records")
    Rel(scheduleComponent, dbLayer, "Reads appointment records by date")
    Rel(authComponent, dbLayer, "Reads user credentials")
    Rel(adminComponent, dbLayer, "CRUD on doctors and users")
    Rel(dbLayer, database, "SQL queries", "TCP")
```

---

## Level 4 – Code Diagram (Appointment Module – Class Level)

> Shows the key classes and their relationships within the core Appointment booking module.

```mermaid
classDiagram
    class Patient {
        +int patientId
        +String name
        +String email
        +String phone
        +searchDoctors(specialisation: String)
        +bookAppointment(slotId: int)
        +cancelAppointment(appointmentId: int)
        +viewAppointmentHistory()
    }

    class Doctor {
        +int doctorId
        +String name
        +String specialisation
        +String qualifications
        +List~TimeSlot~ availableSlots
        +viewDailySchedule(date: Date)
        +markAppointmentComplete(appointmentId: int)
        +markAppointmentMissed(appointmentId: int)
    }

    class Appointment {
        +int appointmentId
        +int patientId
        +int doctorId
        +int slotId
        +Date appointmentDate
        +String status
        +String notes
        +create()
        +cancel()
        +reschedule(newSlotId: int)
        +updateStatus(status: String)
    }

    class TimeSlot {
        +int slotId
        +int doctorId
        +DateTime startTime
        +DateTime endTime
        +boolean isBooked
        +markAsBooked()
        +markAsAvailable()
    }

    class Receptionist {
        +int receptionistId
        +String name
        +String email
        +createAppointmentForPatient(patientId: int, slotId: int)
        +rescheduleAppointment(appointmentId: int, newSlotId: int)
        +cancelAppointment(appointmentId: int)
    }

    class NotificationService {
        +sendConfirmationEmail(appointment: Appointment)
        +sendReminderEmail(appointment: Appointment)
        +sendCancellationEmail(appointment: Appointment)
        +sendRescheduleEmail(appointment: Appointment)
    }

    Patient "1" --> "0..*" Appointment : books
    Doctor "1" --> "0..*" Appointment : receives
    Doctor "1" --> "1..*" TimeSlot : owns
    Appointment "1" --> "1" TimeSlot : occupies
    Receptionist --> Appointment : manages
    Appointment --> NotificationService : triggers
```

---

## End-to-End Component Summary

The table below maps every component from the user's browser all the way to the database and external services:

| Layer | Technology | Role |
|---|---|---|
| User (Browser) | Chrome / Firefox / Safari | Entry point for patients, doctors, receptionists, admins |
| Frontend | React.js | UI — booking portal, doctor dashboard, admin console |
| API Server | Node.js + Express | All business logic and REST API routing |
| Auth Module | JWT + bcrypt | Secure login and role-based access |
| Appointment Module | Express + Sequelize | Core booking, cancellation, rescheduling logic |
| Doctor Module | Express + Sequelize | Doctor profiles and availability slot management |
| Schedule Module | Express + Sequelize | Daily/weekly schedule views |
| Notification Module | Nodemailer | Email confirmations and reminders |
| Scheduler | Node-cron | Automated daily reminder job (runs at 8AM) |
| Database | PostgreSQL | All persistent data storage with slot uniqueness constraints |
| Email Service | SMTP (SendGrid / Gmail) | External email delivery |
| Calendar (Optional) | Google Calendar API | Patient calendar integration |

---

*Document prepared by: [Your Full Name] | [Your Student Number] | CPUT | March 2026*