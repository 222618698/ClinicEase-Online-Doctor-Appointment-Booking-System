# USE_CASE_SPECS.md – Use Case Specifications

## ClinicEase Online Doctor Appointment Booking System

---

## UC-01: Register and Login

| Field | Details |
|---|---|
| **Use Case ID** | UC-01 |
| **Actor(s)** | Patient, Doctor, Receptionist, Administrator, Caregiver |
| **Related Requirement** | FR-01 |
| **Description** | Any user creates an account and logs into the ClinicEase system to access their role-specific dashboard. |
| **Preconditions** | The user has a valid email address. The system is online and accessible. |
| **Postconditions** | The user is authenticated, a JWT token is issued, and the user is redirected to their role-specific dashboard. |

**Basic Flow:**
1. User navigates to the ClinicEase login page.
2. New user clicks "Register" and fills in name, email, password, and role.
3. User ticks the POPIA consent checkbox.
4. System validates all fields and checks the email is not already registered.
5. System hashes the password using bcrypt and saves the user record.
6. System sends a welcome email to the user's address.
7. User is redirected to the login page and enters their email and password.
8. System validates credentials and issues a JWT token.
9. User is redirected to their role-specific dashboard.

**Alternative Flows:**

*A1 — Email already registered:*
- At step 4, if the email exists, the system displays: "An account with this email already exists. Please log in."

*A2 — Incorrect password at login:*
- At step 8, if the password does not match, the system displays: "Incorrect email or password" and increments the failed login counter.

*A3 — Account locked after 5 failed attempts:*
- After 5 consecutive failed login attempts, the account is temporarily locked for 15 minutes and the user is notified by email.

---

## UC-02: Search for a Doctor

| Field | Details |
|---|---|
| **Use Case ID** | UC-02 |
| **Actor(s)** | Patient, Caregiver |
| **Related Requirement** | FR-02 |
| **Description** | A patient or caregiver searches for an available doctor by name, specialisation, or date to find a suitable appointment slot. |
| **Preconditions** | The user is logged in. At least one doctor is registered in the system. |
| **Postconditions** | A list of matching doctors with available slots is displayed to the user. |

**Basic Flow:**
1. User navigates to the "Find a Doctor" page.
2. User enters a search term (name, specialisation, or date) in the search field.
3. User clicks the "Search" button.
4. System queries the database for doctors matching the search criteria.
5. System returns a list of matching doctors showing name, specialisation, qualifications, and next available slot.
6. User clicks on a doctor's profile to view full details and available time slots.

**Alternative Flows:**

*A1 — No results found:*
- At step 5, if no doctors match the criteria, the system displays: "No doctors found matching your search. Please try a different name or specialisation."

*A2 — Doctor fully booked:*
- At step 5, fully booked doctors appear in the results with a "No slots available" badge. The user cannot click to book.

---

## UC-03: Book an Appointment

| Field | Details |
|---|---|
| **Use Case ID** | UC-03 |
| **Actor(s)** | Patient, Caregiver, Receptionist |
| **Related Requirement** | FR-03 |
| **Description** | A patient, caregiver, or receptionist selects an available doctor and time slot to create a confirmed appointment. |
| **Preconditions** | The user is logged in. The selected doctor has at least one available time slot. |
| **Postconditions** | A new appointment record is created with status "Confirmed". The time slot is marked as booked. A confirmation email is sent to the patient. |

**Basic Flow:**
1. User selects a doctor from the search results (UC-02).
2. System displays the doctor's available time slots for the selected date.
3. User selects a preferred time slot.
4. System checks that the slot is still available (includes UC-18: Check Slot Availability).
5. User confirms the booking by clicking "Book Appointment."
6. System creates the appointment record in the database and marks the slot as booked.
7. System triggers a confirmation email to the patient (includes UC-19: Send Email Notification).
8. System displays: "Appointment confirmed! You will receive a confirmation email shortly."

**Alternative Flows:**

*A1 — Slot taken by another user simultaneously:*
- At step 4, if the slot is no longer available, the system displays: "Sorry, this slot was just booked by another patient. Please select a different time."

*A2 — User not logged in:*
- If the user attempts to book without being logged in, they are redirected to the login page and returned to the booking flow after authentication.

---

## UC-04: Cancel or Reschedule an Appointment

| Field | Details |
|---|---|
| **Use Case ID** | UC-04 |
| **Actor(s)** | Patient, Caregiver, Receptionist |
| **Related Requirement** | FR-04 |
| **Description** | A patient, caregiver, or receptionist cancels an existing appointment or reschedules it to a new available time slot. |
| **Preconditions** | The user is logged in. The appointment exists with status "Confirmed." |
| **Postconditions** | If cancelled: appointment status is updated to "Cancelled" and the time slot is released. If rescheduled: the old slot is released and the new slot is marked as booked. The patient receives an email notification. |

**Basic Flow:**
1. User navigates to "My Appointments" or the receptionist's appointment panel.
2. User selects the appointment they wish to change.
3. User clicks "Cancel" or "Reschedule."
4. For rescheduling: user selects a new available time slot from the doctor's calendar.
5. System updates the appointment record and releases or reassigns the time slot.
6. System triggers an email notification to the patient confirming the change (includes UC-19).
7. System displays a success message confirming the cancellation or new appointment time.

**Alternative Flows:**

*A1 — Appointment already cancelled:*
- At step 2, if the appointment is already cancelled, the "Cancel" button is disabled and a message reads: "This appointment has already been cancelled."

*A2 — No available slots for rescheduling:*
- At step 4, if no alternative slots are available, the system displays: "No available slots for this doctor. Please try a different date or choose another doctor."

---

## UC-05: Receive Appointment Reminder

| Field | Details |
|---|---|
| **Use Case ID** | UC-05 |
| **Actor(s)** | Patient, Caregiver, System/Scheduler |
| **Related Requirement** | FR-05 |
| **Description** | The system automatically sends appointment reminder notifications to the patient (and caregiver if registered) 24 hours and 1 hour before a confirmed appointment. |
| **Preconditions** | An appointment exists with status "Confirmed." The appointment is scheduled within the next 24 hours or 1 hour. The patient has a valid email address. |
| **Postconditions** | A reminder email has been delivered to the patient and caregiver (if applicable). The notification is logged in the notifications table. |

**Basic Flow:**
1. The scheduler cron job runs at regular intervals (every 30 minutes).
2. System queries the database for confirmed appointments within the next 24 hours or 1 hour.
3. For each matching appointment, the system composes a reminder email including the doctor's name, appointment date, time, and clinic location.
4. System sends the email via the SMTP service (includes UC-19: Send Email Notification).
5. If a caregiver is linked to the patient, the email is also sent to the caregiver.
6. System logs the notification in the notifications table with a timestamp.

**Alternative Flows:**

*A1 — Email delivery fails:*
- If the SMTP service returns an error, the system retries delivery up to 3 times at 5-minute intervals. If all retries fail, an error is logged for IT staff review.

*A2 — Appointment cancelled before reminder is sent:*
- If the appointment status changes to "Cancelled" before the cron job runs, no reminder is sent.

---

## UC-06: Manage Medication Schedule

| Field | Details |
|---|---|
| **Use Case ID** | UC-06 |
| **Actor(s)** | Patient, Doctor, Caregiver |
| **Related Requirement** | FR-06 |
| **Description** | A doctor prescribes a medication schedule for a patient, or a patient/caregiver adds their own medication reminders. The system stores the schedule and sends daily dose reminders. |
| **Preconditions** | The user is logged in. The patient's profile exists in the system. |
| **Postconditions** | A medication record is saved with the medication name, dosage, frequency, and reminder times. Daily reminders are scheduled. |

**Basic Flow:**
1. Doctor (or patient/caregiver) navigates to the "Medication" section of the patient's profile.
2. User clicks "Add Medication."
3. User enters medication name, dosage, frequency (e.g., twice daily), and preferred reminder times.
4. User clicks "Save."
5. System stores the medication record linked to the patient's profile.
6. System schedules daily reminder notifications at the specified times.
7. System displays: "Medication schedule saved. Reminders have been set."

**Alternative Flows:**

*A1 — Duplicate medication entry:*
- If a medication with the same name already exists in the patient's schedule, the system warns: "This medication is already in your schedule. Do you want to update the existing entry?"

*A2 — Medication nearing end of supply:*
- When the system calculates the medication will run out within 7 days based on dosage and start date, it sends a refill alert to the patient and caregiver.

---

## UC-07: View Patient Medical Records

| Field | Details |
|---|---|
| **Use Case ID** | UC-07 |
| **Actor(s)** | Doctor, Patient |
| **Related Requirement** | FR-10 |
| **Description** | A doctor accesses a patient's full medical history — including past consultations, prescriptions, and test results — before or during a consultation. A patient can also view their own records. |
| **Preconditions** | The user is logged in. For doctors: the doctor has an appointment with the patient. For patients: the patient is viewing their own records. |
| **Postconditions** | The patient's records are displayed on screen. No changes are made unless the doctor saves new consultation notes. |

**Basic Flow:**
1. Doctor clicks on a patient's appointment in their dashboard.
2. System retrieves the patient's full medical history from the database.
3. System displays consultation history, prescriptions, medication schedule, and test results in chronological order.
4. Doctor reviews the records before beginning the consultation.
5. After the consultation, doctor clicks "Add Notes."
6. Doctor types consultation notes and diagnosis.
7. Doctor clicks "Save." System stores the notes linked to the appointment record.

**Alternative Flows:**

*A1 — No previous records:*
- At step 3, if the patient has no prior records, the system displays: "No previous consultations found for this patient."

*A2 — Unauthorised access attempt:*
- If a doctor tries to access records of a patient not in their schedule, the system returns a 403 Forbidden error and logs the attempt.

---

## UC-08: Generate Operational Reports

| Field | Details |
|---|---|
| **Use Case ID** | UC-08 |
| **Actor(s)** | Administrator |
| **Related Requirement** | FR-11 |
| **Description** | The administrator generates reports on clinic operations including total appointments, no-show rates, peak booking times, and appointments per doctor. |
| **Preconditions** | The administrator is logged in. Appointment data exists in the database. |
| **Postconditions** | A report is generated and displayed on screen. The administrator can download it as a CSV or PDF file. |

**Basic Flow:**
1. Administrator navigates to the "Reports" section of the admin panel.
2. Administrator selects report type (e.g., "Monthly Appointments," "No-Show Rate," "Appointments per Doctor").
3. Administrator selects the date range.
4. Administrator clicks "Generate Report."
5. System queries the database using pre-aggregated indexed queries.
6. System displays the report in a table format with summary statistics.
7. Administrator clicks "Download" to export the report as CSV or PDF.

**Alternative Flows:**

*A1 — No data for selected date range:*
- At step 6, if no appointments exist in the selected range, the system displays: "No data available for the selected period."

*A2 — Report generation timeout:*
- If the query takes longer than 10 seconds, the system displays: "Report is being generated. You will be notified when it is ready."

---

*Document prepared by: [Sithembiso] | [222618698] | CPUT | March 2026*