# ROADMAP.md – ClinicEase Project Roadmap

## ClinicEase Online Doctor Appointment Booking System

---

## Current Status — Completed ✅

| Assignment | Feature | Status |
|---|---|---|
| A3 | System Specification and C4 Architecture | ✅ Done |
| A4 | Stakeholder Analysis and Requirements | ✅ Done |
| A5 | Use Case Diagrams and Test Cases | ✅ Done |
| A6 | Agile Planning and Sprint Backlog | ✅ Done |
| A7 | GitHub Kanban Board | ✅ Done |
| A8 | State and Activity Diagrams | ✅ Done |
| A9 | Domain Model and Class Diagram | ✅ Done |
| A10 | Core Classes and Creational Patterns | ✅ Done |
| A11 | Repository Layer (in-memory) | ✅ Done |
| A12 | Service Layer and REST API (FastAPI) | ✅ Done |
| A13 | CI/CD Pipeline with GitHub Actions | ✅ Done |

---

## Phase 1 — Core Infrastructure (Next Sprint)

These features build the foundation for a production-ready system.

### 🔐 Authentication and Security
- [ ] **JWT Authentication** — Secure all API endpoints with JWT tokens
- [ ] **Role-based access control (RBAC)** — Enforce Patient/Doctor/Admin roles on API routes
- [ ] **Password reset via email** — Allow users to reset forgotten passwords
- [ ] **POPIA compliance audit log** — Track all data access for compliance

### 🗄️ Real Database Integration
- [ ] **PostgreSQL integration** — Replace in-memory repository with real PostgreSQL database
- [ ] **SQLAlchemy ORM** — Use SQLAlchemy models mapped to the domain classes
- [ ] **Database migrations with Alembic** — Manage schema changes safely
- [ ] **Connection pooling** — Optimise database performance under load

### 📧 Notification System
- [ ] **Email notifications via SendGrid** — Send real appointment confirmation emails
- [ ] **Medication reminder cron job** — Automated daily dose reminders using APScheduler
- [ ] **Blood test / procedure reminders** — 48-hour advance notification system
- [ ] **Refill alerts** — Notify patients when medication supply is ≤ 7 days

---

## Phase 2 — Feature Enhancements (Future Sprints)

### 📅 Advanced Scheduling
- [ ] **Recurring appointments** — Allow doctors to set recurring availability slots
- [ ] **Waitlist management** — Add patients to a waitlist when slots are full
- [ ] **Calendar sync** — Export appointments to Google Calendar / Outlook
- [ ] **Bulk slot creation** — Allow doctors to create multiple slots at once

### 📂 Paperless Records
- [ ] **File upload for test results** — Upload PDF/image test results to cloud storage
- [ ] **Prescription PDF generation** — Generate printable prescriptions
- [ ] **Patient record export** — Allow patients to download their full history as PDF
- [ ] **Doctor notes with templates** — Pre-built consultation note templates

### 👨‍👩‍👧 Caregiver Features
- [ ] **Caregiver account linking** — Link a caregiver to a dependent patient
- [ ] **Caregiver appointment management** — Book on behalf of a linked patient
- [ ] **Shared medication reminders** — Send reminders to both patient and caregiver
- [ ] **Emergency contact management** — Store and notify emergency contacts

---

## Phase 3 — Scaling and Performance

### ⚡ Performance
- [ ] **Redis caching** — Cache frequently accessed doctor search results
- [ ] **Async FastAPI endpoints** — Convert synchronous routes to async for better throughput
- [ ] **Database query optimisation** — Add indexes on patient_id, doctor_id, appointment date
- [ ] **Load testing with k6** — Verify system handles 500 concurrent users

### 🐳 Deployment
- [ ] **Docker containerisation** — Dockerfile and docker-compose for easy deployment
- [ ] **GitHub Actions CD to cloud** — Auto-deploy to Render/Railway on merge to main
- [ ] **Environment variable management** — Secure secrets with GitHub Secrets and .env files
- [ ] **Health check endpoint** — `/health` endpoint for monitoring uptime

---

## Phase 4 — Frontend and Mobile

### ⚛️ Web Frontend
- [ ] **React.js patient portal** — Full UI for patient booking and medication management
- [ ] **Doctor dashboard UI** — Daily schedule view with appointment management
- [ ] **Admin panel UI** — User management and report generation
- [ ] **Receptionist queue UI** — Walk-in patient and appointment management

### 📱 Mobile App (Future)
- [ ] **React Native mobile app** — Cross-platform iOS and Android patient app
- [ ] **Push notifications** — Native push reminders for appointments and medication
- [ ] **Offline support** — View appointments without an internet connection

---

## Phase 5 — Advanced Integrations

### 🏥 Healthcare Integrations
- [ ] **Medical aid verification API** — Verify patient medical aid membership
- [ ] **HL7 FHIR compliance** — Standard healthcare data exchange format
- [ ] **Pharmacy integration** — Send prescriptions directly to partner pharmacies
- [ ] **Lab results integration** — Receive test results digitally from laboratories

### 📊 Analytics and Reporting
- [ ] **Admin analytics dashboard** — Appointment volume, no-show rates, peak times
- [ ] **Doctor performance metrics** — Consultations per day, patient satisfaction
- [ ] **Automated monthly reports** — PDF reports emailed to clinic administrators
- [ ] **No-show prediction model** — ML model to predict and reduce patient no-shows

---

## How to Contribute to the Roadmap

If you want to work on any of these features:

1. Check the **Issues** tab for an existing issue
2. If none exists, **create a new issue** describing the feature
3. Label it `feature-request` and reference the roadmap item
4. Follow the [CONTRIBUTING.md](./CONTRIBUTING.md) guide to submit a PR

We welcome contributions at any phase! Check the `good-first-issue` label for beginner-friendly tasks.

---

*Last updated: May 2026 | ClinicEase — CPUT Software Engineering*