"""
api/main.py
FastAPI REST API for ClinicEase — Patient, Doctor, and Appointment endpoints.
Auto-generates Swagger UI at http://localhost:8000/docs
"""
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional, List
from datetime import datetime

# Services
from services.patient_service import (
    PatientService, PatientNotFoundError,
    EmailAlreadyRegisteredError, InvalidPatientDataError
)
from services.doctor_service import (
    DoctorService, DoctorNotFoundError, InvalidDoctorDataError
)
from services.appointment_service import (
    AppointmentService, AppointmentNotFoundError,
    SlotNotAvailableError, SlotNotFoundError,
    InvalidAppointmentError, PatientNotFoundError as ApptPatientNotFound,
    DoctorNotFoundError as ApptDoctorNotFound
)

# Repositories
from repositories.inmemory.implementations import (
    InMemoryPatientRepository,
    InMemoryDoctorRepository,
    InMemoryAppointmentRepository,
    InMemoryTimeSlotRepository,
)

# ── App setup ────────────────────────────────────────────────

app = FastAPI(
    title="ClinicEase API",
    description=(
        "REST API for the ClinicEase Online Doctor Appointment Booking System. "
        "Manages patients, doctors, appointments, and time slots."
    ),
    version="1.0.0",
    contact={
        "name": "ClinicEase — CPUT Software Engineering",
    },
    license_info={"name": "MIT"},
)

# ── Dependency injection — wire repositories into services ───

patient_repo = InMemoryPatientRepository()
doctor_repo = InMemoryDoctorRepository()
appointment_repo = InMemoryAppointmentRepository()
slot_repo = InMemoryTimeSlotRepository()

patient_service = PatientService(patient_repo)
doctor_service = DoctorService(doctor_repo)
appointment_service = AppointmentService(
    appointment_repo, slot_repo, patient_repo, doctor_repo
)


# ══════════════════════════════════════════════════════════════
# PYDANTIC REQUEST / RESPONSE SCHEMAS
# ══════════════════════════════════════════════════════════════

class PatientCreateRequest(BaseModel):
    name: str
    email: str
    phone: Optional[str] = ""
    address: Optional[str] = ""
    date_of_birth: Optional[str] = ""

    model_config = {"json_schema_extra": {
        "example": {
            "name": "Sipho Dlamini",
            "email": "sipho@email.com",
            "phone": "0821234567",
            "address": "12 Main Road, Cape Town",
            "date_of_birth": "1990-05-15"
        }
    }}


class PatientUpdateRequest(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None


class PatientResponse(BaseModel):
    patient_id: str
    name: str
    email: str
    phone: str
    status: str


class DoctorCreateRequest(BaseModel):
    name: str
    email: str
    specialisation: str
    qualifications: Optional[str] = ""
    clinic_id: Optional[str] = ""

    model_config = {"json_schema_extra": {
        "example": {
            "name": "Dr Nomsa Khumalo",
            "email": "nkhumalo@clinic.co.za",
            "specialisation": "General Practitioner",
            "qualifications": "MBChB, University of Cape Town",
            "clinic_id": "CLINIC001"
        }
    }}


class DoctorUpdateRequest(BaseModel):
    name: Optional[str] = None
    specialisation: Optional[str] = None
    qualifications: Optional[str] = None


class DoctorResponse(BaseModel):
    doctor_id: str
    name: str
    email: str
    specialisation: str
    qualifications: str
    profile_status: str


class SlotCreateRequest(BaseModel):
    doctor_id: str
    start_time: datetime
    duration_minutes: Optional[int] = 30

    model_config = {"json_schema_extra": {
        "example": {
            "doctor_id": "D001",
            "start_time": "2026-04-15T09:00:00",
            "duration_minutes": 30
        }
    }}


class SlotResponse(BaseModel):
    slot_id: str
    doctor_id: str
    start_time: str
    end_time: str
    status: str
    duration_minutes: int


class AppointmentCreateRequest(BaseModel):
    patient_id: str
    doctor_id: str
    slot_id: str

    model_config = {"json_schema_extra": {
        "example": {
            "patient_id": "P001",
            "doctor_id": "D001",
            "slot_id": "S001"
        }
    }}


class AppointmentResponse(BaseModel):
    appointment_id: str
    patient_id: str
    doctor_id: str
    slot_id: str
    status: str


class RescheduleRequest(BaseModel):
    new_slot_id: str


class CompleteRequest(BaseModel):
    notes: Optional[str] = ""


# ── Helper serialisers ────────────────────────────────────────

def patient_to_dict(p) -> dict:
    return {
        "patient_id": p._user_id,
        "name": p.name,
        "email": p.email,
        "phone": p._phone,
        "status": p.status.value
    }

def doctor_to_dict(d) -> dict:
    return {
        "doctor_id": d._user_id,
        "name": d.name,
        "email": d.email,
        "specialisation": d.specialisation,
        "qualifications": d._qualifications,
        "profile_status": d.profile_status
    }

def appointment_to_dict(a) -> dict:
    return {
        "appointment_id": a.appointment_id,
        "patient_id": a.patient_id,
        "doctor_id": a.doctor_id,
        "slot_id": a.slot_id,
        "status": a.status.value
    }

def slot_to_dict(s) -> dict:
    return {
        "slot_id": s.slot_id,
        "doctor_id": s.doctor_id,
        "start_time": s.start_time.isoformat(),
        "end_time": s._end_time.isoformat(),
        "status": s.status.value,
        "duration_minutes": s.duration_minutes
    }


# ══════════════════════════════════════════════════════════════
# PATIENT ENDPOINTS
# ══════════════════════════════════════════════════════════════

@app.get("/api/patients", tags=["Patients"],
         summary="Get all patients",
         response_description="List of all registered patients")
def get_all_patients():
    """Return a list of all registered patients in the system."""
    patients = patient_service.get_all_patients()
    return [patient_to_dict(p) for p in patients]


@app.post("/api/patients", tags=["Patients"],
          status_code=status.HTTP_201_CREATED,
          summary="Register a new patient",
          response_description="The newly created patient")
def create_patient(request: PatientCreateRequest):
    """
    Register a new patient with the following rules:
    - Name must be at least 2 characters
    - Email must be valid and unique
    """
    try:
        patient = patient_service.register_patient(
            name=request.name,
            email=request.email,
            phone=request.phone,
            address=request.address,
            date_of_birth=request.date_of_birth
        )
        return patient_to_dict(patient)
    except EmailAlreadyRegisteredError as e:
        raise HTTPException(status_code=409, detail=str(e))
    except InvalidPatientDataError as e:
        raise HTTPException(status_code=422, detail=str(e))


@app.get("/api/patients/{patient_id}", tags=["Patients"],
         summary="Get patient by ID")
def get_patient(patient_id: str):
    """Retrieve a single patient by their unique ID."""
    try:
        return patient_to_dict(patient_service.get_patient(patient_id))
    except PatientNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.put("/api/patients/{patient_id}", tags=["Patients"],
         summary="Update patient details")
def update_patient(patient_id: str, request: PatientUpdateRequest):
    """Update a patient's name, phone, or address."""
    try:
        patient = patient_service.update_patient(
            patient_id,
            name=request.name,
            phone=request.phone,
            address=request.address
        )
        return patient_to_dict(patient)
    except PatientNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except InvalidPatientDataError as e:
        raise HTTPException(status_code=422, detail=str(e))


@app.delete("/api/patients/{patient_id}", tags=["Patients"],
            status_code=status.HTTP_204_NO_CONTENT,
            summary="Delete a patient")
def delete_patient(patient_id: str):
    """Permanently delete a patient record."""
    try:
        patient_service.delete_patient(patient_id)
    except PatientNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


# ══════════════════════════════════════════════════════════════
# DOCTOR ENDPOINTS
# ══════════════════════════════════════════════════════════════

@app.get("/api/doctors", tags=["Doctors"],
         summary="Get all doctors")
def get_all_doctors():
    """Return all doctor profiles in the system."""
    return [doctor_to_dict(d) for d in doctor_service.get_all_doctors()]


@app.get("/api/doctors/available", tags=["Doctors"],
         summary="Get available doctors")
def get_available_doctors():
    """Return only doctors with active profiles who can accept bookings."""
    return [doctor_to_dict(d) for d in doctor_service.get_available_doctors()]


@app.get("/api/doctors/search", tags=["Doctors"],
         summary="Search doctors by specialisation")
def search_doctors(specialisation: str):
    """Search for doctors by specialisation (e.g. Cardiology, General Practitioner)."""
    try:
        results = doctor_service.search_by_specialisation(specialisation)
        return [doctor_to_dict(d) for d in results]
    except InvalidDoctorDataError as e:
        raise HTTPException(status_code=422, detail=str(e))


@app.post("/api/doctors", tags=["Doctors"],
          status_code=status.HTTP_201_CREATED,
          summary="Create a doctor profile")
def create_doctor(request: DoctorCreateRequest):
    """
    Create and publish a new doctor profile.
    - Name, email, and specialisation are required
    """
    try:
        doctor = doctor_service.create_doctor(
            name=request.name,
            email=request.email,
            specialisation=request.specialisation,
            qualifications=request.qualifications,
            clinic_id=request.clinic_id
        )
        return doctor_to_dict(doctor)
    except InvalidDoctorDataError as e:
        raise HTTPException(status_code=422, detail=str(e))


@app.get("/api/doctors/{doctor_id}", tags=["Doctors"],
         summary="Get doctor by ID")
def get_doctor(doctor_id: str):
    """Retrieve a single doctor by their unique ID."""
    try:
        return doctor_to_dict(doctor_service.get_doctor(doctor_id))
    except DoctorNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.put("/api/doctors/{doctor_id}", tags=["Doctors"],
         summary="Update doctor profile")
def update_doctor(doctor_id: str, request: DoctorUpdateRequest):
    """Update a doctor's name, specialisation, or qualifications."""
    try:
        doctor = doctor_service.update_doctor(
            doctor_id,
            name=request.name,
            specialisation=request.specialisation,
            qualifications=request.qualifications
        )
        return doctor_to_dict(doctor)
    except DoctorNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except InvalidDoctorDataError as e:
        raise HTTPException(status_code=422, detail=str(e))


@app.patch("/api/doctors/{doctor_id}/unavailable", tags=["Doctors"],
           summary="Set doctor as unavailable")
def set_doctor_unavailable(doctor_id: str):
    """Mark a doctor as unavailable (e.g. on leave). No new bookings accepted."""
    try:
        doctor = doctor_service.set_unavailable(doctor_id)
        return doctor_to_dict(doctor)
    except DoctorNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.patch("/api/doctors/{doctor_id}/available", tags=["Doctors"],
           summary="Set doctor as available")
def set_doctor_available(doctor_id: str):
    """Mark a doctor as available again after a period of unavailability."""
    try:
        doctor = doctor_service.set_available(doctor_id)
        return doctor_to_dict(doctor)
    except DoctorNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.delete("/api/doctors/{doctor_id}", tags=["Doctors"],
            status_code=status.HTTP_204_NO_CONTENT,
            summary="Delete a doctor profile")
def delete_doctor(doctor_id: str):
    """Permanently remove a doctor profile from the system."""
    try:
        doctor_service.delete_doctor(doctor_id)
    except DoctorNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


# ══════════════════════════════════════════════════════════════
# APPOINTMENT ENDPOINTS
# ══════════════════════════════════════════════════════════════

@app.post("/api/slots", tags=["Appointments"],
          status_code=status.HTTP_201_CREATED,
          summary="Create a time slot for a doctor")
def create_slot(request: SlotCreateRequest):
    """Create a new available time slot for a doctor."""
    try:
        slot = appointment_service.create_slot(
            doctor_id=request.doctor_id,
            start_time=request.start_time,
            duration_minutes=request.duration_minutes
        )
        return slot_to_dict(slot)
    except (ApptDoctorNotFound, InvalidAppointmentError) as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.get("/api/doctors/{doctor_id}/slots", tags=["Appointments"],
         summary="Get available slots for a doctor")
def get_available_slots(doctor_id: str):
    """Return all available (unbooked) time slots for a specific doctor."""
    try:
        slots = appointment_service.get_available_slots(doctor_id)
        return [slot_to_dict(s) for s in slots]
    except ApptDoctorNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.get("/api/appointments", tags=["Appointments"],
         summary="Get all appointments")
def get_all_appointments():
    """Return all appointments in the system."""
    return [appointment_to_dict(a) for a in appointment_service.get_all_appointments()]


@app.post("/api/appointments", tags=["Appointments"],
          status_code=status.HTTP_201_CREATED,
          summary="Book an appointment")
def book_appointment(request: AppointmentCreateRequest):
    """
    Book an appointment for a patient with a doctor at a specific slot.
    - Patient and doctor must exist
    - Slot must be available (not already booked)
    - Slot is atomically reserved to prevent double-booking
    """
    try:
        appt = appointment_service.book_appointment(
            patient_id=request.patient_id,
            doctor_id=request.doctor_id,
            slot_id=request.slot_id
        )
        return appointment_to_dict(appt)
    except (ApptPatientNotFound, ApptDoctorNotFound, SlotNotFoundError) as e:
        raise HTTPException(status_code=404, detail=str(e))
    except SlotNotAvailableError as e:
        raise HTTPException(status_code=409, detail=str(e))
    except InvalidAppointmentError as e:
        raise HTTPException(status_code=422, detail=str(e))


@app.get("/api/appointments/{appointment_id}", tags=["Appointments"],
         summary="Get appointment by ID")
def get_appointment(appointment_id: str):
    """Retrieve a single appointment by its unique ID."""
    try:
        return appointment_to_dict(appointment_service.get_appointment(appointment_id))
    except AppointmentNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.get("/api/patients/{patient_id}/appointments", tags=["Appointments"],
         summary="Get all appointments for a patient")
def get_patient_appointments(patient_id: str):
    """Return all appointments booked by a specific patient."""
    try:
        appts = appointment_service.get_patient_appointments(patient_id)
        return [appointment_to_dict(a) for a in appts]
    except ApptPatientNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.get("/api/doctors/{doctor_id}/appointments", tags=["Appointments"],
         summary="Get all appointments for a doctor")
def get_doctor_appointments(doctor_id: str):
    """Return all appointments assigned to a specific doctor."""
    try:
        appts = appointment_service.get_doctor_appointments(doctor_id)
        return [appointment_to_dict(a) for a in appts]
    except ApptDoctorNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.patch("/api/appointments/{appointment_id}/cancel", tags=["Appointments"],
           summary="Cancel an appointment")
def cancel_appointment(appointment_id: str):
    """
    Cancel a confirmed appointment.
    - The time slot is released back to Available
    - Cannot cancel a Completed or already Cancelled appointment
    """
    try:
        appt = appointment_service.cancel_appointment(appointment_id)
        return appointment_to_dict(appt)
    except AppointmentNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except InvalidAppointmentError as e:
        raise HTTPException(status_code=422, detail=str(e))


@app.patch("/api/appointments/{appointment_id}/reschedule", tags=["Appointments"],
           summary="Reschedule an appointment")
def reschedule_appointment(appointment_id: str, request: RescheduleRequest):
    """
    Reschedule a confirmed appointment to a new available slot.
    - Old slot is released back to Available
    - New slot must be Available
    """
    try:
        appt = appointment_service.reschedule_appointment(
            appointment_id, request.new_slot_id
        )
        return appointment_to_dict(appt)
    except AppointmentNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except (SlotNotFoundError, SlotNotAvailableError) as e:
        raise HTTPException(status_code=409, detail=str(e))
    except InvalidAppointmentError as e:
        raise HTTPException(status_code=422, detail=str(e))


@app.patch("/api/appointments/{appointment_id}/complete", tags=["Appointments"],
           summary="Complete an appointment")
def complete_appointment(appointment_id: str, request: CompleteRequest):
    """Mark an appointment as completed with optional consultation notes."""
    try:
        appt = appointment_service.complete_appointment(
            appointment_id, request.notes
        )
        return appointment_to_dict(appt)
    except AppointmentNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except InvalidAppointmentError as e:
        raise HTTPException(status_code=422, detail=str(e))


# ── Health check ─────────────────────────────────────────────

@app.get("/", tags=["Health"], summary="API health check")
def root():
    """Health check endpoint — confirms the API is running."""
    return {
        "service": "ClinicEase API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs",
        "entities": ["patients", "doctors", "appointments"]
    }