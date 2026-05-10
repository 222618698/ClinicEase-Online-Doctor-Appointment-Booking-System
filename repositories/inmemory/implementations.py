"""
repositories/inmemory/implementations.py
In-memory (HashMap/dict) implementations of all repository interfaces.
Fast, zero-dependency storage — ideal for unit testing and early development.
"""
from typing import Optional, List, Dict
from repositories.interfaces import (
    PatientRepository, DoctorRepository, AppointmentRepository,
    TimeSlotRepository, MedicalRecordRepository,
    MedicationReminderRepository, NotificationRepository
)


# ══════════════════════════════════════════════════════════════
# BASE IN-MEMORY REPOSITORY
# Provides the generic CRUD implementation using a Python dict
# (equivalent to a Java HashMap). All entity-specific in-memory
# repos inherit from this to avoid repeating CRUD logic.
# ══════════════════════════════════════════════════════════════

class InMemoryRepository:
    """
    Base in-memory repository using a dict as the storage backend.
    Subclasses only need to add domain-specific query methods.
    """

    def __init__(self):
        self._storage: Dict[str, object] = {}

    def save(self, entity) -> None:
        """Store or overwrite entity keyed by its ID."""
        entity_id = self._get_id(entity)
        self._storage[entity_id] = entity

    def find_by_id(self, entity_id: str) -> Optional[object]:
        return self._storage.get(entity_id, None)

    def find_all(self) -> List[object]:
        return list(self._storage.values())

    def delete(self, entity_id: str) -> None:
        if entity_id not in self._storage:
            raise KeyError(f"Entity with id '{entity_id}' not found.")
        del self._storage[entity_id]

    def exists(self, entity_id: str) -> bool:
        return entity_id in self._storage

    def count(self) -> int:
        return len(self._storage)

    def _get_id(self, entity) -> str:
        """Extract the ID from an entity using common attribute names."""
        class_name = type(entity).__name__
        id_map = {
            "Patient": "_patient_id", "Doctor": "_doctor_id",
            "Appointment": "_appointment_id", "TimeSlot": "_slot_id",
            "MedicalRecord": "_record_id", "MedicationReminder": "_reminder_id",
            "Notification": "_notification_id",
        }
        attr = id_map.get(class_name)
        if attr and hasattr(entity, attr):
            return getattr(entity, attr)
        for attr in ("user_id", "patient_id", "doctor_id", "appointment_id",
                     "slot_id", "record_id", "reminder_id", "notification_id"):
            if hasattr(entity, attr):
                return getattr(entity, attr)
        raise AttributeError(f"Cannot determine ID for entity: {type(entity)}")


# ══════════════════════════════════════════════════════════════
# PATIENT IN-MEMORY REPOSITORY
# ══════════════════════════════════════════════════════════════

class InMemoryPatientRepository(InMemoryRepository, PatientRepository):
    """
    In-memory implementation of PatientRepository.
    Stores Patient objects in a dict keyed by patient_id.
    """

    def find_by_email(self, email: str) -> Optional[object]:
        """Linear scan — acceptable for in-memory; use indexed query for DB."""
        for patient in self._storage.values():
            if patient.email.lower() == email.lower():
                return patient
        return None

    def find_by_caregiver_id(self, caregiver_id: str) -> List:
        return [p for p in self._storage.values()
                if p._caregiver_id == caregiver_id]


# ══════════════════════════════════════════════════════════════
# DOCTOR IN-MEMORY REPOSITORY
# ══════════════════════════════════════════════════════════════

class InMemoryDoctorRepository(InMemoryRepository, DoctorRepository):
    """In-memory implementation of DoctorRepository."""

    def find_by_specialisation(self, specialisation: str) -> List:
        return [d for d in self._storage.values()
                if d.specialisation.lower() == specialisation.lower()]

    def find_available(self) -> List:
        return [d for d in self._storage.values()
                if d.profile_status == "active"]


# ══════════════════════════════════════════════════════════════
# APPOINTMENT IN-MEMORY REPOSITORY
# ══════════════════════════════════════════════════════════════

class InMemoryAppointmentRepository(InMemoryRepository, AppointmentRepository):
    """In-memory implementation of AppointmentRepository."""

    def find_by_patient_id(self, patient_id: str) -> List:
        return [a for a in self._storage.values()
                if a.patient_id == patient_id]

    def find_by_doctor_id(self, doctor_id: str) -> List:
        return [a for a in self._storage.values()
                if a.doctor_id == doctor_id]

    def find_by_status(self, status: str) -> List:
        return [a for a in self._storage.values()
                if a.status.value == status]

    def find_by_slot_id(self, slot_id: str) -> Optional[object]:
        for appt in self._storage.values():
            if appt.slot_id == slot_id:
                return appt
        return None


# ══════════════════════════════════════════════════════════════
# TIME SLOT IN-MEMORY REPOSITORY
# ══════════════════════════════════════════════════════════════

class InMemoryTimeSlotRepository(InMemoryRepository, TimeSlotRepository):
    """In-memory implementation of TimeSlotRepository."""

    def find_by_doctor_id(self, doctor_id: str) -> List:
        return [s for s in self._storage.values()
                if s.doctor_id == doctor_id]

    def find_available_by_doctor(self, doctor_id: str) -> List:
        from src.models import SlotStatus
        return [s for s in self._storage.values()
                if s.doctor_id == doctor_id
                and s.status == SlotStatus.AVAILABLE]


# ══════════════════════════════════════════════════════════════
# MEDICAL RECORD IN-MEMORY REPOSITORY
# ══════════════════════════════════════════════════════════════

class InMemoryMedicalRecordRepository(InMemoryRepository, MedicalRecordRepository):
    """In-memory implementation of MedicalRecordRepository."""

    def find_by_patient_id(self, patient_id: str) -> List:
        return [r for r in self._storage.values()
                if r.patient_id == patient_id]

    def find_by_doctor_id(self, doctor_id: str) -> List:
        return [r for r in self._storage.values()
                if r._doctor_id == doctor_id]


# ══════════════════════════════════════════════════════════════
# MEDICATION REMINDER IN-MEMORY REPOSITORY
# ══════════════════════════════════════════════════════════════

class InMemoryMedicationReminderRepository(InMemoryRepository, MedicationReminderRepository):
    """In-memory implementation of MedicationReminderRepository."""

    def find_by_patient_id(self, patient_id: str) -> List:
        return [r for r in self._storage.values()
                if r._patient_id == patient_id]

    def find_active(self) -> List:
        from src.models import ReminderStatus
        return [r for r in self._storage.values()
                if r.status in (ReminderStatus.SCHEDULED, ReminderStatus.ACTIVE)]


# ══════════════════════════════════════════════════════════════
# NOTIFICATION IN-MEMORY REPOSITORY
# ══════════════════════════════════════════════════════════════

class InMemoryNotificationRepository(InMemoryRepository, NotificationRepository):
    """In-memory implementation of NotificationRepository."""

    def find_by_recipient_id(self, recipient_id: str) -> List:
        return [n for n in self._storage.values()
                if n._recipient_id == recipient_id]

    def find_by_status(self, status: str) -> List:
        return [n for n in self._storage.values()
                if n.status.value == status]