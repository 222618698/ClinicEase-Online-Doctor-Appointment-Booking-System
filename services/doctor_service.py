"""
services/doctor_service.py
Business logic for Doctor operations.
"""
from typing import List, Optional
from src.users import Doctor
from repositories.interfaces import DoctorRepository


class DoctorNotFoundError(Exception):
    pass

class InvalidDoctorDataError(Exception):
    pass


class DoctorService:
    """
    Service layer for Doctor business operations.
    Business rules:
    - A doctor must have a specialisation to be published
    - Only active doctors appear in search results
    - A doctor cannot be deleted if they have active appointments
    """

    def __init__(self, doctor_repo: DoctorRepository):
        self._repo = doctor_repo
        self._id_counter = 1

    def _generate_id(self) -> str:
        did = f"D{self._id_counter:03d}"
        self._id_counter += 1
        return did

    def create_doctor(self, name: str, email: str,
                      specialisation: str, qualifications: str = "",
                      clinic_id: str = "") -> Doctor:
        """
        Create and publish a doctor profile.
        Business rules:
        - Name, email, and specialisation are required
        - Doctor profile starts as Draft then is published immediately
        """
        if not name or len(name.strip()) < 2:
            raise InvalidDoctorDataError("Doctor name must be at least 2 characters.")
        if not email or "@" not in email:
            raise InvalidDoctorDataError("A valid email address is required.")
        if not specialisation or len(specialisation.strip()) < 2:
            raise InvalidDoctorDataError("Specialisation is required.")

        doctor_id = self._generate_id()
        doctor = Doctor(doctor_id, name.strip(), email.strip(),
                        specialisation=specialisation.strip(),
                        qualifications=qualifications,
                        clinic_id=clinic_id)
        doctor.publish_profile()
        self._repo.save(doctor)
        return doctor

    def get_doctor(self, doctor_id: str) -> Doctor:
        """Retrieve a doctor by ID."""
        doctor = self._repo.find_by_id(doctor_id)
        if not doctor:
            raise DoctorNotFoundError(f"Doctor '{doctor_id}' not found.")
        return doctor

    def get_all_doctors(self) -> List[Doctor]:
        """Return all doctor profiles."""
        return self._repo.find_all()

    def get_available_doctors(self) -> List[Doctor]:
        """Return only active (available) doctors."""
        return self._repo.find_available()

    def search_by_specialisation(self, specialisation: str) -> List[Doctor]:
        """Search doctors by specialisation."""
        if not specialisation:
            raise InvalidDoctorDataError("Specialisation search term cannot be empty.")
        return self._repo.find_by_specialisation(specialisation)

    def update_doctor(self, doctor_id: str, name: str = None,
                      specialisation: str = None,
                      qualifications: str = None) -> Doctor:
        """Update doctor profile details."""
        doctor = self.get_doctor(doctor_id)
        if name:
            doctor.update_profile(name=name.strip())
        if specialisation:
            doctor._specialisation = specialisation.strip()
        if qualifications:
            doctor._qualifications = qualifications
        self._repo.save(doctor)
        return doctor

    def set_unavailable(self, doctor_id: str) -> Doctor:
        """Mark a doctor as unavailable (e.g. on leave)."""
        doctor = self.get_doctor(doctor_id)
        doctor.set_unavailable()
        self._repo.save(doctor)
        return doctor

    def set_available(self, doctor_id: str) -> Doctor:
        """Mark a doctor as available again."""
        doctor = self.get_doctor(doctor_id)
        doctor.set_available()
        self._repo.save(doctor)
        return doctor

    def delete_doctor(self, doctor_id: str) -> None:
        """Remove a doctor profile."""
        self.get_doctor(doctor_id)
        self._repo.delete(doctor_id)

    def get_doctor_count(self) -> int:
        return self._repo.count()