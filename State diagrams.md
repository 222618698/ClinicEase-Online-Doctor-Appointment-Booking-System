# STATE_DIAGRAMS.md – Object State Modeling

## ClinicEase Online Doctor Appointment Booking System

---

## Overview

This document models the lifecycle of 7 critical objects in the ClinicEase system using UML state transition diagrams written in Mermaid. Each diagram shows the states an object can be in, the events that trigger transitions between states, and any guard conditions that apply.

---

## Object 1: Appointment

### State Diagram

```mermaid
stateDiagram-v2
    [*] --> Pending : Patient selects time slot

    Pending --> Confirmed : [slot is available] Payment/confirmation received
    Pending --> Cancelled : Patient cancels before confirmation
    Pending --> Expired : [no action taken within 10 minutes]

    Confirmed --> Rescheduled : Patient or receptionist reschedules
    Confirmed --> Cancelled : Patient or receptionist cancels
    Confirmed --> InProgress : Doctor starts consultation
    Confirmed --> NoShow : [patient does not arrive within 15 mins of slot time]

    Rescheduled --> Confirmed : New slot confirmed
    Rescheduled --> Cancelled : Patient cancels after rescheduling

    InProgress --> Completed : Doctor ends consultation and saves notes
    InProgress --> Cancelled : Emergency cancellation during session

    NoShow --> Cancelled : Admin marks as cancelled
    NoShow --> Rescheduled : Patient requests reschedule

    Completed --> [*]
    Cancelled --> [*]
    Expired --> [*]
```

### Explanation

| State | Description |
|---|---|
| **Pending** | Appointment created but not yet confirmed. Slot is temporarily held. |
| **Confirmed** | Slot is locked. Reminders are scheduled. Patient and doctor are notified. |
| **Rescheduled** | Original slot released. New slot being selected. |
| **InProgress** | Doctor has started the consultation. |
| **Completed** | Consultation finished. Notes saved. Records updated. |
| **NoShow** | Patient did not arrive. Slot is logged for reporting. |
| **Cancelled** | Appointment terminated. Slot released immediately. |
| **Expired** | Pending appointment not confirmed within 10 minutes. Slot released. |

**Traceability:**
- Confirmed state → FR-03 (Book Appointment)
- Cancelled transition → FR-04 (Cancel/Reschedule)
- Reminders triggered from Confirmed → FR-05 (Appointment Reminders)
- NoShow state → FR-11 (Admin Reports — no-show rate)
- US-004, US-005, US-006 | UC-03, UC-04

---

## Object 2: User Account

### State Diagram

```mermaid
stateDiagram-v2
    [*] --> Unverified : User submits registration form

    Unverified --> Active : [email verified] User clicks verification link
    Unverified --> Deleted : User abandons registration / admin deletes

    Active --> Locked : [5 consecutive failed login attempts]
    Active --> Suspended : Admin suspends account
    Active --> Deactivated : Admin deactivates account
    Active --> Active : User updates profile / changes password

    Locked --> Active : [lockout period of 15 mins expires] OR admin unlocks
    Locked --> Suspended : Admin suspends while locked

    Suspended --> Active : Admin reinstates account
    Suspended --> Deactivated : Admin permanently deactivates

    Deactivated --> Active : Admin reactivates account
    Deactivated --> Deleted : Admin deletes account after POPIA request

    Deleted --> [*]
```

### Explanation

| State | Description |
|---|---|
| **Unverified** | Account created but email not yet confirmed. |
| **Active** | Full system access granted based on assigned role. |
| **Locked** | Temporary lock after 5 failed login attempts. Auto-unlocks after 15 minutes. |
| **Suspended** | Admin has suspended the account pending investigation. |
| **Deactivated** | Account disabled but data retained for audit purposes. |
| **Deleted** | All personal data removed in compliance with POPIA. |

**Traceability:**
- Active state → FR-01 (User Registration and Login)
- Locked transition → NFR-SEC1 (Security — brute force protection)
- Deleted state → NFR-SEC3 (POPIA compliance — right to erasure)
- US-001, US-002, US-015 | UC-01

---

## Object 3: Doctor Profile

### State Diagram

```mermaid
stateDiagram-v2
    [*] --> Draft : Admin creates doctor profile

    Draft --> Active : [all required fields completed] Admin publishes profile
    Draft --> Deleted : Admin discards incomplete profile

    Active --> Unavailable : Doctor marks themselves unavailable (leave/holiday)
    Active --> Suspended : Admin suspends doctor account
    Active --> Inactive : Admin deactivates profile

    Unavailable --> Active : Doctor marks themselves available again
    Unavailable --> Suspended : Admin suspends during unavailability

    Suspended --> Active : Admin reinstates doctor
    Suspended --> Inactive : Admin permanently deactivates

    Inactive --> Active : Admin reactivates profile
    Inactive --> Deleted : Admin deletes profile

    Deleted --> [*]
```

### Explanation

| State | Description |
|---|---|
| **Draft** | Profile created but not yet visible to patients. |
| **Active** | Doctor is visible in search results and can receive bookings. |
| **Unavailable** | Doctor temporarily not accepting bookings (e.g., on leave). |
| **Suspended** | Account under review. No new bookings accepted. |
| **Inactive** | Profile disabled. Not visible to patients. |
| **Deleted** | Profile permanently removed from the system. |

**Traceability:**
- Active state → FR-02 (Doctor Search)
- Unavailable state → FR-03 (Slot Availability Check)
- US-003, US-008 | UC-02, UC-07

---

## Object 4: Time Slot

### State Diagram

```mermaid
stateDiagram-v2
    [*] --> Available : Doctor or admin creates time slot

    Available --> Reserved : [appointment pending] Patient selects slot
    Available --> Blocked : Doctor blocks slot (meeting/break)
    Available --> Expired : [slot datetime has passed with no booking]

    Reserved --> Booked : [appointment confirmed] Booking completed
    Reserved --> Available : [10 minute timeout] Patient does not confirm
    Reserved --> Available : Patient cancels during pending state

    Booked --> Available : Appointment cancelled or rescheduled
    Booked --> Completed : Appointment completed successfully
    Booked --> NoShow : Patient does not arrive

    Blocked --> Available : Doctor unblocks the slot
    Blocked --> Expired : Slot datetime passes while blocked

    NoShow --> Expired : Slot logged and closed
    Completed --> Expired : Slot closed after completion

    Expired --> [*]
```

### Explanation

| State | Description |
|---|---|
| **Available** | Slot is open and visible to patients for booking. |
| **Reserved** | Temporarily held for a patient completing their booking. |
| **Booked** | Slot is confirmed and locked to a specific appointment. |
| **Blocked** | Doctor has manually blocked the slot — not available to patients. |
| **Completed** | The appointment in this slot finished successfully. |
| **NoShow** | Patient did not attend — slot is logged and then expired. |
| **Expired** | Slot datetime has passed. Removed from active availability. |

**Traceability:**
- Available → Reserved → Booked → FR-03 (Booking with slot check)
- Available release on cancel → FR-04 (Cancellation)
- Reserved timeout → NFR-P2 (Performance — fast slot release)
- US-004, US-005 | UC-03, UC-04, UC-18

---

## Object 5: Medication Reminder

### State Diagram

```mermaid
stateDiagram-v2
    [*] --> Scheduled : Doctor or patient creates medication schedule

    Scheduled --> Active : [reminder time reached] System triggers reminder
    Scheduled --> Paused : Patient pauses reminders temporarily
    Scheduled --> Cancelled : Patient or doctor removes medication from schedule

    Active --> Sent : Reminder email/notification delivered successfully
    Active --> Failed : [SMTP error] Email delivery fails

    Sent --> Scheduled : Next dose scheduled automatically
    Sent --> RefillAlert : [medication supply ≤ 7 days remaining]

    Failed --> Retrying : System retries up to 3 times
    Retrying --> Sent : Retry successful
    Retrying --> Failed : [3 retries exhausted] Logged for IT review

    RefillAlert --> Sent : Refill alert sent to patient and caregiver
    RefillAlert --> Scheduled : Patient updates supply quantity

    Paused --> Scheduled : Patient resumes reminders
    Paused --> Cancelled : Patient deletes medication from schedule

    Cancelled --> [*]
```

### Explanation

| State | Description |
|---|---|
| **Scheduled** | Reminder is set and waiting for the trigger time. |
| **Active** | Trigger time reached. Reminder being dispatched. |
| **Sent** | Reminder successfully delivered. Next dose automatically scheduled. |
| **Failed** | Delivery failed. System enters retry cycle. |
| **Retrying** | System attempting redelivery up to 3 times. |
| **RefillAlert** | Supply running low. Special refill alert dispatched. |
| **Paused** | Patient temporarily suspended reminders. |
| **Cancelled** | Medication removed from schedule entirely. |

**Traceability:**
- Scheduled → Sent → FR-06 (Medication Reminder System)
- RefillAlert state → FR-06 acceptance criteria (7-day refill alert)
- Failed → Retrying → NFR-SEC1 (system reliability)
- US-007 | UC-06

---

## Object 6: Patient Medical Record

### State Diagram

```mermaid
stateDiagram-v2
    [*] --> Created : Patient registers and profile is initialised

    Created --> Active : First consultation note or test result added

    Active --> Updated : Doctor adds consultation notes or test results
    Active --> Archived : Patient account deactivated (data retained)
    Active --> UnderReview : Admin flags record for compliance review

    Updated --> Active : Update saved successfully
    Updated --> Active : Doctor discards unsaved changes

    UnderReview --> Active : Review completed — no issues found
    UnderReview --> Archived : Record archived pending investigation

    Archived --> Active : Patient account reactivated
    Archived --> PendingDeletion : Patient submits POPIA data deletion request

    PendingDeletion --> Deleted : [30 day retention period elapsed] Data purged
    PendingDeletion --> Archived : Deletion request withdrawn by patient

    Deleted --> [*]
```

### Explanation

| State | Description |
|---|---|
| **Created** | Empty record initialised on patient registration. |
| **Active** | Record is live and being updated by doctors. |
| **Updated** | Transient state during a save operation. Returns to Active. |
| **Archived** | Record preserved but not actively updated. |
| **UnderReview** | Flagged by admin for compliance or audit review. |
| **PendingDeletion** | Patient has requested data removal under POPIA. |
| **Deleted** | All personal data permanently removed. |

**Traceability:**
- Active → Updated → FR-10 (Paperless Patient Records)
- PendingDeletion → Deleted → NFR-SEC3 (POPIA Compliance)
- US-010 | UC-07

---

## Object 7: Notification

### State Diagram

```mermaid
stateDiagram-v2
    [*] --> Queued : System event triggers notification creation

    Queued --> Sending : Notification service picks up the queued item

    Sending --> Delivered : SMTP/push service confirms delivery
    Sending --> Failed : [delivery error] Service returns failure response

    Failed --> Retrying : [retry attempt ≤ 3] System schedules retry
    Retrying --> Sending : Retry attempt begins
    Retrying --> PermanentFailure : [3rd retry fails] Escalated to IT log

    Delivered --> Read : User opens notification or email
    Delivered --> Unread : [24 hours pass] Notification marked as unread

    Read --> Archived : Notification moved to history after 30 days
    Unread --> Archived : Notification moved to history after 30 days

    PermanentFailure --> Archived : Logged and archived for IT review

    Archived --> [*]
```

### Explanation

| State | Description |
|---|---|
| **Queued** | Notification created and waiting to be dispatched. |
| **Sending** | Active dispatch attempt in progress. |
| **Delivered** | Confirmed delivery by the email/push service. |
| **Failed** | Delivery attempt failed. Retry cycle begins. |
| **Retrying** | Retry in progress. Maximum 3 retries. |
| **PermanentFailure** | All retries exhausted. IT staff alerted via log. |
| **Read** | User has opened the notification. |
| **Unread** | Delivered but not yet opened after 24 hours. |
| **Archived** | Notification moved to history log after 30 days. |

**Traceability:**
- Queued → Delivered → FR-05 (Appointment Reminders), FR-06 (Medication Reminders)
- Failed → Retrying → NFR-P3 (Cron job reliability)
- PermanentFailure → NFR-M1 (IT logging and monitoring)
- US-006, US-007, US-009 | UC-05, UC-06

---

## Traceability Summary

| Object | Key States | Functional Requirement | User Story |
|---|---|---|---|
| Appointment | Pending → Confirmed → Completed | FR-03, FR-04, FR-05 | US-004, US-005, US-006 |
| User Account | Unverified → Active → Locked | FR-01, NFR-SEC1, NFR-SEC3 | US-001, US-002, US-015 |
| Doctor Profile | Draft → Active → Unavailable | FR-02, FR-08 | US-003, US-008 |
| Time Slot | Available → Reserved → Booked | FR-03, FR-04, NFR-P2 | US-004, US-005 |
| Medication Reminder | Scheduled → Sent → RefillAlert | FR-06 | US-007 |
| Patient Medical Record | Created → Active → PendingDeletion | FR-10, NFR-SEC3 | US-010 |
| Notification | Queued → Delivered → Archived | FR-05, FR-06, NFR-P3 | US-006, US-007, US-009 |

---

*Document prepared by: [Sithembiso Mthembu] | [222618698] | CPUT | March 2026*