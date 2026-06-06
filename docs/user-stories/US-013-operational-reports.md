# US-013: Admin Generates Operational Reports 📊🏥

## Document Purpose

This document expands and strengthens the user story for **US-013: Admin generates operational reports**.

The original issue already defines the main user story, priority, story points, linked requirement, linked use case, and acceptance criteria. This document builds on that foundation by adding deeper implementation guidance, reporting logic, validation expectations, API behaviour, export rules, edge cases, and suggested test scenarios.

The purpose of this contribution is not to implement the reporting feature directly. Instead, it creates a clear and developer-friendly specification that future contributors can use when building the operational reporting module.

This makes the feature easier to understand, easier to implement, easier to test, and easier to review.

---

## Linked GitHub Issue

**Issue:** `#13 [US-013] Admin generates operational reports`

**User Story:**  
As a clinic administrator, I want to generate operational reports so that I can monitor clinic performance and identify improvement areas.

---

## Feature Summary

Operational reports allow clinic administrators to understand how the clinic is performing over a selected time period. Instead of manually counting appointment records, reviewing doctor schedules one by one, or estimating no-show patterns, the administrator should be able to generate a structured report on demand.

The report should provide a clear picture of clinic activity, including:

- how many appointments were created,
- how many appointments were completed,
- how many patients did not attend,
- how many appointments were cancelled,
- how appointment workload is distributed across doctors,
- whether the selected date range contains useful appointment data,
- and whether the report can be exported for offline use.

This feature supports better decision-making because administrators can move from guessing to using real system data.

---

## Why This Feature Matters 🌍

ClinicEase is designed to reduce long queues, missed appointments, paper-based processes, and manual clinic administration. Operational reporting supports that mission by giving administrators visibility into how the clinic is functioning.

Without reports, administrators may struggle to answer important questions such as:

- Are patients missing appointments often?
- Which doctors are overloaded with bookings?
- Are some days busier than others?
- Are appointment cancellations increasing?
- Is the clinic using its available doctor time efficiently?
- Are there periods where no appointments are being recorded?
- Is the clinic improving after introducing online booking?

Operational reports turn appointment data into management insight.

This is important because a clinic system is not only about booking appointments. It is also about helping administrators understand whether the clinic is running effectively.

---

## Business Value

The operational reports feature adds value in several ways.

| Business Area | Value Added |
|---|---|
| Clinic planning | Helps administrators understand appointment demand |
| Staff management | Shows how appointment workload is distributed across doctors |
| Service improvement | Highlights no-show trends and cancellation patterns |
| Patient care | Supports better planning so patients experience fewer delays |
| Accountability | Gives administrators evidence-based reporting instead of manual estimates |
| Efficiency | Reduces time spent preparing reports manually |
| Decision-making | Helps management identify improvement areas using real data |

---

## Stakeholder Impact

| Stakeholder | How This Feature Helps |
|---|---|
| Administrator | Can generate reports quickly and monitor clinic performance |
| Doctor | Workload patterns can be reviewed and balanced more fairly |
| Receptionist | Less pressure to manually count appointments or prepare summaries |
| Patient | Better clinic planning can reduce waiting time and improve service |
| Clinic management | Can make decisions using measurable operational data |

---

## User Story Details

| Field | Value |
|---|---|
| User Story ID | US-013 |
| Title | Admin generates operational reports |
| Actor | Clinic Administrator |
| Priority | Should-have |
| Story Points | 5 |
| Linked Requirement | FR-11 |
| Linked Use Case | UC-08 |
| Suggested Module | Reporting / Admin |
| Risk Level | Medium |
| Contribution Type | Documentation and implementation guidance |

---

## User Goal

The administrator wants to generate reports without manually calculating appointment statistics.

The system should collect appointment information, apply the selected filters, calculate summary metrics, and return the report in a format that is easy to view and export.

The administrator should be able to use the report to understand clinic performance and identify areas that need attention.

---

## Functional Scope

This feature should focus on appointment-based operational reporting.

### In Scope

The first version of the operational report should include:

- total appointments,
- completed appointments,
- cancelled appointments,
- no-show appointments,
- no-show rate,
- appointments per doctor,
- date range filtering,
- no-data handling,
- CSV export,
- PDF export.

### Out of Scope for First Version

The following features can be considered later, but should not block the first implementation:

- charts and graphs,
- automatic scheduled reports,
- email delivery of reports,
- advanced analytics,
- predictive forecasting,
- department-level comparisons,
- revenue reporting,
- patient demographic breakdowns,
- doctor performance scoring.

Keeping the first version focused will make the feature easier to implement and test.

---

## Core Report Metrics

The operational report should calculate and display the following metrics.

| Metric | Description | Example |
|---|---|---|
| Total appointments | Number of appointments in the selected date range | `120` |
| Completed appointments | Appointments marked as completed | `95` |
| Cancelled appointments | Appointments cancelled by a patient, receptionist, or admin | `10` |
| No-show appointments | Appointments where the patient did not attend | `15` |
| No-show rate | Percentage of appointments marked as no-show | `12.5%` |
| Appointments per doctor | Count of appointments grouped by doctor | `Dr Smith: 45` |
| Date range | Start and end date used for report generation | `2026-01-01 to 2026-01-31` |
| Generated timestamp | Date and time when report was generated | `2026-01-31 15:30` |

---

## No-Show Rate Calculation

The no-show rate should be calculated using the following formula:

```text
no_show_rate = (no_show_appointments / total_appointments) * 100
```