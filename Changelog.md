# CHANGELOG.md – ClinicEase Project

All notable changes to the ClinicEase project are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [Assignment 10] – 2026-03-01

### Added
- `src/user.py` – Base `User` class with bcrypt password hashing, login, lockout, and status management
- `src/users.py` – `Patient`, `Doctor`, `Receptionist`, `Administrator` subclasses extending `User`
- `src/models.py` – `Appointment`, `TimeSlot`, `Notification`, `MedicalRecord`, `MedicationReminder` classes with full state management
- `creational_patterns/patterns.py` – All six creational design patterns:
  - **Simple Factory** – `UserFactory` creates correct User subclass by role string
  - **Factory Method** – `NotificationCreator` and 4 concrete subclasses for different notification types
  - **Abstract Factory** – `StandardSchedulingFactory` and `UrgentSchedulingFactory` for different appointment families
  - **Builder** – `MedicalRecordBuilder` for step-by-step record construction
  - **Prototype** – `MedicationReminderPrototype` for cloning pre-configured medication templates
  - **Singleton** – `DatabaseConnection` with thread-safe double-checked locking
- `tests/test_all.py` – 69 unit tests covering all core classes and all 6 creational patterns
- `setup.cfg` – pytest and coverage configuration

### Test Results
- **69 tests — 69 passed — 0 failed**
- **Overall coverage: 88%**
- `creational_patterns/patterns.py`: 97% coverage
- `src/models.py`: 92% coverage
- `src/user.py`: 81% coverage
- `src/users.py`: 72% coverage

### Language Choice
Python 3.12 was chosen because:
- It is the primary language taught at CPUT for backend development
- `bcrypt`, `pytest`, and `pytest-cov` are easy to install and use
- Python's `copy.deepcopy` makes the Prototype pattern clean to implement
- `threading.Lock` provides straightforward thread-safe Singleton implementation

---

## [Assignment 9] – 2026-03-01
### Added
- `DOMAIN_MODEL.md` – 8 domain entities with attributes, methods, and business rules
- `CLASS_DIAGRAM.md` – Full Mermaid.js class diagram with 11 classes

## [Assignment 8] – 2026-03-01
### Added
- `STATE_DIAGRAMS.md` – 7 UML state transition diagrams
- `ACTIVITY_DIAGRAMS.md` – 8 UML activity diagrams with swimlanes

## [Assignment 7] – 2026-03-01
### Added
- `template_analysis.md`, `kanban_explanation.md`, `KANBAN_SETUP.md`, `reflection.md`

## [Assignment 6] – 2026-03-01
### Added
- `AGILE_PLANNING.md` – 18 user stories, MoSCoW backlog, Sprint 1 plan

## [Assignment 5] – 2026-03-01
### Added
- `USE_CASE_DIAGRAM.md`, `USE_CASE_SPECS.md`, `TEST_CASES.md`

## [Assignment 4] – 2026-03-01
### Added
- `STAKEHOLDERS.md`, `SRD.md`, `REFLECTION.md`

## [Assignment 3] – 2026-03-01
### Added
- `README.md`, `SPECIFICATION.md`, `ARCHITECTURE.md`