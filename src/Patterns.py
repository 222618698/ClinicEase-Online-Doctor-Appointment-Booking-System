"""
creational_patterns/patterns.py
All six creational design patterns for ClinicEase
"""

import copy
import threading
from datetime import datetime, timedelta
from typing import Optional

from src.user import UserRole
from src.users import Patient, Doctor, Receptionist, Administrator
from src.models import (
    Appointment, AppointmentStatus,
    TimeSlot, SlotStatus,
    Notification, NotificationType,
    MedicalRecord,
    MedicationReminder, ReminderStatus
)


# ══════════════════════════════════════════════════════════════
# PATTERN 1: SIMPLE FACTORY
# Creates a User object based on the role string provided.
# Centralises object creation so the caller does not need to
# know which subclass to instantiate.
# ══════════════════════════════════════════════════════════════

class UserFactory:
    """
    Simple Factory — centralises User subclass creation.
    Use case: The registration endpoint receives a role string
    from the form and calls UserFactory.create_user() to get
    the correct subclass without any if/else in the controller.
    """

    @staticmethod
    def create_user(role: str, user_id: str, name: str, email: str, **kwargs):
        """
        Factory method that returns the correct User subclass.

        Args:
            role: One of 'patient', 'doctor', 'receptionist', 'admin'
            user_id: Unique identifier
            name: Full name
            email: Email address
            **kwargs: Role-specific fields (e.g. specialisation for Doctor)

        Returns:
            Instance of Patient, Doctor, Receptionist, or Administrator

        Raises:
            ValueError: If role is not recognised
        """
        role = role.lower()
        if role == "patient":
            return Patient(
                user_id, name, email,
                date_of_birth=kwargs.get("date_of_birth", ""),
                phone=kwargs.get("phone", ""),
                address=kwargs.get("address", "")
            )
        elif role == "doctor":
            return Doctor(
                user_id, name, email,
                specialisation=kwargs.get("specialisation", ""),
                qualifications=kwargs.get("qualifications", ""),
                clinic_id=kwargs.get("clinic_id", "")
            )
        elif role == "receptionist":
            return Receptionist(
                user_id, name, email,
                clinic_id=kwargs.get("clinic_id", "")
            )
        elif role == "admin":
            return Administrator(
                user_id, name, email,
                clinic_id=kwargs.get("clinic_id", "")
            )
        else:
            raise ValueError(f"Unknown role: '{role}'. "
                             f"Must be patient, doctor, receptionist, or admin.")


# ══════════════════════════════════════════════════════════════
# PATTERN 2: FACTORY METHOD
# Defines an interface for creating a Notification, but lets
# subclasses decide which type of notification to create.
# ══════════════════════════════════════════════════════════════

class NotificationCreator:
    """
    Factory Method — abstract creator for Notifications.
    Each subclass overrides create_notification() to produce
    a specific notification type with the correct message.
    """

    def create_notification(self, notification_id: str,
                            recipient_id: str) -> Notification:
        raise NotImplementedError("Subclasses must implement create_notification()")

    def notify(self, notification_id: str, recipient_id: str) -> Notification:
        """Template method: create then send the notification."""
        notification = self.create_notification(notification_id, recipient_id)
        notification.send()
        return notification


class AppointmentConfirmationCreator(NotificationCreator):
    """Concrete creator for appointment confirmation emails."""

    def __init__(self, appointment_id: str, doctor_name: str,
                 appointment_time: str):
        self._appointment_id = appointment_id
        self._doctor_name = doctor_name
        self._appointment_time = appointment_time

    def create_notification(self, notification_id: str,
                            recipient_id: str) -> Notification:
        message = (
            f"Your appointment with Dr {self._doctor_name} "
            f"on {self._appointment_time} has been confirmed. "
            f"Reference: {self._appointment_id}"
        )
        return Notification(
            notification_id, recipient_id,
            NotificationType.APPOINTMENT_CONFIRMATION, message
        )


class MedicationReminderCreator(NotificationCreator):
    """Concrete creator for medication reminder notifications."""

    def __init__(self, medication_name: str, dosage: str):
        self._medication_name = medication_name
        self._dosage = dosage

    def create_notification(self, notification_id: str,
                            recipient_id: str) -> Notification:
        message = (
            f"Medication Reminder: Please take {self._dosage} "
            f"of {self._medication_name} now."
        )
        return Notification(
            notification_id, recipient_id,
            NotificationType.MEDICATION_REMINDER, message
        )


class CancellationNotificationCreator(NotificationCreator):
    """Concrete creator for appointment cancellation notifications."""

    def __init__(self, appointment_id: str):
        self._appointment_id = appointment_id

    def create_notification(self, notification_id: str,
                            recipient_id: str) -> Notification:
        message = (
            f"Your appointment {self._appointment_id} has been cancelled. "
            f"Please rebook at your convenience."
        )
        return Notification(
            notification_id, recipient_id,
            NotificationType.CANCELLATION, message
        )


class RefillAlertCreator(NotificationCreator):
    """Concrete creator for medication refill alert notifications."""

    def __init__(self, medication_name: str, days_remaining: int):
        self._medication_name = medication_name
        self._days_remaining = days_remaining

    def create_notification(self, notification_id: str,
                            recipient_id: str) -> Notification:
        message = (
            f"Refill Alert: You have {self._days_remaining} days of "
            f"{self._medication_name} remaining. Please arrange a refill soon."
        )
        return Notification(
            notification_id, recipient_id,
            NotificationType.REFILL_ALERT, message
        )


# ══════════════════════════════════════════════════════════════
# PATTERN 3: ABSTRACT FACTORY
# Creates families of related scheduling objects.
# Two families: StandardScheduling (normal hours) and
# UrgentScheduling (emergency / same-day appointments).
# ══════════════════════════════════════════════════════════════

class SchedulingFactory:
    """
    Abstract Factory — defines the interface for creating
    scheduling-related objects (TimeSlot + Appointment).
    """

    def create_time_slot(self, slot_id: str, doctor_id: str) -> TimeSlot:
        raise NotImplementedError

    def create_appointment(self, appointment_id: str, patient_id: str,
                           doctor_id: str, slot_id: str) -> Appointment:
        raise NotImplementedError


class StandardSchedulingFactory(SchedulingFactory):
    """
    Concrete Factory — creates standard 30-minute time slots
    and regular appointments.
    Use case: Normal scheduled consultations during clinic hours.
    """

    def create_time_slot(self, slot_id: str, doctor_id: str) -> TimeSlot:
        start = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0)
        end = start + timedelta(minutes=30)
        slot = TimeSlot(slot_id, doctor_id, start, end)
        return slot

    def create_appointment(self, appointment_id: str, patient_id: str,
                           doctor_id: str, slot_id: str) -> Appointment:
        appt = Appointment(appointment_id, patient_id, doctor_id, slot_id)
        appt.confirm()
        return appt


class UrgentSchedulingFactory(SchedulingFactory):
    """
    Concrete Factory — creates 15-minute urgent time slots
    and appointments that are auto-confirmed as high priority.
    Use case: Same-day emergency consultations.
    """

    def create_time_slot(self, slot_id: str, doctor_id: str) -> TimeSlot:
        start = datetime.now()
        end = start + timedelta(minutes=15)
        slot = TimeSlot(slot_id, doctor_id, start, end)
        return slot

    def create_appointment(self, appointment_id: str, patient_id: str,
                           doctor_id: str, slot_id: str) -> Appointment:
        appt = Appointment(appointment_id, patient_id, doctor_id, slot_id)
        appt.confirm()
        appt.mark_in_progress()  # Urgent — start immediately
        return appt


# ══════════════════════════════════════════════════════════════
# PATTERN 4: BUILDER
# Constructs complex MedicalRecord objects step by step.
# Allows building records with different optional components
# (diagnosis, prescriptions, test results, procedures).
# ══════════════════════════════════════════════════════════════

class MedicalRecordBuilder:
    """
    Builder — constructs a MedicalRecord step by step.
    Use case: After a consultation, a doctor builds a record
    by adding diagnosis, notes, prescriptions, and test results
    in separate steps rather than passing everything to a
    constructor with many parameters.
    """

    def __init__(self, record_id: str, patient_id: str,
                 doctor_id: str, appointment_id: str):
        self._record = MedicalRecord(
            record_id, patient_id, doctor_id, appointment_id
        )

    def with_diagnosis(self, diagnosis: str, notes: str = "") -> "MedicalRecordBuilder":
        self._record.add_consultation_notes(diagnosis, notes)
        return self

    def with_prescription(self, prescription: str) -> "MedicalRecordBuilder":
        self._record.add_prescription(prescription)
        return self

    def with_test_result(self, test_name: str, result: str,
                         date: str = "") -> "MedicalRecordBuilder":
        self._record.add_test_result({
            "test_name": test_name,
            "result": result,
            "date": date or datetime.now().isoformat()
        })
        return self

    def build(self) -> MedicalRecord:
        """Return the fully constructed MedicalRecord."""
        return self._record


# ══════════════════════════════════════════════════════════════
# PATTERN 5: PROTOTYPE
# Clones pre-configured MedicationReminder objects to avoid
# re-entering the same configuration for common medications.
# ══════════════════════════════════════════════════════════════

class MedicationReminderPrototype:
    """
    Prototype — stores pre-configured MedicationReminder templates
    that can be cloned and customised for individual patients.
    Use case: A doctor prescribes a common chronic medication
    (e.g., hypertension tablets). Instead of re-entering all
    settings each time, the system clones a pre-configured
    template and assigns it to the new patient.
    """

    _prototypes: dict = {}

    @classmethod
    def register(cls, name: str, reminder: MedicationReminder):
        """Register a prototype template by name."""
        cls._prototypes[name] = reminder

    @classmethod
    def clone(cls, name: str, new_reminder_id: str,
              new_patient_id: str) -> MedicationReminder:
        """
        Clone a registered prototype and assign a new ID and patient.

        Raises:
            KeyError: If prototype name is not registered
        """
        if name not in cls._prototypes:
            raise KeyError(f"No prototype registered with name '{name}'.")
        cloned = copy.deepcopy(cls._prototypes[name])
        cloned._reminder_id = new_reminder_id
        cloned._patient_id = new_patient_id
        cloned._start_date = datetime.now()
        cloned._status = ReminderStatus.SCHEDULED
        return cloned

    @classmethod
    def list_prototypes(cls) -> list:
        return list(cls._prototypes.keys())


# ══════════════════════════════════════════════════════════════
# PATTERN 6: SINGLETON
# Ensures only one DatabaseConnection instance exists globally.
# Thread-safe implementation using a lock.
# ══════════════════════════════════════════════════════════════

class DatabaseConnection:
    """
    Singleton — ensures only one database connection instance
    exists across the entire ClinicEase application.
    Use case: PostgreSQL connections are expensive to create.
    A singleton ensures the same connection pool is reused
    everywhere rather than opening a new connection per request.
    Thread-safe using double-checked locking.
    """

    _instance: Optional["DatabaseConnection"] = None
    _lock: threading.Lock = threading.Lock()

    def __new__(cls, host: str = "localhost", port: int = 5432,
                database: str = "clinicease"):
        if cls._instance is None:
            with cls._lock:
                # Double-checked locking
                if cls._instance is None:
                    instance = super().__new__(cls)
                    instance._host = host
                    instance._port = port
                    instance._database = database
                    instance._connected = False
                    instance._query_count = 0
                    cls._instance = instance
        return cls._instance

    def connect(self) -> bool:
        if not self._connected:
            # In real system: establish psycopg2 connection
            self._connected = True
        return self._connected

    def disconnect(self):
        self._connected = False

    def execute_query(self, query: str) -> str:
        if not self._connected:
            raise ConnectionError("Database not connected. Call connect() first.")
        self._query_count += 1
        return f"Query executed: {query} (total queries: {self._query_count})"

    @property
    def is_connected(self) -> bool:
        return self._connected

    @property
    def query_count(self) -> int:
        return self._query_count

    @property
    def host(self) -> str:
        return self._host

    @classmethod
    def reset_instance(cls):
        """For testing purposes only — resets the singleton."""
        with cls._lock:
            cls._instance = None

    def __repr__(self):
        return (f"<DatabaseConnection host={self._host} "
                f"port={self._port} db={self._database} "
                f"connected={self._connected}>")