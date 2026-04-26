# DOMAIN_MODEL.md – Domain Model Documentation

## ClinicEase Online Doctor Appointment Booking System

---

## Overview

The ClinicEase domain model identifies the core entities of the system, their attributes, responsibilities, relationships, and the business rules that govern their behaviour. This model is derived from the functional requirements (Assignment 4), use cases (Assignment 5), and state diagrams (Assignment 8).

---

## Core Domain Entities

### Entity 1: User

| Field | Details |
|---|---|
| **Description** | The base entity representing any person who interacts with the ClinicEase system. Specialised into Patient, Doctor, Receptionist, and Administrator through inheritance. |
| **Attributes** | `userId: String`, `name: String`, `email: String`, `passwordHash: String`, `role: Enum(Patient, Doctor, Receptionist, Admin)`, `status: Enum(Unverified, Active, Locked, Suspended, Deactivated, Deleted)`, `createdAt: DateTime`, `lastLoginAt: DateTime` |
| **Methods** | `register()`, `login()`, `logout()`, `updateProfile()`, `changePassword()`, `deactivate()` |
| **Relationships** | Parent of Patient, Doctor, Receptionist, Administrator (inheritance) |

**Business Rules:**
- A user's email must be unique across the entire system
- Password must be hashed with bcrypt (cost factor ≥ 12) before storage
- Account is locked after 5 consecutive failed login attempts for 15 minutes
- A user can only hold one role at a time

---

### Entity 2: Patient

| Field | Details |
|---|---|
| **Description** | A registered patient who books appointments, manages medication schedules, and views their medical records. Extends User. |
| **Attributes** | `patientId: String`, `dateOfBirth: Date`, `phone: String`, `address: String`, `medicalAidNumber: String` (optional), `caregiverId: String` (optional, FK) |
| **Methods** | `searchDoctors(query: String)`, `bookAppointment(slotId: String)`, `cancelAppointment(appointmentId: String)`, `rescheduleAppointment(appointmentId: String, newSlotId: String)`, `viewMedicalRecords()`, `addMedication(medication: Medication)`, `requestDataDeletion()` |
| **Relationships** | Books many Appointments; has many MedicalRecords; has many MedicationReminders; optionally linked to one Caregiver |

**Business Rules:**
- A patient can have at most one linked caregiver
- A patient can only view their own medical records unless explicit permission is granted
- A patient can book multiple appointments but not two appointments at the same time slot with the same doctor

---

### Entity 3: Doctor

| Field | Details |
|---|---|
| **Description** | A medical practitioner registered in the system who accepts appointments, manages their schedule, and updates patient records. Extends User. |
| **Attributes** | `doctorId: String`, `specialisation: String`, `qualifications: String`, `bio: String`, `profileStatus: Enum(Draft, Active, Unavailable, Suspended, Inactive)`, `clinicId: String` (FK) |
| **Methods** | `viewDailySchedule(date: Date)`, `viewWeeklySchedule()`, `updateConsultationNotes(appointmentId: String, notes: String)`, `scheduleProcedure(patientId: String, procedure: Procedure)`, `addMedicationForPatient(patientId: String, medication: Medication)`, `setAvailability(slots: List<TimeSlot>)`, `blockSlot(slotId: String)` |
| **Relationships** | Owns many TimeSlots; receives many Appointments; writes many MedicalRecords; schedules many Procedures |

**Business Rules:**
- A doctor must have at least one active TimeSlot to appear in patient search results
- A doctor can only update medical records for patients they have an appointment with
- A doctor in Unavailable or Suspended status cannot receive new bookings

---

### Entity 4: Appointment

| Field | Details |
|---|---|
| **Description** | The central booking entity representing a confirmed consultation between a patient and a doctor at a specific time slot. |
| **Attributes** | `appointmentId: String`, `patientId: String` (FK), `doctorId: String` (FK), `slotId: String` (FK), `status: Enum(Pending, Confirmed, Rescheduled, InProgress, Completed, Cancelled, NoShow, Expired)`, `createdAt: DateTime`, `updatedAt: DateTime`, `notes: String` (post-consultation) |
| **Methods** | `confirm()`, `cancel()`, `reschedule(newSlotId: String)`, `markInProgress()`, `markCompleted(notes: String)`, `markNoShow()`, `sendConfirmationEmail()`, `scheduleReminders()` |
| **Relationships** | Belongs to one Patient; assigned to one Doctor; occupies one TimeSlot; triggers many Notifications; linked to one MedicalRecord entry |

**Business Rules:**
- An appointment can only be Confirmed if the selected TimeSlot has status Available
- Only one appointment can occupy a given TimeSlot at any time (enforced by DB unique constraint)
- An appointment in Completed or Cancelled status cannot be modified
- Reminders are only sent for appointments with status Confirmed

---

### Entity 5: TimeSlot

| Field | Details |
|---|---|
| **Description** | A specific block of time in a doctor's schedule that can be booked by a patient. Owned by a Doctor. |
| **Attributes** | `slotId: String`, `doctorId: String` (FK), `startTime: DateTime`, `endTime: DateTime`, `status: Enum(Available, Reserved, Booked, Blocked, Completed, Expired)`, `durationMinutes: Int` |
| **Methods** | `markReserved()`, `markBooked()`, `markAvailable()`, `markBlocked()`, `markExpired()`, `isAvailable(): Boolean` |
| **Relationships** | Belongs to one Doctor; referenced by zero or one Appointment |

**Business Rules:**
- A TimeSlot can only belong to one Doctor
- A Reserved slot automatically reverts to Available after 10 minutes if not confirmed
- A TimeSlot cannot be booked if its startTime is in the past
- A Doctor can block a TimeSlot to prevent any bookings (e.g., lunch break, meeting)

---

### Entity 6: MedicalRecord

| Field | Details |
|---|---|
| **Description** | A digital record of a patient's complete medical history, including consultations, prescriptions, test results, and procedures. |
| **Attributes** | `recordId: String`, `patientId: String` (FK), `doctorId: String` (FK), `appointmentId: String` (FK), `consultationDate: DateTime`, `diagnosis: String`, `notes: String`, `prescriptions: List<String>`, `testResults: List<TestResult>`, `status: Enum(Active, Archived, PendingDeletion, Deleted)` |
| **Methods** | `addConsultationNotes(notes: String)`, `addTestResult(result: TestResult)`, `addPrescription(prescription: String)`, `archive()`, `requestDeletion()`, `getFullHistory(): List<MedicalRecord>` |
| **Relationships** | Belongs to one Patient; written by one Doctor; linked to one Appointment; may contain many TestResults |

**Business Rules:**
- Medical records are never hard-deleted immediately — they go through PendingDeletion before being purged after 30 days (POPIA compliance)
- Only the treating doctor (linked via appointmentId) can create or edit a record entry
- Patients can view but not edit their own records
- Archived records are read-only

---

### Entity 7: MedicationReminder

| Field | Details |
|---|---|
| **Description** | A scheduled daily reminder for a patient to take their medication, configured by the doctor or patient. |
| **Attributes** | `reminderId: String`, `patientId: String` (FK), `medicationName: String`, `dosage: String`, `frequencyPerDay: Int`, `reminderTimes: List<Time>`, `startDate: Date`, `endDate: Date` (optional), `supplyDays: Int`, `status: Enum(Scheduled, Active, Paused, Cancelled)` |
| **Methods** | `schedule()`, `pause()`, `resume()`, `cancel()`, `calculateDaysRemaining(): Int`, `triggerReminder()`, `sendRefillAlert()` |
| **Relationships** | Belongs to one Patient; triggers many Notifications |

**Business Rules:**
- A refill alert is sent automatically when `calculateDaysRemaining()` returns ≤ 7
- A patient cannot have two active reminders for the same medication name
- A Cancelled reminder cannot be reactivated — a new one must be created

---

### Entity 8: Notification

| Field | Details |
|---|---|
| **Description** | A system-generated message sent to a user via email or in-app alert, triggered by appointment events, medication schedules, or procedure reminders. |
| **Attributes** | `notificationId: String`, `recipientId: String` (FK → User), `type: Enum(AppointmentConfirmation, AppointmentReminder, Cancellation, MedicationReminder, RefillAlert, ProcedureReminder)`, `channel: Enum(Email, InApp)`, `status: Enum(Queued, Sending, Delivered, Failed, Retrying, PermanentFailure, Read, Archived)`, `message: String`, `sentAt: DateTime`, `retryCount: Int` |
| **Methods** | `send()`, `retry()`, `markDelivered()`, `markRead()`, `markFailed()`, `archive()` |
| **Relationships** | Sent to one User (Patient or Caregiver); triggered by Appointment, MedicationReminder, or Procedure |

**Business Rules:**
- A notification is retried up to 3 times on delivery failure before being marked PermanentFailure
- Notifications are archived after 30 days regardless of read status
- Reminder notifications are never sent for Cancelled appointments

---

## Relationships Summary

| Relationship | Type | Multiplicity | Description |
|---|---|---|---|
| User → Patient | Inheritance | 1:1 | Patient extends User |
| User → Doctor | Inheritance | 1:1 | Doctor extends User |
| User → Receptionist | Inheritance | 1:1 | Receptionist extends User |
| User → Administrator | Inheritance | 1:1 | Administrator extends User |
| Doctor → TimeSlot | Composition | 1 to 1..* | Doctor owns and controls their slots |
| TimeSlot → Appointment | Association | 1 to 0..1 | One slot holds at most one appointment |
| Patient → Appointment | Association | 1 to 0..* | Patient books many appointments |
| Doctor → Appointment | Association | 1 to 0..* | Doctor receives many appointments |
| Appointment → Notification | Aggregation | 1 to 0..* | Appointment triggers notifications |
| Patient → MedicalRecord | Aggregation | 1 to 1..* | Patient has at least one record |
| Doctor → MedicalRecord | Association | 1 to 0..* | Doctor writes records |
| Patient → MedicationReminder | Composition | 1 to 0..* | Patient owns their reminders |
| MedicationReminder → Notification | Aggregation | 1 to 0..* | Reminder triggers notifications |

---

*Document prepared by: [Sithembiso lungisani Mthembu] | [222618698] | CPUT | March 2026*