# USE_CASE_DIAGRAM.md – ClinicEase Use Case Diagram

---

## Use Case Diagram (Mermaid)

```mermaid
flowchart LR
    %% ── ACTORS ──
    P(["👤 Patient"])
    CG(["👨‍👩‍👧 Caregiver"])
    DOC(["👨‍⚕️ Doctor"])
    REC(["🖥️ Receptionist"])
    ADM(["🔑 Administrator"])
    IT(["🛠️ IT Staff"])
    SYS(["⚙️ System / Scheduler"])

    %% ── USE CASES ──
    UC1["Register & Login"]
    UC2["Search Doctor\nby Name / Specialisation"]
    UC3["Book Appointment"]
    UC4["Cancel / Reschedule\nAppointment"]
    UC5["Receive Appointment\nReminder"]
    UC6["Manage Medication\nSchedule"]
    UC7["Receive Medication\nReminder"]
    UC8["Schedule Blood Test\nor Procedure"]
    UC9["Receive Procedure\nReminder"]
    UC10["View Patient\nMedical Records"]
    UC11["View Daily\nSchedule"]
    UC12["Update Consultation\nNotes"]
    UC13["Manage Appointments\nfor Patients"]
    UC14["Add Walk-in Patient\nto Queue"]
    UC15["Manage Users\n& Clinic Settings"]
    UC16["Generate Operational\nReports"]
    UC17["Monitor System\nUptime & Logs"]
    UC18["Check Slot\nAvailability"]
    UC19["Send Email\nNotification"]

    %% ── PATIENT CONNECTIONS ──
    P --> UC1
    P --> UC2
    P --> UC3
    P --> UC4
    P --> UC5
    P --> UC6
    P --> UC7
    P --> UC10

    %% ── CAREGIVER CONNECTIONS ──
    CG --> UC1
    CG --> UC2
    CG --> UC3
    CG --> UC4
    CG --> UC6
    CG --> UC5

    %% ── DOCTOR CONNECTIONS ──
    DOC --> UC1
    DOC --> UC11
    DOC --> UC10
    DOC --> UC12
    DOC --> UC8

    %% ── RECEPTIONIST CONNECTIONS ──
    REC --> UC1
    REC --> UC13
    REC --> UC14

    %% ── ADMIN CONNECTIONS ──
    ADM --> UC1
    ADM --> UC15
    ADM --> UC16

    %% ── IT STAFF CONNECTIONS ──
    IT --> UC17

    %% ── SYSTEM / SCHEDULER ──
    SYS --> UC5
    SYS --> UC7
    SYS --> UC9
    SYS --> UC19

    %% ── INCLUDE RELATIONSHIPS ──
    UC3 -.->|includes| UC18
    UC3 -.->|includes| UC19
    UC4 -.->|includes| UC19
    UC5 -.->|includes| UC19
    UC7 -.->|includes| UC19
    UC9 -.->|includes| UC19
    UC8 -.->|includes| UC9

    %% ── STYLES ──
    classDef actor    fill:#E1F5EE,stroke:#0F6E56,color:#085041
    classDef usecase  fill:#E6F1FB,stroke:#185FA5,color:#0C447C
    classDef system   fill:#EEEDFE,stroke:#534AB7,color:#3C3489

    class P,CG,DOC,REC,ADM,IT actor
    class SYS system
    class UC1,UC2,UC3,UC4,UC5,UC6,UC7,UC8,UC9,UC10,UC11,UC12,UC13,UC14,UC15,UC16,UC17,UC18,UC19 usecase
```

---

## Written Explanation

### Key Actors and Their Roles

| Actor | Role in the System |
|---|---|
| **Patient** | The primary user. Registers, searches for doctors, books and cancels appointments, manages medication schedules, and views medical records. |
| **Caregiver** | Books and manages appointments on behalf of a dependent patient. Can manage medication reminders and receive notifications. Shares most use cases with the Patient. |
| **Doctor** | Views their daily schedule, accesses patient medical history, updates consultation notes, and schedules follow-up procedures like blood tests. |
| **Receptionist** | Manages appointments on behalf of patients, adds walk-in patients to the queue, and handles rescheduling at the front desk. |
| **Administrator** | Manages all user accounts, clinic settings, and generates operational reports. Has full system access. |
| **IT Staff** | Monitors system uptime, reviews error logs, and ensures the system is running correctly. Does not interact with patient-facing features. |
| **System / Scheduler** | An automated actor representing the cron job that triggers appointment reminders, medication reminders, and procedure alerts without human input. |

---

### Relationships Between Actors and Use Cases

**Inclusion relationships (`includes`):**
- **Book Appointment** includes **Check Slot Availability** — before a booking is confirmed, the system must verify the slot is still open. This prevents double-booking (FR-03).
- **Book Appointment** and **Cancel/Reschedule Appointment** both include **Send Email Notification** — every booking action triggers an automated email to the patient (FR-03, FR-04).
- **Receive Appointment Reminder**, **Receive Medication Reminder**, and **Receive Procedure Reminder** all include **Send Email Notification** — reminders are always delivered via email (FR-05, FR-06, FR-07).
- **Schedule Blood Test or Procedure** includes **Receive Procedure Reminder** — when a doctor schedules a procedure, it automatically creates a future reminder (FR-07, FR-08).

**Generalisation:**
- The **Caregiver** actor shares the registration, search, booking, and reminder use cases with the **Patient** actor, because caregivers perform these actions on behalf of patients. This reflects the stakeholder concern from Assignment 4 that caregivers need the same booking capabilities as patients.

---

### How the Diagram Addresses Stakeholder Concerns from Assignment 4

| Stakeholder | Concern from Assignment 4 | Use Case(s) Addressing It |
|---|---|---|
| Patient | Book appointments without visiting the clinic | UC2, UC3 |
| Patient | Never miss medication or procedure | UC6, UC7, UC9 |
| Patient | No more paper files | UC10 |
| Doctor | Real-time view of daily schedule | UC11 |
| Doctor | Access patient history before consultation | UC10, UC12 |
| Receptionist | Fast appointment management and walk-ins | UC13, UC14 |
| Administrator | Control user access and generate reports | UC15, UC16 |
| IT Staff | Monitor system health | UC17 |
| Caregiver | Manage a dependent's appointments remotely | UC2, UC3, UC4, UC6 |
| System/Scheduler | Automate all reminder notifications | UC5, UC7, UC9, UC19 |

---

*Document prepared by: [Your Full Name] | [Your Student Number] | CPUT | March 2026*