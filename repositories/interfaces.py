"""
repositories/interfaces.py
Generic repository interface and entity-specific interfaces for ClinicEase.
"""
from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Optional, List

# Generic type variables
T = TypeVar("T")   # Entity type
ID = TypeVar("ID") # ID type (usually str)


# ══════════════════════════════════════════════════════════════
# GENERIC REPOSITORY INTERFACE
# Defines the standard CRUD contract for ALL entity repositories.
# Using generics avoids duplicating save/find/delete signatures
# across every entity-specific interface.
# ══════════════════════════════════════════════════════════════

class Repository(ABC, Generic[T, ID]):
    """
    Generic base repository interface.
    All entity repositories must implement these CRUD operations.
    """

    @abstractmethod
    def save(self, entity: T) -> None:
        """Create or update an entity in the storage backend."""
        ...

    @abstractmethod
    def find_by_id(self, entity_id: ID) -> Optional[T]:
        """Return an entity by its ID, or None if not found."""
        ...

    @abstractmethod
    def find_all(self) -> List[T]:
        """Return all entities in the storage backend."""
        ...

    @abstractmethod
    def delete(self, entity_id: ID) -> None:
        """Remove an entity by its ID."""
        ...

    @abstractmethod
    def exists(self, entity_id: ID) -> bool:
        """Return True if an entity with the given ID exists."""
        ...

    @abstractmethod
    def count(self) -> int:
        """Return the total number of stored entities."""
        ...


# ══════════════════════════════════════════════════════════════
# ENTITY-SPECIFIC INTERFACES
# Each extends the generic Repository and may add
# domain-specific query methods (e.g. find_by_email).
# ══════════════════════════════════════════════════════════════

class PatientRepository(Repository, ABC):
    """Repository interface for Patient entities."""

    @abstractmethod
    def find_by_email(self, email: str):
        """Find a patient by their email address."""
        ...

    @abstractmethod
    def find_by_caregiver_id(self, caregiver_id: str) -> List:
        """Find all patients linked to a specific caregiver."""
        ...


class DoctorRepository(Repository, ABC):
    """Repository interface for Doctor entities."""

    @abstractmethod
    def find_by_specialisation(self, specialisation: str) -> List:
        """Find all doctors with a given specialisation."""
        ...

    @abstractmethod
    def find_available(self) -> List:
        """Find all doctors with profile_status = active."""
        ...


class AppointmentRepository(Repository, ABC):
    """Repository interface for Appointment entities."""

    @abstractmethod
    def find_by_patient_id(self, patient_id: str) -> List:
        """Find all appointments for a specific patient."""
        ...

    @abstractmethod
    def find_by_doctor_id(self, doctor_id: str) -> List:
        """Find all appointments for a specific doctor."""
        ...

    @abstractmethod
    def find_by_status(self, status: str) -> List:
        """Find all appointments with a given status."""
        ...

    @abstractmethod
    def find_by_slot_id(self, slot_id: str):
        """Find the appointment occupying a specific slot."""
        ...


class TimeSlotRepository(Repository, ABC):
    """Repository interface for TimeSlot entities."""

    @abstractmethod
    def find_by_doctor_id(self, doctor_id: str) -> List:
        """Find all time slots owned by a specific doctor."""
        ...

    @abstractmethod
    def find_available_by_doctor(self, doctor_id: str) -> List:
        """Find all available (unbooked) slots for a doctor."""
        ...


class MedicalRecordRepository(Repository, ABC):
    """Repository interface for MedicalRecord entities."""

    @abstractmethod
    def find_by_patient_id(self, patient_id: str) -> List:
        """Find all records belonging to a patient."""
        ...

    @abstractmethod
    def find_by_doctor_id(self, doctor_id: str) -> List:
        """Find all records written by a doctor."""
        ...


class MedicationReminderRepository(Repository, ABC):
    """Repository interface for MedicationReminder entities."""

    @abstractmethod
    def find_by_patient_id(self, patient_id: str) -> List:
        """Find all medication reminders for a patient."""
        ...

    @abstractmethod
    def find_active(self) -> List:
        """Find all reminders with status = scheduled or active."""
        ...


class NotificationRepository(Repository, ABC):
    """Repository interface for Notification entities."""

    @abstractmethod
    def find_by_recipient_id(self, recipient_id: str) -> List:
        """Find all notifications sent to a specific user."""
        ...

    @abstractmethod
    def find_by_status(self, status: str) -> List:
        """Find all notifications with a given status."""
        ...