"""
factories/repository_factory.py
Factory Pattern implementation for switching between storage backends.
Decouples business logic from storage details — swap backends without
changing any service or controller code.
"""
from repositories.inmemory.implementations import (
    InMemoryPatientRepository,
    InMemoryDoctorRepository,
    InMemoryAppointmentRepository,
    InMemoryTimeSlotRepository,
    InMemoryMedicalRecordRepository,
    InMemoryMedicationReminderRepository,
    InMemoryNotificationRepository,
)


# ══════════════════════════════════════════════════════════════
# REPOSITORY FACTORY
# Returns the correct repository implementation based on the
# storage type string. Adding a new backend (e.g. DATABASE)
# only requires adding a new case here — no other code changes.
# ══════════════════════════════════════════════════════════════

class RepositoryFactory:
    """
    Factory that returns repository implementations by storage type.

    Supported storage types:
        "MEMORY"     — In-memory dict (default, for testing/dev)
        "FILESYSTEM" — JSON file storage (stub, future implementation)
        "DATABASE"   — PostgreSQL via psycopg2 (stub, future implementation)

    Usage:
        repo = RepositoryFactory.get_patient_repository("MEMORY")
        repo.save(patient)
    """

    SUPPORTED_TYPES = ("MEMORY", "FILESYSTEM", "DATABASE")

    @staticmethod
    def _validate(storage_type: str):
        if storage_type not in RepositoryFactory.SUPPORTED_TYPES:
            raise ValueError(
                f"Unsupported storage type: '{storage_type}'. "
                f"Choose from: {RepositoryFactory.SUPPORTED_TYPES}"
            )

    @staticmethod
    def get_patient_repository(storage_type: str = "MEMORY"):
        RepositoryFactory._validate(storage_type)
        if storage_type == "MEMORY":
            return InMemoryPatientRepository()
        elif storage_type == "FILESYSTEM":
            from repositories.filesystem.implementations import FileSystemPatientRepository
            return FileSystemPatientRepository("data/patients.json")
        elif storage_type == "DATABASE":
            from repositories.database.implementations import DatabasePatientRepository
            return DatabasePatientRepository()

    @staticmethod
    def get_doctor_repository(storage_type: str = "MEMORY"):
        RepositoryFactory._validate(storage_type)
        if storage_type == "MEMORY":
            return InMemoryDoctorRepository()
        elif storage_type == "FILESYSTEM":
            from repositories.filesystem.implementations import FileSystemDoctorRepository
            return FileSystemDoctorRepository("data/doctors.json")
        elif storage_type == "DATABASE":
            from repositories.database.implementations import DatabaseDoctorRepository
            return DatabaseDoctorRepository()

    @staticmethod
    def get_appointment_repository(storage_type: str = "MEMORY"):
        RepositoryFactory._validate(storage_type)
        if storage_type == "MEMORY":
            return InMemoryAppointmentRepository()
        elif storage_type == "FILESYSTEM":
            from repositories.filesystem.implementations import FileSystemAppointmentRepository
            return FileSystemAppointmentRepository("data/appointments.json")
        elif storage_type == "DATABASE":
            from repositories.database.implementations import DatabaseAppointmentRepository
            return DatabaseAppointmentRepository()

    @staticmethod
    def get_time_slot_repository(storage_type: str = "MEMORY"):
        RepositoryFactory._validate(storage_type)
        if storage_type == "MEMORY":
            return InMemoryTimeSlotRepository()
        elif storage_type == "FILESYSTEM":
            from repositories.filesystem.implementations import FileSystemTimeSlotRepository
            return FileSystemTimeSlotRepository("data/slots.json")
        elif storage_type == "DATABASE":
            from repositories.database.implementations import DatabaseTimeSlotRepository
            return DatabaseTimeSlotRepository()

    @staticmethod
    def get_medical_record_repository(storage_type: str = "MEMORY"):
        RepositoryFactory._validate(storage_type)
        if storage_type == "MEMORY":
            return InMemoryMedicalRecordRepository()
        elif storage_type == "FILESYSTEM":
            from repositories.filesystem.implementations import FileSystemMedicalRecordRepository
            return FileSystemMedicalRecordRepository("data/records.json")
        elif storage_type == "DATABASE":
            from repositories.database.implementations import DatabaseMedicalRecordRepository
            return DatabaseMedicalRecordRepository()

    @staticmethod
    def get_medication_reminder_repository(storage_type: str = "MEMORY"):
        RepositoryFactory._validate(storage_type)
        if storage_type == "MEMORY":
            return InMemoryMedicationReminderRepository()
        elif storage_type == "DATABASE":
            from repositories.database.implementations import DatabaseMedicationReminderRepository
            return DatabaseMedicationReminderRepository()

    @staticmethod
    def get_notification_repository(storage_type: str = "MEMORY"):
        RepositoryFactory._validate(storage_type)
        if storage_type == "MEMORY":
            return InMemoryNotificationRepository()
        elif storage_type == "DATABASE":
            from repositories.database.implementations import DatabaseNotificationRepository
            return DatabaseNotificationRepository()