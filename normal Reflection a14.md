# REFLECTION.md – Open-Source Collaboration Reflection

## ClinicEase Online Doctor Appointment Booking System — Assignment 14

---

## Introduction

Preparing ClinicEase for open-source collaboration and peer review was a fundamentally different challenge from the technical work of the previous assignments. Building the system was largely a solo intellectual exercise — designing classes, writing tests, implementing patterns. But preparing it for others to contribute to forced me to think about the project from an entirely different perspective: not "how does this work?" but "how would someone who has never seen this code understand it well enough to contribute?"

---

## How I Improved the Repository Based on Peer Feedback

The peer review process revealed several gaps that I had not noticed because I was too close to the code. The most significant improvement came from feedback about the **project setup experience**. A classmate told me that after cloning the repository, they were not sure where to start — the README had technical information but no clear "first steps" section aimed at a new contributor.

In response, I restructured the README to include a dedicated **"Getting Started"** section at the top, with a numbered list of exactly four commands needed to go from a fresh clone to running tests. I also added a **"Features for Contribution"** table that maps roadmap items to specific files in the codebase, so a contributor knows immediately which file to open when picking up an issue.

A second piece of feedback was that the issues on GitHub had no labels, making it impossible for newcomers to know which tasks were appropriate for their skill level. I addressed this by adding `good-first-issue` labels to five simple tasks — such as adding a new test case for an existing feature — and `feature-request` labels to three more complex items from the ROADMAP. This labelling system is standard practice in major open-source projects like Django and FastAPI, and it makes a repository immediately more welcoming to newcomers.

---

## Challenges in Onboarding Contributors

The biggest challenge in onboarding contributors was the **gap between how the code works locally and how it behaves in different environments**. The `sys.path` problem that caused multiple CI/CD failures (Assignment 13) is a perfect example. On my Windows machine, the conftest.py approach worked perfectly. But when GitHub Actions ran the same tests on Ubuntu Linux with a doubled folder path, the imports broke completely.

This experience taught me that good onboarding documentation must not assume the contributor's environment is identical to the developer's. The CONTRIBUTING.md I wrote explicitly states the Python version, the exact pip install command, and how to verify the setup by running all 188 tests before writing a single line of code.

A second challenge was writing issues that are genuinely self-contained for a newcomer. My first attempt at writing `good-first-issue` tickets were too vague — "add tests for the medication module" — which required the contributor to understand the entire medication module before even knowing what to test. I rewrote them to be more specific: "Add a test case to `tests/test_services.py` that verifies `MedicationService.cancel()` changes the reminder status to `ReminderStatus.CANCELLED`." This specificity reduces the cognitive load on new contributors significantly.

---

## Lessons Learned About Open-Source Collaboration

**Documentation is a first-class feature.** Before this assignment, I treated markdown files as an afterthought — something to fill in after the code was done. The peer review process made it clear that for many potential contributors, the documentation IS the product. If the CONTRIBUTING.md is unclear or the README does not explain how to run the project, a contributor will simply move on to another repository. Time spent on documentation is not time away from development — it is development.

**The CI/CD pipeline is an onboarding tool.** When a contributor submits a PR and the GitHub Actions pipeline automatically runs 188 tests and either passes or gives clear error messages, it removes the need for a maintainer to manually review every line of code for correctness. The pipeline acts as an always-available, always-objective reviewer. This is especially valuable in a class setting where the "maintainer" (me) cannot be available 24 hours a day to review contributions.

**Stars and forks are lagging indicators.** The peer voting process made me realise that stars and forks are a consequence of quality, not a cause of it. Repositories that are well-documented, have a working CI pipeline, and have clearly labelled beginner issues naturally attract more engagement. The technical work of Assignments 3 through 13 was the foundation — Assignment 14 was about making that foundation visible and accessible to others.

**Open source requires empathy.** The most important lesson is that contributing to an open-source project is an act of trust. A contributor trusts that the maintainer will review their work fairly, give constructive feedback, and merge good contributions. Preparing ClinicEase for open-source collaboration was ultimately an exercise in designing for others — which is the same skill at the heart of good software engineering.

---

*Word count: approximately 720 words*

*Document prepared by: [Sithembiso Lungisani] | [222618698] | CPUT | May 2026*