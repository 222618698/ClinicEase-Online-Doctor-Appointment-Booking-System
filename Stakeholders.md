# STAKEHOLDERS.md – ClinicEase Stakeholder Analysis

---

## Overview

This document identifies and analyses all key stakeholders for the **ClinicEase Online Doctor Appointment Booking System**. Each stakeholder's role, concerns, pain points, and success metrics are documented to ensure the system is built around real user needs.

---

## Stakeholder Analysis Table

### Stakeholder 1: Patient

| Field | Details |
|---|---|
| **Role** | The primary end-user of ClinicEase. Patients register on the platform, search for doctors, book appointments, receive medication reminders, and view their medical history. |
| **Key Concerns** | Easy online booking without needing to call or visit the clinic. Receiving reminders for appointments, medication doses, and blood tests. Not having to carry a paper folder to every visit. |
| **Pain Points** | Currently must travel to the clinic or wait on the phone just to book a slot. Frequently forgets medication times or follow-up test dates. Paper files are often lost or damaged. Long queues mean wasted time even for a short consultation. |
| **Success Metrics** | 80% reduction in time spent booking an appointment. Zero missed medication doses due to in-app and email reminders. Patient wait time at the clinic reduced by at least 50%. |

---

### Stakeholder 2: Doctor

| Field | Details |
|---|---|
| **Role** | Medical practitioners who use ClinicEase to view their daily and weekly appointment schedules, update patient consultation notes, and flag patients needing follow-up care. |
| **Key Concerns** | Having a clear, real-time view of their daily schedule. Being able to access a patient's full medical history before the consultation begins. Reducing time spent on administrative tasks. |
| **Pain Points** | Currently relies on paper-based or spreadsheet schedules that are prone to double-booking. Cannot easily access a patient's previous visits, prescriptions, or test results before the appointment. No way to digitally flag patients who need a follow-up. |
| **Success Metrics** | 100% of appointments visible on the doctor's digital dashboard in real time. Average consultation preparation time reduced by 30% due to instant access to patient history. Zero double-bookings per week. |

---

### Stakeholder 3: Receptionist

| Field | Details |
|---|---|
| **Role** | Clinic administrative staff who manage the appointment queue, register walk-in patients, reschedule appointments, and assist patients who are unable to use the online system themselves. |
| **Key Concerns** | A fast and simple interface for creating and rescheduling appointments. The ability to view all appointments for the day at a glance. Managing walk-in patients alongside pre-booked appointments without confusion. |
| **Pain Points** | Currently manages appointments using paper registers or basic spreadsheets. Overbooking and scheduling conflicts happen frequently. Patients who miss appointments leave gaps that cannot be filled in time. No automated way to notify patients of changes. |
| **Success Metrics** | Scheduling conflicts reduced to zero per week. Time to book or reschedule an appointment reduced to under 2 minutes. Walk-in patients integrated into the digital queue within 1 minute. |

---

### Stakeholder 4: Clinic Administrator

| Field | Details |
|---|---|
| **Role** | Manages the overall clinic operations through the ClinicEase admin panel. Responsible for adding and deactivating doctor accounts, managing clinic settings, generating reports, and ensuring the system runs smoothly. |
| **Key Concerns** | Full control over which doctors and staff have system access. Ability to generate reports on appointment volumes, no-shows, and peak times. Ensuring the system complies with POPIA (Protection of Personal Information Act). |
| **Pain Points** | No centralised digital tool to manage staff access or generate operational reports. Difficulty tracking appointment statistics manually. No visibility into how many patients are served per day or per doctor. |
| **Success Metrics** | Monthly appointment and no-show reports generated automatically with zero manual effort. All staff accounts managed from a single admin panel. Full POPIA compliance confirmed through audit logs. |

---

### Stakeholder 5: IT Support Staff

| Field | Details |
|---|---|
| **Role** | Responsible for deploying, maintaining, and monitoring the ClinicEase system. Handles server uptime, database backups, security patches, and technical troubleshooting. |
| **Key Concerns** | System must be easy to deploy and maintain. Clear API documentation for future integrations. System must have proper error logging and monitoring. Security vulnerabilities must be patched promptly. |
| **Pain Points** | Systems with poor documentation are time-consuming to maintain. No existing monitoring or alerting for system downtime. Manual database backups are unreliable. Lack of role-based access control creates security risks. |
| **Success Metrics** | System uptime of 99% or higher per month. All API endpoints documented in a developer guide. Automated daily database backups with zero data loss incidents. Security patches deployed within 48 hours of discovery. |

---

### Stakeholder 6: Patient's Family Member / Caregiver

| Field | Details |
|---|---|
| **Role** | A family member or caregiver (e.g., parent, child, or guardian) who may book appointments or manage medication reminders on behalf of a patient who is elderly, a minor, or unable to use the system independently. |
| **Key Concerns** | Ability to book and manage appointments on behalf of another person. Receiving medication and appointment reminders on behalf of the patient. Simple, easy-to-understand interface that does not require technical knowledge. |
| **Pain Points** | Currently must physically accompany the patient to the clinic just to book an appointment. No way to remotely track whether a dependent family member has taken their medication or attended their appointment. |
| **Success Metrics** | Caregivers can manage a dependent's full appointment schedule remotely from any device. Medication reminder notifications successfully delivered to the caregiver's contact details. Caregiver interface usability rating of 4/5 or higher in user testing. |

---

### Stakeholder 7: Medical Aid / Health Insurance Provider (External)

| Field | Details |
|---|---|
| **Role** | An external organisation that may in future integrate with ClinicEase to verify patient medical aid membership, pre-authorise procedures, or receive appointment records for claims processing. |
| **Key Concerns** | Secure and standardised data exchange. Patient consent before any data is shared. Accurate and timestamped appointment records for audit and claims purposes. |
| **Pain Points** | Currently receives paper-based or fax-based records from clinics. No digital channel for real-time pre-authorisation or claims verification. Manual processes create delays and errors in claims. |
| **Success Metrics** | (Future scope) Digital integration ready with a documented REST API. All shared data encrypted and patient-consented. Claims processing time reduced by 40% through digital record submission. |

---

## Stakeholder Priority Summary

| Stakeholder | Priority | Influence | Interest |
|---|---|---|---|
| Patient | High | Medium | Very High |
| Doctor | High | High | High |
| Receptionist | High | Medium | High |
| Clinic Administrator | High | Very High | High |
| IT Support Staff | Medium | High | Medium |
| Family Member / Caregiver | Medium | Low | Very High |
| Medical Aid Provider | Low (future) | Medium | Medium |

---

*Document prepared by: [Sithembiso] | [222618698] | CPUT | March 2026*