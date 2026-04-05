# REFLECTION_A6.md – Challenges in Agile Planning, Prioritisation, and Estimation

## ClinicEase Online Doctor Appointment Booking System

---

Working through Assignment 6 as a solo developer playing the roles of both Product Owner and Scrum Master simultaneously was a genuinely difficult experience — not because of a lack of understanding, but because of the internal resistance and conflict that comes with wearing both hats at once.

### The Tension Between Product Owner and Scrum Master

In a real Scrum team, the Product Owner decides *what* to build and the Scrum Master ensures the team works effectively. These roles naturally balance each other. The Product Owner pushes for more features; the Scrum Master protects the team from overcommitting. As a single person doing both, I found myself in constant internal conflict.

When planning Sprint 1, my Product Owner instinct wanted to include medication reminders, doctor schedule viewing, and receptionist management — because all of these feel important to stakeholders. But my Scrum Master instinct pushed back: that is far too much work for two weeks and would result in nothing being finished properly. This tension was genuinely uncomfortable. I had to force myself to accept that an incomplete feature is worse than a missing one, and that the sprint goal must be achievable.

I resolved this by strictly applying the MoSCoW method and asking one question for each story: *"Can the MVP exist without this?"* If the answer was yes, the story moved to a later sprint. This discipline helped me settle on a focused Sprint 1 goal — the end-to-end booking flow — that is small enough to complete but valuable enough to demonstrate real progress.

### The Challenge of Estimation Without a Team

Estimating story points alone was surprisingly difficult. In a real Scrum team, Planning Poker creates healthy debate that forces the team to surface hidden complexity. Alone, I had no one to challenge my assumptions. My first estimates were consistently too low because I was thinking only about the happy path — the code that works when everything goes right.

When I added the alternative flows from Assignment 5 to my thinking — account lockout after 5 failed attempts, preventing simultaneous double-bookings, retrying failed emails — the complexity of stories like US-004 (Book an Appointment) jumped from what I initially estimated as 3 points to 5 points. This taught me that estimation must always account for error handling, edge cases, and testing — not just the core feature.

I also struggled with estimating infrastructure tasks like setting up the database schema and configuring HTTPS. These tasks have no user-facing value but are essential before any other work can proceed. I eventually treated them as sprint tasks without story points (T-019 to T-024), which is a common Agile pattern, but it felt wrong at first to do work that does not map directly to a user story.

### Prioritisation Was More Personal Than Expected

The assignment noted that as a solo developer, I am the only stakeholder — and I should use my own internal resistance as material for reflection. This was surprisingly accurate. I noticed I was consistently tempted to prioritise features I find technically interesting (the scheduler cron job, the notification system) over features that are more important to users but less exciting to build (the registration form, the search UI).

This bias is a real risk in solo projects and small teams. The most critical user-facing features are often the least technically interesting. I had to remind myself repeatedly that the patient's ability to register and book is more important than a perfectly designed notification architecture — even if the notification system is more fun to build.

The MoSCoW framework helped counteract this bias by forcing me to evaluate each story against stakeholder success metrics from Assignment 4, not against my personal interest in the implementation. Stories that directly addressed the patient's core pain point — "no way to book online without visiting the clinic" — were Must-have by definition, regardless of how exciting they were to build.

### What I Would Do Differently

If I were to restart this assignment, I would write the sprint goal *first* — before selecting user stories or estimating points. Having a clear goal statement ("a patient can book an appointment end-to-end") made every subsequent prioritisation decision easier and more consistent. I spent too long trying to select stories before I had a clear goal, which led to scope creep in my initial draft.

I would also create the GitHub issues and project board at the same time as writing this document, so that the two artifacts stay in sync. The discipline of actually creating tickets — with labels, milestones, and task checklists — makes the planning feel real rather than theoretical.

---

*Word count: approximately 690 words*

*Document prepared by: [Sithembiso lungisani mthembu] | [222618698] | CPUT | March 2026*