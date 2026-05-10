"""
repositories/filesystem/implementations.py
Filesystem (JSON) storage stubs — future implementation.
Shows how the repository pattern makes swapping backends trivial.
"""
import json
import os
from typing import Optional, List
from repositories.interfaces import (
    PatientRepository, DoctorRepository, AppointmentRepository,
    TimeSlotRepository, MedicalRecordRepository
)


class FileSystemRepository:
    """
    Base filesystem repository. Serialises/deserialises entities to JSON.
    Stub — methods are scaffolded but not fully implemented.
    """

    def __init__(self, file_path: str):
        self._file_path = file_path
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        if not os.path.exists(file_path):
            with open(file_path, "w") as f:
                json.dump({}, f)

    def _load(self) -> dict:
        with open(self._file_path, "r") as f:
            return json.load(f)

    def _save_all(self, data: dict) -> None:
        with open(self._file_path, "w") as f:
            json.dump(data, f, indent=2, default=str)

    def save(self, entity) -> None:
        # TODO: implement entity serialisation to dict
        raise NotImplementedError("FileSystem save() not yet implemented.")

    def find_by_id(self, entity_id: str) -> Optional[object]:
        raise NotImplementedError("FileSystem find_by_id() not yet implemented.")

    def find_all(self) -> List:
        raise NotImplementedError("FileSystem find_all() not yet implemented.")

    def delete(self, entity_id: str) -> None:
        data = self._load()
        if entity_id in data:
            del data[entity_id]
            self._save_all(data)

    def exists(self, entity_id: str) -> bool:
        return entity_id in self._load()

    def count(self) -> int:
        return len(self._load())


class FileSystemPatientRepository(FileSystemRepository, PatientRepository):
    """Filesystem stub for PatientRepository."""

    def find_by_email(self, email: str): raise NotImplementedError
    def find_by_caregiver_id(self, caregiver_id: str): raise NotImplementedError


class FileSystemDoctorRepository(FileSystemRepository, DoctorRepository):
    """Filesystem stub for DoctorRepository."""

    def find_by_specialisation(self, specialisation: str): raise NotImplementedError
    def find_available(self): raise NotImplementedError


class FileSystemAppointmentRepository(FileSystemRepository, AppointmentRepository):
    """Filesystem stub for AppointmentRepository."""

    def find_by_patient_id(self, patient_id: str): raise NotImplementedError
    def find_by_doctor_id(self, doctor_id: str): raise NotImplementedError
    def find_by_status(self, status: str): raise NotImplementedError
    def find_by_slot_id(self, slot_id: str): raise NotImplementedError


class FileSystemTimeSlotRepository(FileSystemRepository, TimeSlotRepository):
    """Filesystem stub for TimeSlotRepository."""

    def find_by_doctor_id(self, doctor_id: str): raise NotImplementedError
    def find_available_by_doctor(self, doctor_id: str): raise NotImplementedError


class FileSystemMedicalRecordRepository(FileSystemRepository, MedicalRecordRepository):
    """Filesystem stub for MedicalRecordRepository."""

    def find_by_patient_id(self, patient_id: str): raise NotImplementedError
    def find_by_doctor_id(self, doctor_id: str): raise NotImplementedError