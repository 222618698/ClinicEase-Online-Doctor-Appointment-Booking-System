"""
src/users.py - Patient, Doctor, Receptionist, Administrator subclasses
"""
from datetime import datetime
from typing import List, Optional
from src.user import User, UserRole


class Patient(User):
    def __init__(self, user_id: str, name: str, email: str,
                 date_of_birth: str = "", phone: str = "", address: str = ""):
        super().__init__(user_id, name, email, UserRole.PATIENT)
        self._date_of_birth = date_of_birth
        self._phone = phone
        self._address = address
        self._medical_aid_number: Optional[str] = None
        self._caregiver_id: Optional[str] = None
        self._appointments: List[str] = []       # appointment IDs
        self._medical_records: List[str] = []    # record IDs
        self._medication_reminders: List[str] = []

    @property
    def phone(self): return self._phone

    @property
    def caregiver_id(self): return self._caregiver_id

    @property
    def appointments(self): return list(self._appointments)

    def link_caregiver(self, caregiver_id: str):
        self._caregiver_id = caregiver_id

    def add_appointment(self, appointment_id: str):
        self._appointments.append(appointment_id)

    def remove_appointment(self, appointment_id: str):
        if appointment_id in self._appointments:
            self._appointments.remove(appointment_id)

    def add_medication_reminder(self, reminder_id: str):
        self._medication_reminders.append(reminder_id)

    def view_medical_records(self) -> List[str]:
        return list(self._medical_records)

    def request_data_deletion(self) -> str:
        return f"Data deletion request submitted for patient {self._user_id}"

    def __repr__(self):
        return f"<Patient id={self._user_id} name={self._name}>"


class Doctor(User):
    def __init__(self, user_id: str, name: str, email: str,
                 specialisation: str = "", qualifications: str = "", clinic_id: str = ""):
        super().__init__(user_id, name, email, UserRole.DOCTOR)
        self._specialisation = specialisation
        self._qualifications = qualifications
        self._bio = ""
        self._profile_status = "draft"
        self._clinic_id = clinic_id
        self._time_slots: List[str] = []      # slot IDs
        self._appointments: List[str] = []

    @property
    def specialisation(self): return self._specialisation

    @property
    def qualifications(self): return self._qualifications

    @property
    def profile_status(self): return self._profile_status

    @property
    def time_slots(self): return list(self._time_slots)

    def publish_profile(self):
        self._profile_status = "active"

    def set_unavailable(self):
        self._profile_status = "unavailable"

    def set_available(self):
        self._profile_status = "active"

    def add_time_slot(self, slot_id: str):
        self._time_slots.append(slot_id)

    def block_slot(self, slot_id: str) -> str:
        return f"Slot {slot_id} blocked by doctor {self._user_id}"

    def view_daily_schedule(self, date: datetime) -> List[str]:
        return [a for a in self._appointments]  # simplified

    def update_consultation_notes(self, appointment_id: str, notes: str) -> str:
        return f"Notes updated for appointment {appointment_id}"

    def __repr__(self):
        return f"<Doctor id={self._user_id} name={self._name} specialisation={self._specialisation}>"


class Receptionist(User):
    def __init__(self, user_id: str, name: str, email: str, clinic_id: str = ""):
        super().__init__(user_id, name, email, UserRole.RECEPTIONIST)
        self._clinic_id = clinic_id

    def create_appointment_for_patient(self, patient_id: str, slot_id: str) -> str:
        return f"Appointment created for patient {patient_id} at slot {slot_id}"

    def add_walk_in_patient(self, patient_id: str) -> str:
        return f"Walk-in patient {patient_id} added to queue"

    def search_patient(self, query: str) -> str:
        return f"Search results for: {query}"

    def __repr__(self):
        return f"<Receptionist id={self._user_id} name={self._name}>"


class Administrator(User):
    def __init__(self, user_id: str, name: str, email: str, clinic_id: str = ""):
        super().__init__(user_id, name, email, UserRole.ADMIN)
        self._clinic_id = clinic_id
        self._audit_logs: List[dict] = []

    def deactivate_user(self, user: User):
        user.deactivate()
        self._log_action("deactivate", user.user_id)

    def activate_user(self, user: User):
        user.activate()
        self._log_action("activate", user.user_id)

    def generate_report(self, report_type: str, date_range: dict) -> dict:
        return {
            "type": report_type,
            "date_range": date_range,
            "generated_at": datetime.now().isoformat(),
            "generated_by": self._user_id
        }

    def view_audit_logs(self) -> List[dict]:
        return list(self._audit_logs)

    def _log_action(self, action: str, target_user_id: str):
        self._audit_logs.append({
            "action": action,
            "target_user_id": target_user_id,
            "timestamp": datetime.now().isoformat(),
            "admin_id": self._user_id
        })

    def __repr__(self):
        return f"<Administrator id={self._user_id} name={self._name}>"