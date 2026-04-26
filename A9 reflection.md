# a9_reflection.md – Reflection on Domain Modeling and Class Diagram Design

## ClinicEase Online Doctor Appointment Booking System — Assignment 9

---

## Introduction

Designing the domain model and class diagram for ClinicEase was the most intellectually demanding assignment of the semester. Every previous assignment contributed a piece of the picture — requirements, use cases, state diagrams, activity diagrams — but the class diagram forced me to synthesise all of that into a single, coherent structural model. The result had to be both technically accurate and practically implementable.

---

## Challenge 1: Abstraction — What Belongs in a Class and What Does Not

The first challenge was deciding what level of abstraction to use for each class. A class diagram is not a database schema — it models behaviour and responsibility, not just data storage. In my first draft, I had a `User` class with 20 attributes covering every possible user type. This was wrong. A Doctor does not need a `caregiverId` field and a Patient does not need a `specialisation` field.

The solution was to introduce inheritance. A base `User` class holds only what is common to all users — authentication credentials, status, role, and profile metadata. Each subclass (Patient, Doctor, Receptionist, Administrator) holds only what is specific to that role. This is the Single Responsibility Principle applied to class design: each class should hold only the attributes and methods that are its direct responsibility.

This decision was validated by FR-12 (Role-Based Access Control) from Assignment 4, which requires the system to enforce different permissions for different roles. Inheritance makes this natural — the role field on the base User class determines which subclass's capabilities the user has access to.

---

## Challenge 2: Choosing Between Composition, Aggregation, and Association

Deciding the correct relationship type between classes was harder than I expected. The three relationship types — composition, aggregation, and association — look similar but have very different implications for how the system behaves when objects are created or deleted.

The most difficult decision was the relationship between `Patient` and `MedicalRecord`. My first instinct was composition (strong ownership — if the patient is deleted, their records are deleted). But this would violate POPIA compliance requirements from NFR-SEC3, which requires patient data to be retained for a period after account deletion before being permanently purged. Composition would mean the records disappear the moment the account is deleted. I changed this to aggregation — the records exist independently of the patient account and survive deactivation.

By contrast, `Doctor` → `TimeSlot` is correctly composition because a time slot has no meaning outside of the doctor it belongs to. If a doctor's profile is deleted, their slots should be deleted too — there is no reason to retain an orphaned time slot with no owner.

This distinction — whether a part can survive without its whole — became my decision rule for choosing between composition and aggregation throughout the diagram.

---

## Challenge 3: Defining Methods at the Right Level

Defining methods for each class required me to think about responsibility — which class should perform which action? For example, when a patient books an appointment, who is responsible for checking slot availability? The `Patient` class calls `bookAppointment(slotId)`, but the actual availability check is performed by `TimeSlot.isAvailable()`. The `Appointment` class then calls `confirm()` to lock the booking.

This separation of responsibility — where each class handles only its own state changes — reflects the principle of encapsulation. The Patient does not need to know how availability is checked internally; it just calls the booking method and trusts the system to handle the rest. This design maps directly to the Booking workflow from the activity diagrams (Assignment 8), where the System swimlane handles the slot check independently of the Patient's actions.

---

## How the Class Diagram Aligns with Previous Assignments

The class diagram did not emerge in isolation — every class and relationship can be traced back to prior work:

**From Assignment 4 (Requirements):** Every class corresponds to at least one functional requirement. The `MedicationReminder` class exists because of FR-06. The `Notification` class exists because of FR-05, FR-06, and FR-07. The `AuditLog` class exists because of FR-11's acceptance criteria requiring admin actions to be logged with timestamps.

**From Assignment 5 (Use Cases):** The methods on each class correspond directly to use case steps. The `Patient.bookAppointment()` method is the system-side action that executes when UC-03's basic flow reaches step 6. The `Doctor.updateConsultationNotes()` method corresponds to UC-07's step 7.

**From Assignment 8 (State and Activity Diagrams):** The `status` attribute on Appointment, TimeSlot, MedicalRecord, MedicationReminder, and Notification all reflect the states modeled in the state transition diagrams. The methods on these classes (`confirm()`, `markBooked()`, `archive()`, `retry()`) are the event triggers that cause state transitions.

---

## Trade-offs Made

**Simplifying inheritance depth:** I chose a single level of inheritance (User → Patient/Doctor/Receptionist/Administrator) rather than a deeper hierarchy. A deeper hierarchy — for example, a `HealthcareWorker` intermediate class between User and Doctor — would be more theoretically correct but would add complexity without meaningful benefit for a system of this size.

**Excluding low-level infrastructure classes:** Classes like `EmailService`, `DatabaseConnection`, and `CronScheduler` exist in the implementation but are excluded from the domain class diagram. Domain class diagrams model business entities and their relationships, not technical infrastructure. Including infrastructure classes would make the diagram harder to read without adding domain value.

**Procedure as a separate class:** I debated whether `Procedure` (blood tests, injections, follow-ups) should be a subtype of `Appointment` or a separate class. I chose a separate class because a procedure does not occupy a time slot in the same way an appointment does — it has a scheduled date and preparation notes but does not go through the full booking workflow. Modelling it as a separate entity avoids forcing a procedure into the appointment lifecycle where it does not fit.

---

## Lessons Learned About Object-Oriented Design

The most important lesson from this assignment is that **good class design is discovered through constraints, not invented freely**. Every good design decision — using inheritance for users, composition for doctor-slot ownership, aggregation for patient records — was forced by a real constraint from the requirements or business rules. When I tried to design freely without constraints, I made poor choices. When I asked "what does this relationship mean if one object is deleted?", the right answer became obvious.

A second lesson is that the class diagram is the bridge between requirements and code. It is the first artifact that a developer could actually implement. Writing the class diagram revealed several gaps in the requirements — for example, the `Report` class was implied by FR-11 but never explicitly described. Modeling it as a class with `exportCSV()` and `exportPDF()` methods made the requirement concrete and implementable.

---

*Word count: approximately 880 words*

*Document prepared by: [Sithembiso Lungisani Mthembu] | [222618698] | CPUT | March 2026*