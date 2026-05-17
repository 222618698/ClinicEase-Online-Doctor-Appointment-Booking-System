"""
services/appointment_service.py
Business logic for Appointment operations.
Enforces booking rules and coordinates between Patient, Doctor, and Slot repositories.
"""
from datetime import datetime, timedelta
from typing import List, Optional
from src.models import Appointment, AppointmentStatus, TimeSlot, SlotStatus
from repositories.interfaces import (
    AppointmentRepository, TimeSlotRepository,
    PatientRepository, DoctorRepository
)


class AppointmentNotFoundError(Exception):
    pass

class SlotNotAvailableError(Exception):
    pass

class SlotNotFoundError(Exception):
    pass

class InvalidAppointmentError(Exception):
    pass

class PatientNotFoundError(Exception):
    pass

class DoctorNotFoundError(Exception):
    pass


class AppointmentService:
    """
    Service layer for Appointment business operations.

    Business rules enforced:
    - A slot must be Available before it can be booked
    - A patient cannot book two appointments at the same time slot
    - Only Confirmed appointments can be rescheduled
    - Completed or Cancelled appointments cannot be modified
    - Cancelling an appointment releases the slot back to Available
    """

    def __init__(self, appointment_repo: AppointmentRepository,
                 slot_repo: TimeSlotRepository,
                 patient_repo: PatientRepository,
                 doctor_repo: DoctorRepository):
        self._appt_repo = appointment_repo
        self._slot_repo = slot_repo
        self._patient_repo = patient_repo
        self._doctor_repo = doctor_repo
        self._id_counter = 1

    def _generate_id(self) -> str:
        aid = f"A{self._id_counter:03d}"
        self._id_counter += 1
        return aid

    def _generate_slot_id(self) -> str:
        self._slot_counter = getattr(self, "_slot_counter", 0) + 1
        return f"SLOT{self._slot_counter:06d}"

    def create_slot(self, doctor_id: str, start_time: datetime,
                    duration_minutes: int = 30) -> TimeSlot:
        """Create a new available time slot for a doctor."""
        doctor = self._doctor_repo.find_by_id(doctor_id)
        if not doctor:
            raise DoctorNotFoundError(f"Doctor '{doctor_id}' not found.")
        if doctor.profile_status != "active":
            raise InvalidAppointmentError(
                f"Doctor '{doctor_id}' is not available for bookings."
            )
        end_time = start_time + timedelta(minutes=duration_minutes)
        slot = TimeSlot(self._generate_slot_id(), doctor_id, start_time, end_time)
        self._slot_repo.save(slot)
        return slot

    def book_appointment(self, patient_id: str,
                         doctor_id: str, slot_id: str) -> Appointment:
        """
        Book an appointment for a patient with a doctor.

        Business rules:
        1. Patient must exist
        2. Doctor must exist and be active
        3. Slot must exist and be Available
        4. Slot is Reserved then Booked atomically to prevent double-booking
        """
        # Validate patient
        patient = self._patient_repo.find_by_id(patient_id)
        if not patient:
            raise PatientNotFoundError(f"Patient '{patient_id}' not found.")

        # Validate doctor
        doctor = self._doctor_repo.find_by_id(doctor_id)
        if not doctor:
            raise DoctorNotFoundError(f"Doctor '{doctor_id}' not found.")
        if doctor.profile_status != "active":
            raise InvalidAppointmentError(
                f"Doctor '{doctor_id}' is not currently accepting appointments."
            )

        # Validate and reserve slot
        slot = self._slot_repo.find_by_id(slot_id)
        if not slot:
            raise SlotNotFoundError(f"Time slot '{slot_id}' not found.")
        if not slot.is_available():
            raise SlotNotAvailableError(
                f"Slot '{slot_id}' is not available. "
                f"Current status: {slot.status.value}"
            )

        # Reserve then book the slot (prevents race conditions)
        slot.mark_reserved()
        slot.mark_booked()
        self._slot_repo.save(slot)

        # Create and confirm appointment
        appt_id = self._generate_id()
        appointment = Appointment(appt_id, patient_id, doctor_id, slot_id)
        appointment.confirm()
        self._appt_repo.save(appointment)

        return appointment

    def get_appointment(self, appointment_id: str) -> Appointment:
        """Retrieve an appointment by ID."""
        appt = self._appt_repo.find_by_id(appointment_id)
        if not appt:
            raise AppointmentNotFoundError(
                f"Appointment '{appointment_id}' not found."
            )
        return appt

    def get_all_appointments(self) -> List[Appointment]:
        """Return all appointments."""
        return self._appt_repo.find_all()

    def get_patient_appointments(self, patient_id: str) -> List[Appointment]:
        """Return all appointments for a specific patient."""
        patient = self._patient_repo.find_by_id(patient_id)
        if not patient:
            raise PatientNotFoundError(f"Patient '{patient_id}' not found.")
        return self._appt_repo.find_by_patient_id(patient_id)

    def get_doctor_appointments(self, doctor_id: str) -> List[Appointment]:
        """Return all appointments for a specific doctor."""
        doctor = self._doctor_repo.find_by_id(doctor_id)
        if not doctor:
            raise DoctorNotFoundError(f"Doctor '{doctor_id}' not found.")
        return self._appt_repo.find_by_doctor_id(doctor_id)

    def cancel_appointment(self, appointment_id: str) -> Appointment:
        """
        Cancel an appointment and release the slot back to Available.
        Business rule: Cannot cancel a Completed or already Cancelled appointment.
        """
        appt = self.get_appointment(appointment_id)
        if appt.status in (AppointmentStatus.COMPLETED,
                           AppointmentStatus.CANCELLED):
            raise InvalidAppointmentError(
                f"Cannot cancel appointment with status: {appt.status.value}"
            )
        appt.cancel()
        self._appt_repo.save(appt)

        # Release the slot
        slot = self._slot_repo.find_by_id(appt.slot_id)
        if slot:
            slot.mark_available()
            self._slot_repo.save(slot)

        return appt

    def reschedule_appointment(self, appointment_id: str,
                               new_slot_id: str) -> Appointment:
        """
        Reschedule an appointment to a new slot.
        Business rules:
        - Only Confirmed appointments can be rescheduled
        - New slot must be Available
        - Old slot is released back to Available
        """
        appt = self.get_appointment(appointment_id)
        if appt.status not in (AppointmentStatus.CONFIRMED,
                               AppointmentStatus.RESCHEDULED):
            raise InvalidAppointmentError(
                f"Only confirmed appointments can be rescheduled. "
                f"Current status: {appt.status.value}"
            )

        new_slot = self._slot_repo.find_by_id(new_slot_id)
        if not new_slot:
            raise SlotNotFoundError(f"New slot '{new_slot_id}' not found.")
        if not new_slot.is_available():
            raise SlotNotAvailableError(
                f"New slot '{new_slot_id}' is not available."
            )

        # Release old slot
        old_slot = self._slot_repo.find_by_id(appt.slot_id)
        if old_slot:
            old_slot.mark_available()
            self._slot_repo.save(old_slot)

        # Book new slot
        new_slot.mark_reserved()
        new_slot.mark_booked()
        self._slot_repo.save(new_slot)

        # Update appointment
        appt.reschedule(new_slot_id)
        self._appt_repo.save(appt)
        return appt

    def complete_appointment(self, appointment_id: str,
                             notes: str = "") -> Appointment:
        """Mark an appointment as completed with optional notes."""
        appt = self.get_appointment(appointment_id)
        if appt.status != AppointmentStatus.IN_PROGRESS:
            appt.mark_in_progress()
        appt.mark_completed(notes)

        slot = self._slot_repo.find_by_id(appt.slot_id)
        if slot:
            slot.mark_completed()
            self._slot_repo.save(slot)

        self._appt_repo.save(appt)
        return appt

    def get_available_slots(self, doctor_id: str) -> List[TimeSlot]:
        """Return all available slots for a doctor."""
        return self._slot_repo.find_available_by_doctor(doctor_id)

    def get_appointment_count(self) -> int:
        return self._appt_repo.count()