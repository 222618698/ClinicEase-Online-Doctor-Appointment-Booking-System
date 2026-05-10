"""
repositories/database/implementations.py
PostgreSQL database storage stubs — future implementation.
Demonstrates how adding a new backend requires ONLY implementing
these classes — no changes to services, factories, or business logic.
"""
from typing import Optional, List
from repositories.interfaces import (
    PatientRepository, DoctorRepository, AppointmentRepository,
    TimeSlotRepository, MedicalRecordRepository,
    MedicationReminderRepository, NotificationRepository
)


class DatabaseRepository:
    """
    Base database repository stub.
    Full implementation would use psycopg2 or SQLAlchemy ORM.

    To implement:
    1. pip install psycopg2-binary sqlalchemy
    2. Replace each raise NotImplementedError with real SQL queries
    3. Use the DatabaseConnection singleton from creational_patterns/patterns.py
    """

    def __init__(self):
        # Future: inject DatabaseConnection singleton here
        # from creational_patterns.patterns import DatabaseConnection
        # self._db = DatabaseConnection()
        # self._db.connect()
        pass

    def save(self, entity) -> None:
        # Future: INSERT INTO ... ON CONFLICT DO UPDATE ...
        raise NotImplementedError("Database save() not yet implemented.")

    def find_by_id(self, entity_id: str) -> Optional[object]:
        # Future: SELECT * FROM ... WHERE id = %s
        raise NotImplementedError("Database find_by_id() not yet implemented.")

    def find_all(self) -> List:
        # Future: SELECT * FROM ...
        raise NotImplementedError("Database find_all() not yet implemented.")

    def delete(self, entity_id: str) -> None:
        # Future: DELETE FROM ... WHERE id = %s
        raise NotImplementedError("Database delete() not yet implemented.")

    def exists(self, entity_id: str) -> bool:
        # Future: SELECT EXISTS(SELECT 1 FROM ... WHERE id = %s)
        raise NotImplementedError("Database exists() not yet implemented.")

    def count(self) -> int:
        # Future: SELECT COUNT(*) FROM ...
        raise NotImplementedError("Database count() not yet implemented.")


class DatabasePatientRepository(DatabaseRepository, PatientRepository):
    """
    PostgreSQL stub for PatientRepository.
    Table: patients (patient_id, name, email, phone, address, ...)
    """
    def find_by_email(self, email: str): raise NotImplementedError
    def find_by_caregiver_id(self, caregiver_id: str): raise NotImplementedError


class DatabaseDoctorRepository(DatabaseRepository, DoctorRepository):
    """
    PostgreSQL stub for DoctorRepository.
    Table: doctors (doctor_id, name, email, specialisation, ...)
    """
    def find_by_specialisation(self, specialisation: str): raise NotImplementedError
    def find_available(self): raise NotImplementedError


class DatabaseAppointmentRepository(DatabaseRepository, AppointmentRepository):
    """
    PostgreSQL stub for AppointmentRepository.
    Table: appointments (appointment_id, patient_id, doctor_id, slot_id, status, ...)
    """
    def find_by_patient_id(self, patient_id: str): raise NotImplementedError
    def find_by_doctor_id(self, doctor_id: str): raise NotImplementedError
    def find_by_status(self, status: str): raise NotImplementedError
    def find_by_slot_id(self, slot_id: str): raise NotImplementedError


class DatabaseTimeSlotRepository(DatabaseRepository, TimeSlotRepository):
    """
    PostgreSQL stub for TimeSlotRepository.
    Table: time_slots (slot_id, doctor_id, start_time, end_time, status, ...)
    """
    def find_by_doctor_id(self, doctor_id: str): raise NotImplementedError
    def find_available_by_doctor(self, doctor_id: str): raise NotImplementedError


class DatabaseMedicalRecordRepository(DatabaseRepository, MedicalRecordRepository):
    """
    PostgreSQL stub for MedicalRecordRepository.
    Table: medical_records (record_id, patient_id, doctor_id, diagnosis, ...)
    """
    def find_by_patient_id(self, patient_id: str): raise NotImplementedError
    def find_by_doctor_id(self, doctor_id: str): raise NotImplementedError


class DatabaseMedicationReminderRepository(DatabaseRepository, MedicationReminderRepository):
    """
    PostgreSQL stub for MedicationReminderRepository.
    Table: medication_reminders (reminder_id, patient_id, medication_name, ...)
    """
    def find_by_patient_id(self, patient_id: str): raise NotImplementedError
    def find_active(self): raise NotImplementedError


class DatabaseNotificationRepository(DatabaseRepository, NotificationRepository):
    """
    PostgreSQL stub for NotificationRepository.
    Table: notifications (notification_id, recipient_id, type, status, ...)
    """
    def find_by_recipient_id(self, recipient_id: str): raise NotImplementedError
    def find_by_status(self, status: str): raise NotImplementedError