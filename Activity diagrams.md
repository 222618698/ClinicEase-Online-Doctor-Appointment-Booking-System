# ACTIVITY_DIAGRAMS.md – Activity Workflow Modeling

## ClinicEase Online Doctor Appointment Booking System

---

## Overview

This document models 8 critical workflows in ClinicEase using UML activity diagrams written in Mermaid. Each diagram includes start/end nodes, actions, decision points, parallel actions, and swimlanes showing which actor is responsible for each step.

---

## Workflow 1: Patient Registration

```mermaid
flowchart TD
    START([🟢 Start]) --> A

    subgraph Patient ["👤 Patient"]
        A[Open registration page]
        B[Fill in name, email, password]
        C[Tick POPIA consent checkbox]
        D[Click Register]
        M[Check inbox for verification email]
        N[Click verification link]
    end

    subgraph System ["⚙️ System"]
        E{All fields valid?}
        F[Display validation errors]
        G{Email already registered?}
        H[Show: Email already exists]
        I[Hash password with bcrypt]
        J[Save user record to database]
        K[Send welcome and verification email]
        L{Email link clicked?}
        O[Activate account]
        P[Redirect to login page]
        Q[Expire verification link after 24h]
    end

    A --> B --> C --> D --> E
    E -- No --> F --> B
    E -- Yes --> G
    G -- Yes --> H --> B
    G -- No --> I --> J --> K --> M --> N --> L
    L -- Yes --> O --> P --> END([🔴 End])
    L -- No --> Q --> END
```

### Explanation
This workflow covers US-001 (FR-01). The parallel actions of saving the user record and sending the welcome email happen in sequence but the system handles both without patient input. Key decision points validate email format and check for duplicate accounts — addressing the IT staff concern about data integrity. The POPIA consent checkbox directly satisfies NFR-SEC3.

---

## Workflow 2: Doctor Search and Appointment Booking

```mermaid
flowchart TD
    START([🟢 Start]) --> A

    subgraph Patient ["👤 Patient / Caregiver"]
        A[Navigate to Find a Doctor]
        B[Enter search term: name / specialisation / date]
        C[Click Search]
        H[Select a doctor from results]
        I[Choose available time slot]
        J[Click Book Appointment]
        M[Receive confirmation message on screen]
    end

    subgraph System ["⚙️ System"]
        D{Results found?}
        E[Display doctor list with availability]
        F[Show: No doctors found]
        G[Display doctor profile with time slots]
        K{Is slot still available?}
        L[Show: Slot just taken - choose another]
        N[Create appointment record - status: Confirmed]
        O[Mark slot as Booked]
        P[Send confirmation email]
        Q[Schedule 24h and 1h reminders]
    end

    A --> B --> C --> D
    D -- No --> F --> B
    D -- Yes --> E --> H --> G --> I --> J --> K
    K -- No --> L --> I
    K -- Yes --> N & O
    N --> M
    O --> P
    P --> Q --> END([🔴 End])
```

### Explanation
This workflow covers US-003 and US-004 (FR-02, FR-03). The parallel actions after a confirmed booking — creating the appointment record, marking the slot as booked, sending confirmation email, and scheduling reminders — all happen simultaneously to ensure the fastest possible confirmation. This directly addresses the patient stakeholder's pain point of long queues and manual booking processes.

---

## Workflow 3: Appointment Cancellation and Rescheduling

```mermaid
flowchart TD
    START([🟢 Start]) --> A

    subgraph Patient ["👤 Patient / Receptionist"]
        A[Navigate to My Appointments]
        B[Select appointment]
        C{Cancel or Reschedule?}
        D[Click Cancel]
        E[Click Reschedule]
        F[Select new time slot]
        G[Confirm cancellation]
        K[Confirm new booking]
    end

    subgraph System ["⚙️ System"]
        H[Update appointment status to Cancelled]
        I[Release original slot - status: Available]
        J[Send cancellation email to patient]
        L{Is new slot available?}
        M[Show: Slot not available]
        N[Update appointment with new slot]
        O[Release old slot - status: Available]
        P[Send rescheduling confirmation email]
    end

    A --> B --> C
    C -- Cancel --> D --> G --> H & I
    H --> J --> END([🔴 End])
    I --> END
    C -- Reschedule --> E --> F --> L
    L -- No --> M --> F
    L -- Yes --> K --> N & O
    N --> P --> END
    O --> END
```

### Explanation
This workflow covers US-005 (FR-04). The parallel actions on cancellation — updating the appointment status AND releasing the slot — must happen simultaneously to prevent any window where a slot appears booked but has no active appointment. This addresses the receptionist's concern about scheduling conflicts and overbooking.

---

## Workflow 4: Automated Appointment Reminder

```mermaid
flowchart TD
    START([🟢 Start]) --> A

    subgraph System_Scheduler ["⚙️ System Scheduler - Cron Job"]
        A[Cron job triggers every 30 minutes]
        B[Query database for appointments in next 24h or 1h]
        C{Appointments found?}
        D[Exit - no reminders needed]
        E[For each appointment: check status]
        F{Status = Confirmed?}
        G[Skip - appointment cancelled or completed]
        H[Compose reminder email with doctor name, date, time, location]
    end

    subgraph Notification_Service ["📧 Notification Service"]
        I[Send email to patient]
        J{Caregiver linked?}
        K[Send email to caregiver]
        L{Email delivered?}
        M[Log success in notifications table]
        N[Retry up to 3 times]
        O{Retry successful?}
        P[Log failure for IT review]
    end

    subgraph Patient ["👤 Patient / Caregiver"]
        Q[Receive reminder email]
        R[Attend appointment]
    end

    A --> B --> C
    C -- No --> D --> END([🔴 End])
    C -- Yes --> E --> F
    F -- No --> G --> E
    F -- Yes --> H --> I --> J
    J -- Yes --> K --> L
    J -- No --> L
    L -- Yes --> M --> Q --> R --> END
    L -- No --> N --> O
    O -- Yes --> M
    O -- No --> P --> END
```

### Explanation
This workflow covers US-006 (FR-05). The parallel sending to both patient and caregiver (when linked) satisfies the caregiver stakeholder concern about managing a dependent's healthcare remotely. The retry mechanism directly addresses NFR-P3 (cron job reliability). This workflow runs entirely without human intervention — the System/Scheduler swimlane handles all logic automatically.

---

## Workflow 5: Medication Reminder Setup and Delivery

```mermaid
flowchart TD
    START([🟢 Start]) --> A

    subgraph Doctor_Patient ["👨‍⚕️ Doctor / 👤 Patient"]
        A[Navigate to Medication section]
        B[Click Add Medication]
        C[Enter name, dosage, frequency, reminder time]
        D[Click Save]
    end

    subgraph System ["⚙️ System"]
        E{Duplicate medication?}
        F[Show: Already exists - update instead?]
        G[Save medication record to database]
        H[Schedule daily reminder at specified time]
        I[Calculate days of supply remaining]
        J{Supply ≤ 7 days?}
        K[Queue refill alert notification]
        L[Trigger daily reminder at scheduled time]
        M[Send reminder email and in-app notification]
        N{Delivery successful?}
        O[Log reminder as Sent]
        P[Retry up to 3 times]
        Q[Log failure for IT review]
    end

    subgraph Patient ["👤 Patient / Caregiver"]
        R[Receive medication reminder]
        S[Take medication]
        T[Receive refill alert]
        U[Reorder medication]
    end

    A --> B --> C --> D --> E
    E -- Yes --> F --> C
    E -- No --> G --> H --> I --> J
    J -- Yes --> K --> T --> U --> END([🔴 End])
    J -- No --> L --> M --> N
    N -- Yes --> O --> R --> S --> END
    N -- No --> P --> Q --> END
```

### Explanation
This workflow covers US-007 (FR-06). The parallel tracks of daily reminder delivery and refill alert monitoring operate independently — the system calculates supply levels on every reminder cycle. This addresses the patient and caregiver stakeholder concerns about medication adherence, which was one of the most unique features of ClinicEase identified in the project description.

---

## Workflow 6: Doctor Consultation and Record Update

```mermaid
flowchart TD
    START([🟢 Start]) --> A

    subgraph Doctor ["👨‍⚕️ Doctor"]
        A[Log in and open dashboard]
        B[Click on today's appointment]
        C[Review patient medical history]
        D[Conduct consultation]
        E[Click Add Consultation Notes]
        F[Type diagnosis and notes]
        G[Schedule follow-up procedure if needed]
        H[Click Save]
    end

    subgraph System ["⚙️ System"]
        I[Load patient full medical history]
        J{History loaded successfully?}
        K[Show: No previous records found]
        L[Display records in chronological order]
        M{Follow-up procedure scheduled?}
        N[Create procedure record]
        O[Schedule 48h procedure reminder]
        P[Save consultation notes to database]
        Q[Update appointment status to Completed]
        R[Archive appointment in patient history]
    end

    subgraph Patient ["👤 Patient"]
        S[Receive procedure reminder 48h before]
    end

    A --> B --> I --> J
    J -- No --> K --> C
    J -- Yes --> L --> C --> D --> E --> F --> G --> H
    G --> M
    M -- Yes --> N --> O --> P & Q
    M -- No --> P & Q
    P --> R --> S --> END([🔴 End])
    Q --> END
```

### Explanation
This workflow covers US-008, US-009, US-010 (FR-07, FR-08, FR-10). The parallel actions at the end — saving notes AND updating appointment status — ensure both the patient record and the appointment record are updated atomically. The swimlane separation shows that the patient only receives the outcome (procedure reminder) without being involved in the clinical documentation process.

---

## Workflow 7: Receptionist Walk-in Patient Management

```mermaid
flowchart TD
    START([🟢 Start]) --> A

    subgraph Receptionist ["🖥️ Receptionist"]
        A[Log in to receptionist panel]
        B[Click Add Walk-in Patient]
        C{Patient registered?}
        D[Search for existing patient by name or ID]
        E[Create new patient profile]
        F[Select available doctor and slot]
        G[Confirm walk-in booking]
        N[Inform patient of their slot]
    end

    subgraph System ["⚙️ System"]
        H{Doctor available?}
        I[Show: No doctors available - suggest next slot]
        J[Create appointment - status: Confirmed]
        K[Mark slot as Booked]
        L[Send confirmation email to patient]
        M[Add patient to today's queue display]
    end

    subgraph Patient ["👤 Patient"]
        O[Wait for allocated time slot]
        P[Attend consultation]
    end

    A --> B --> C
    C -- Yes --> D --> F
    C -- No --> E --> F
    F --> H
    H -- No --> I --> F
    H -- Yes --> G --> J & K
    J --> L --> M --> N --> O --> P --> END([🔴 End])
    K --> END
```

### Explanation
This workflow covers US-011 (FR-09). The parallel actions of creating the appointment record and marking the slot as booked prevent any gap where double-booking could occur. The receptionist swimlane handles all decision-making while the system swimlane handles data operations — reflecting the real-world division of responsibility in a clinic environment. This addresses the receptionist's pain point of managing walk-ins alongside pre-booked patients.

---

## Workflow 8: Admin User Management and Report Generation

```mermaid
flowchart TD
    START([🟢 Start]) --> A

    subgraph Admin ["🔑 Administrator"]
        A[Log in to admin panel]
        B{What task?}
        C[Navigate to User Management]
        D[Search for user by name or email]
        E{Action required?}
        F[Activate account]
        G[Deactivate account]
        H[Change user role]
        N[Navigate to Reports section]
        O[Select report type]
        P[Select date range]
        Q[Click Generate Report]
        U[Download as CSV or PDF]
    end

    subgraph System ["⚙️ System"]
        I[Update user status in database]
        J[Log action with timestamp and admin ID]
        K[Send notification email to affected user]
        L{Data exists for range?}
        M[Show: No data available]
        R[Query database using indexed fields]
        S[Aggregate results]
        T[Display report table with summary stats]
    end

    A --> B
    B -- User Management --> C --> D --> E
    E -- Activate --> F --> I
    E -- Deactivate --> G --> I
    E -- Change Role --> H --> I
    I --> J --> K --> END([🔴 End])

    B -- Reports --> N --> O --> P --> Q --> L
    L -- No --> M --> END
    L -- Yes --> R --> S --> T --> U --> END
```

### Explanation
This workflow covers US-012 and US-013 (FR-11, FR-12). The two parallel tracks — user management and report generation — are both available from the same admin panel entry point. All admin actions are logged with timestamp and admin ID (shown in the System swimlane), satisfying the audit requirement identified in the Clinic Administrator stakeholder analysis from Assignment 4. Indexed database queries ensure reports generate within the performance threshold defined in NFR-S2.

---

## Traceability Summary

| Workflow | Functional Requirement | User Story | Sprint |
|---|---|---|---|
| Patient Registration | FR-01, NFR-SEC3 | US-001, US-002 | Sprint 1 |
| Doctor Search & Booking | FR-02, FR-03 | US-003, US-004 | Sprint 1 |
| Cancellation & Rescheduling | FR-04 | US-005 | Sprint 2 |
| Automated Appointment Reminder | FR-05 | US-006 | Sprint 2 |
| Medication Reminder Setup | FR-06 | US-007 | Sprint 2 |
| Doctor Consultation & Records | FR-07, FR-08, FR-10 | US-008, US-009, US-010 | Sprint 2 |
| Receptionist Walk-in Management | FR-09 | US-011 | Sprint 3 |
| Admin User Management & Reports | FR-11, FR-12 | US-012, US-013 | Sprint 3 |

---

*Document prepared by: [Sithembiso Lungisani Mthembu] | [222618698] | CPUT | March 2026*