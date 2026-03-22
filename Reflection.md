# REFLECTION.md – Challenges Faced in Balancing Stakeholder Needs

## ClinicEase Online Doctor Appointment Booking System

---

## Introduction

Developing the requirements for ClinicEase required careful consideration of seven different stakeholders, each with unique needs, priorities, and sometimes conflicting expectations. This reflection documents the key challenges encountered in balancing those needs and the decisions made to address them.

---

## Challenge 1: Patient Convenience vs. IT Security Requirements

One of the most significant tensions was between the **patient's desire for a fast, frictionless booking experience** and the **IT staff's requirement for strong security measures**.

Patients want to log in quickly, book an appointment in as few steps as possible, and receive instant confirmations. However, IT staff require password hashing, HTTPS enforcement, JWT authentication, and POPIA-compliant consent forms — all of which add steps or processing time to the user journey.

**How I balanced it:** I designed the security measures to work in the background without disrupting the user experience. For example, bcrypt hashing happens server-side invisibly, HTTPS is enforced via automatic redirect, and the POPIA consent checkbox appears only once during registration. This way, security is not sacrificed, but the patient's experience remains smooth.

---

## Challenge 2: Doctor's Need for Detailed Patient History vs. Patient Privacy

Doctors need full access to a patient's medical history, previous prescriptions, and test results to provide effective care. However, patients have a right to privacy and may not want all their information visible to every doctor they visit.

**How I balanced it:** I implemented role-based access control (FR-12) so that only the treating doctor assigned to an appointment can view the patient's full records during that consultation. Patients can also view their own records from the patient portal (FR-10). This respects privacy while still giving doctors the information they need. POPIA compliance (NFR-SEC3) further protects patient data rights.

---

## Challenge 3: Receptionist Speed vs. System Accuracy

Receptionists need to book, reschedule, and add walk-in patients as fast as possible — sometimes during busy morning queues. This created a conflict with the system's need to validate every booking carefully to prevent double-booking and data errors.

**How I balanced it:** I introduced database-level uniqueness constraints on time slots (FR-03 acceptance criteria) so that even if the receptionist works quickly, the system prevents two bookings from occupying the same slot simultaneously. The interface is designed to show available slots only, reducing the chance of human error without slowing down the receptionist's workflow.

---

## Challenge 4: Caregiver Access vs. Patient Data Ownership

Family members and caregivers need to manage appointments and medication schedules on behalf of elderly or dependent patients. However, allowing a third party full access to another person's medical records raises serious privacy and consent concerns.

**How I balanced it:** I scoped caregiver access to only what is necessary — booking appointments, receiving reminders, and managing medication schedules. Caregivers cannot view detailed medical history or consultation notes unless the patient explicitly grants that permission. This limits access while still making the system useful for families managing a dependent's healthcare.

---

## Challenge 5: Clinic Administrator's Reporting Needs vs. System Performance

The clinic administrator wants detailed reports on appointment volumes, no-show rates, and peak booking times. Generating these reports from a live database with thousands of records could slow down the system for other users.

**How I balanced it:** I specified that reports be generated on demand (FR-11) rather than in real time, using pre-aggregated queries on indexed fields (NFR-S2). This means the database is not queried heavily during peak booking hours — reports are processed at off-peak times and cached for the administrator to view.

---

## Challenge 6: Medical Aid Provider Integration vs. Project Scope

The medical aid provider stakeholder raised a valid future need — digital integration for claims and pre-authorisation. However, including full medical aid API integration within a single semester project would have made the scope unmanageable.

**How I balanced it:** I classified medical aid integration as **out of scope** for the current semester but documented it clearly in the SPECIFICATION.md and noted that the REST API is designed to be extensible for future integration (NFR-M1, NFR-M2). This satisfies the stakeholder's concern without overcomplicating the current deliverable.

---

## Key Lessons Learned

**Requirements engineering is a negotiation.** Every stakeholder believes their needs are the most important. The role of the requirements engineer is not to satisfy everyone fully, but to find a design that satisfies everyone *enough* — especially for high-priority stakeholders like patients and doctors.

**Specificity prevents conflict.** Vague requirements like "the system should be fast" caused the most disagreement. Once I specified "booking shall complete within 2 seconds" (NFR-P2), it became easier to design and test for.

**Security and usability are not opposites.** Early on I assumed that adding security would always hurt the user experience. Through this process I learned that well-designed security (like background encryption and single-consent POPIA forms) can be invisible to the user while still fully protecting their data.

**Agile methodology allows requirements to evolve.** As stated in the assignment brief, requirements can change over the semester. Documenting stakeholder concerns in detail now means that when requirements do change, I can trace them back to a specific stakeholder need rather than making arbitrary changes.

---

*Document prepared by: [Your Full Name] | [Your Student Number] | CPUT | March 2026*