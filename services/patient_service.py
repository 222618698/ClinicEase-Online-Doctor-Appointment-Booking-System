"""
services/patient_service.py
Business logic for Patient operations.
Uses PatientRepository for persistence and enforces domain rules.
"""
from typing import Optional, List
from src.users import Patient
from repositories.interfaces import PatientRepository


class PatientNotFoundError(Exception):
    pass

class EmailAlreadyRegisteredError(Exception):
    pass

class InvalidPatientDataError(Exception):
    pass


class PatientService:
    """
    Service layer for Patient business operations.
    Injects PatientRepository — works with ANY backend (memory/DB/filesystem).
    """

    def __init__(self, patient_repo: PatientRepository):
        self._repo = patient_repo
        self._id_counter = 1

    def _generate_id(self) -> str:
        pid = f"P{self._id_counter:03d}"
        self._id_counter += 1
        return pid

    def register_patient(self, name: str, email: str,
                         phone: str = "", address: str = "",
                         date_of_birth: str = "") -> Patient:
        """
        Register a new patient.
        Business rules:
        - Name and email are required
        - Email must be unique across all patients
        - Name must be at least 2 characters
        """
        if not name or len(name.strip()) < 2:
            raise InvalidPatientDataError("Name must be at least 2 characters.")
        if not email or "@" not in email:
            raise InvalidPatientDataError("A valid email address is required.")

        existing = self._repo.find_by_email(email)
        if existing:
            raise EmailAlreadyRegisteredError(
                f"A patient with email '{email}' is already registered."
            )

        patient_id = self._generate_id()
        patient = Patient(patient_id, name.strip(), email.strip(),
                          date_of_birth=date_of_birth,
                          phone=phone, address=address)
        self._repo.save(patient)
        return patient

    def get_patient(self, patient_id: str) -> Patient:
        """Retrieve a patient by ID. Raises PatientNotFoundError if missing."""
        patient = self._repo.find_by_id(patient_id)
        if not patient:
            raise PatientNotFoundError(f"Patient '{patient_id}' not found.")
        return patient

    def get_all_patients(self) -> List[Patient]:
        """Return all registered patients."""
        return self._repo.find_all()

    def update_patient(self, patient_id: str, name: str = None,
                       phone: str = None, address: str = None) -> Patient:
        """Update a patient's profile details."""
        patient = self.get_patient(patient_id)
        if name:
            if len(name.strip()) < 2:
                raise InvalidPatientDataError("Name must be at least 2 characters.")
            patient.update_profile(name=name.strip())
        if phone:
            patient._phone = phone
        if address:
            patient._address = address
        self._repo.save(patient)
        return patient

    def delete_patient(self, patient_id: str) -> None:
        """Delete a patient record. Raises PatientNotFoundError if missing."""
        self.get_patient(patient_id)  # Validates existence
        self._repo.delete(patient_id)

    def find_by_email(self, email: str) -> Optional[Patient]:
        """Find a patient by email address."""
        return self._repo.find_by_email(email)

    def get_patient_count(self) -> int:
        """Return total number of registered patients."""
        return self._repo.count()