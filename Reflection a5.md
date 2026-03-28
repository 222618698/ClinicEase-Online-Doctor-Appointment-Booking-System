# REFLECTION_A5.md – Challenges in Translating Requirements to Use Cases and Test Cases

## ClinicEase Online Doctor Appointment Booking System

---

Translating the stakeholder requirements from Assignment 4 into use case diagrams, detailed specifications, and test cases was one of the most challenging yet rewarding parts of the ClinicEase project. While the requirements document told us *what* the system must do, use cases forced me to think about *how* users actually interact with the system step by step — and test cases forced me to think about *when* the system could fail.

### Challenge 1: Deciding the Right Level of Detail for Use Cases

The first major challenge was determining how granular each use case should be. For example, "Send Email Notification" could either be its own separate use case or folded into each booking-related use case. If I made it too granular, the diagram would become cluttered with dozens of tiny use cases. If I made it too high-level, important system behaviour would be invisible.

I resolved this by treating "Send Email Notification" as a shared included use case (UC-19) that other use cases reference via an `includes` relationship. This kept the diagram clean while still making it clear that email delivery is a critical shared behaviour across booking, cancellation, rescheduling, and all reminder types. This decision was directly driven by the requirement FR-05 which states reminders must be sent via email.

### Challenge 2: Modelling the Automated System as an Actor

One unexpected challenge was deciding how to represent the automated cron job scheduler in the use case diagram. Traditional use case theory defines actors as humans or external systems that interact with the subject system. However, in ClinicEase, the scheduler is internal — it runs inside the system itself and triggers notifications without any human input.

After research, I decided to model it as a separate "System/Scheduler" actor to make the automated behaviour visible and explicit. This is important for the IT staff stakeholder, who needs to understand that the reminder system operates independently and must be monitored. Without representing the scheduler as an actor, the reminder use cases would appear to have no trigger, which would be confusing and incomplete.

### Challenge 3: Writing Meaningful Alternative Flows

Writing the basic flow for each use case was straightforward, but writing meaningful alternative flows required me to think like a tester rather than a developer. It is easy to write a happy path — the scenario where everything works. The hard part is imagining every realistic way the flow could break down.

For example, for UC-03 (Book an Appointment), I initially only considered the case where the slot was available. But then I realised that two users could attempt to book the same slot at exactly the same moment — a classic race condition. This led me to specify in both the use case and the test cases (TC-006) that the system must use a database uniqueness constraint to prevent double-booking, not just a front-end check. This was a direct improvement to the system design that came from writing use cases carefully.

### Challenge 4: Making Test Cases Specific and Traceable

Writing test cases that are genuinely useful — not just obvious — was harder than expected. It was tempting to write vague tests like "verify the system works correctly." The assignment required specific, traceable test cases with clear expected results, and the rubric required alignment with the functional requirements from Assignment 4.

The discipline of tracing every test case back to a specific requirement (e.g., TC-005 traces to FR-03) forced me to check whether every requirement I wrote in Assignment 4 was actually testable. I discovered that some of my earlier requirements were not specific enough. For example, FR-05 originally said reminders should be sent "on time" — which is untestable. I refined it to say "24 hours and 1 hour before the appointment," which gave me a clear, measurable criterion for TC-009.

### Challenge 5: Balancing Functional and Non-Functional Test Coverage

The assignment required at least two non-functional test cases covering areas like performance and security. This was challenging because non-functional testing requires different tools and mindsets compared to functional testing. A functional test checks whether a feature works; a non-functional test checks whether it works *well enough* under pressure.

For TC-NFR-001 (performance), I had to specify the load testing tool (k6/JMeter), the number of concurrent users (500), and the exact threshold (2 seconds for 95% of requests). For TC-NFR-002 (security), I had to specify exactly how to verify bcrypt hashing — not just "check the password is secure" but "inspect the database and confirm the value starts with $2b$12$." This level of specificity was uncomfortable at first because it felt overly technical, but it is precisely what makes a test case useful in a real project.

### Conclusion

This assignment taught me that requirements engineering is not complete after writing the SRD. Use cases and test cases are the bridge between what the system is supposed to do and what it actually does in practice. The process of writing them revealed gaps and ambiguities in my Assignment 4 requirements that I was then able to correct. Going forward, I will write use cases and at least draft test cases in parallel with requirements — because the two activities sharpen each other.

---

*Word count: approximately 750 words*

*Document prepared by: [Sithembiso ] | [222618698 ] | CPUT | March 2026*