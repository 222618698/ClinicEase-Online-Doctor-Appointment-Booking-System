"""
tests/test_services.py
Unit tests for PatientService, DoctorService, and AppointmentService.
"""
import pytest
from datetime import datetime, timedelta

from src.users import Patient, Doctor
from src.models import AppointmentStatus, SlotStatus
from repositories.inmemory.implementations import (
    InMemoryPatientRepository, InMemoryDoctorRepository,
    InMemoryAppointmentRepository, InMemoryTimeSlotRepository
)
from services.patient_service import (
    PatientService, PatientNotFoundError,
    EmailAlreadyRegisteredError, InvalidPatientDataError
)
from services.doctor_service import (
    DoctorService, DoctorNotFoundError, InvalidDoctorDataError
)
from services.appointment_service import (
    AppointmentService, AppointmentNotFoundError,
    SlotNotAvailableError, SlotNotFoundError,
    InvalidAppointmentError
)


@pytest.fixture
def patient_service():
    return PatientService(InMemoryPatientRepository())

@pytest.fixture
def doctor_service():
    return DoctorService(InMemoryDoctorRepository())


def make_appt_service():
    patient_repo = InMemoryPatientRepository()
    doctor_repo = InMemoryDoctorRepository()
    appt_repo = InMemoryAppointmentRepository()
    slot_repo = InMemoryTimeSlotRepository()
    appt_svc = AppointmentService(appt_repo, slot_repo, patient_repo, doctor_repo)
    pat_svc = PatientService(patient_repo)
    doc_svc = DoctorService(doctor_repo)
    return pat_svc, doc_svc, appt_svc


class TestPatientService:

    def test_register_patient_success(self, patient_service):
        p = patient_service.register_patient("Sipho Dlamini", "sipho@email.com")
        assert p.name == "Sipho Dlamini"
        assert p.email == "sipho@email.com"
        assert p._user_id.startswith("P")

    def test_register_assigns_unique_ids(self, patient_service):
        p1 = patient_service.register_patient("Alice", "alice@email.com")
        p2 = patient_service.register_patient("Bob", "bob@email.com")
        assert p1._user_id != p2._user_id

    def test_register_duplicate_email_raises(self, patient_service):
        patient_service.register_patient("Alice", "alice@email.com")
        with pytest.raises(EmailAlreadyRegisteredError):
            patient_service.register_patient("Alice2", "alice@email.com")

    def test_register_invalid_name_raises(self, patient_service):
        with pytest.raises(InvalidPatientDataError, match="Name"):
            patient_service.register_patient("A", "valid@email.com")

    def test_register_invalid_email_raises(self, patient_service):
        with pytest.raises(InvalidPatientDataError, match="email"):
            patient_service.register_patient("Valid Name", "notanemail")

    def test_register_empty_name_raises(self, patient_service):
        with pytest.raises(InvalidPatientDataError):
            patient_service.register_patient("", "valid@email.com")

    def test_get_patient_success(self, patient_service):
        p = patient_service.register_patient("Thabo", "thabo@email.com")
        result = patient_service.get_patient(p._user_id)
        assert result is p

    def test_get_patient_not_found_raises(self, patient_service):
        with pytest.raises(PatientNotFoundError):
            patient_service.get_patient("GHOST")

    def test_get_all_patients(self, patient_service):
        patient_service.register_patient("Alice", "alice@email.com")
        patient_service.register_patient("Bob", "bob@email.com")
        assert len(patient_service.get_all_patients()) == 2

    def test_update_patient_name(self, patient_service):
        p = patient_service.register_patient("Old Name", "old@email.com")
        updated = patient_service.update_patient(p._user_id, name="New Name")
        assert updated.name == "New Name"

    def test_update_patient_not_found_raises(self, patient_service):
        with pytest.raises(PatientNotFoundError):
            patient_service.update_patient("GHOST", name="Name")

    def test_delete_patient(self, patient_service):
        p = patient_service.register_patient("Delete Me", "delete@email.com")
        patient_service.delete_patient(p._user_id)
        assert patient_service.get_patient_count() == 0

    def test_delete_patient_not_found_raises(self, patient_service):
        with pytest.raises(PatientNotFoundError):
            patient_service.delete_patient("GHOST")

    def test_find_by_email(self, patient_service):
        patient_service.register_patient("Fatima", "fatima@email.com")
        result = patient_service.find_by_email("fatima@email.com")
        assert result is not None
        assert result.name == "Fatima"

    def test_patient_count(self, patient_service):
        patient_service.register_patient("Alpha", "a@email.com")
        patient_service.register_patient("Beta", "b@email.com")
        assert patient_service.get_patient_count() == 2


class TestDoctorService:

    def test_create_doctor_success(self, doctor_service):
        d = doctor_service.create_doctor("Dr Khumalo", "khumalo@clinic.com", "Cardiology")
        assert d.name == "Dr Khumalo"
        assert d.specialisation == "Cardiology"
        assert d.profile_status == "active"

    def test_create_doctor_invalid_name_raises(self, doctor_service):
        with pytest.raises(InvalidDoctorDataError, match="name"):
            doctor_service.create_doctor("D", "d@clinic.com", "GP")

    def test_create_doctor_missing_specialisation_raises(self, doctor_service):
        with pytest.raises(InvalidDoctorDataError, match="Specialisation"):
            doctor_service.create_doctor("Dr Valid", "v@clinic.com", "")

    def test_create_doctor_invalid_email_raises(self, doctor_service):
        with pytest.raises(InvalidDoctorDataError, match="email"):
            doctor_service.create_doctor("Dr Valid", "notanemail", "GP")

    def test_get_doctor_success(self, doctor_service):
        d = doctor_service.create_doctor("Dr Smith", "smith@clinic.com", "GP")
        result = doctor_service.get_doctor(d._user_id)
        assert result is d

    def test_get_doctor_not_found_raises(self, doctor_service):
        with pytest.raises(DoctorNotFoundError):
            doctor_service.get_doctor("GHOST")

    def test_get_all_doctors(self, doctor_service):
        doctor_service.create_doctor("Dr A", "a@clinic.com", "GP")
        doctor_service.create_doctor("Dr B", "b@clinic.com", "Cardiology")
        assert len(doctor_service.get_all_doctors()) == 2

    def test_get_available_doctors(self, doctor_service):
        d1 = doctor_service.create_doctor("Dr A", "a@clinic.com", "GP")
        d2 = doctor_service.create_doctor("Dr B", "b@clinic.com", "Cardiology")
        doctor_service.set_unavailable(d2._user_id)
        available = doctor_service.get_available_doctors()
        assert len(available) == 1
        assert available[0] is d1

    def test_search_by_specialisation(self, doctor_service):
        doctor_service.create_doctor("Dr A", "a@clinic.com", "Cardiology")
        doctor_service.create_doctor("Dr B", "b@clinic.com", "GP")
        results = doctor_service.search_by_specialisation("Cardiology")
        assert len(results) == 1

    def test_search_empty_term_raises(self, doctor_service):
        with pytest.raises(InvalidDoctorDataError):
            doctor_service.search_by_specialisation("")

    def test_set_unavailable(self, doctor_service):
        d = doctor_service.create_doctor("Dr C", "c@clinic.com", "GP")
        doctor_service.set_unavailable(d._user_id)
        assert doctor_service.get_doctor(d._user_id).profile_status == "unavailable"

    def test_set_available_after_unavailable(self, doctor_service):
        d = doctor_service.create_doctor("Dr D", "d@clinic.com", "GP")
        doctor_service.set_unavailable(d._user_id)
        doctor_service.set_available(d._user_id)
        assert doctor_service.get_doctor(d._user_id).profile_status == "active"

    def test_update_doctor(self, doctor_service):
        d = doctor_service.create_doctor("Dr Old", "old@clinic.com", "GP")
        updated = doctor_service.update_doctor(d._user_id, specialisation="Cardiology")
        assert updated.specialisation == "Cardiology"

    def test_delete_doctor(self, doctor_service):
        d = doctor_service.create_doctor("Dr Delete", "del@clinic.com", "GP")
        doctor_service.delete_doctor(d._user_id)
        assert doctor_service.get_doctor_count() == 0


class TestAppointmentService:

    def test_book_appointment_success(self):
        pat_svc, doc_svc, appt_svc = make_appt_service()
        patient = pat_svc.register_patient("Sipho", "sipho@email.com")
        doctor = doc_svc.create_doctor("Dr K", "k@clinic.com", "GP")
        slot = appt_svc.create_slot(doctor._user_id, datetime.now() + timedelta(hours=1))
        appt = appt_svc.book_appointment(patient._user_id, doctor._user_id, slot.slot_id)
        assert appt.status == AppointmentStatus.CONFIRMED
        assert appt.patient_id == patient._user_id

    def test_book_appointment_slot_becomes_booked(self):
        pat_svc, doc_svc, appt_svc = make_appt_service()
        patient = pat_svc.register_patient("PatA", "a@email.com")
        doctor = doc_svc.create_doctor("Dr Bosman", "b@clinic.com", "GP")
        slot = appt_svc.create_slot(doctor._user_id, datetime.now() + timedelta(hours=1))
        appt_svc.book_appointment(patient._user_id, doctor._user_id, slot.slot_id)
        updated_slot = appt_svc._slot_repo.find_by_id(slot.slot_id)
        assert updated_slot.status == SlotStatus.BOOKED

    def test_book_appointment_double_booking_raises(self):
        pat_svc, doc_svc, appt_svc = make_appt_service()
        p1 = pat_svc.register_patient("PatOne", "p1@email.com")
        p2 = pat_svc.register_patient("PatTwo", "p2@email.com")
        doctor = doc_svc.create_doctor("Dr Xavier", "x@clinic.com", "GP")
        slot = appt_svc.create_slot(doctor._user_id, datetime.now() + timedelta(hours=1))
        appt_svc.book_appointment(p1._user_id, doctor._user_id, slot.slot_id)
        with pytest.raises(SlotNotAvailableError):
            appt_svc.book_appointment(p2._user_id, doctor._user_id, slot.slot_id)

    def test_book_appointment_patient_not_found_raises(self):
        _, doc_svc, appt_svc = make_appt_service()
        doctor = doc_svc.create_doctor("Dr Yusuf", "y@clinic.com", "GP")
        slot = appt_svc.create_slot(doctor._user_id, datetime.now() + timedelta(hours=1))
        with pytest.raises(Exception):
            appt_svc.book_appointment("GHOST_P", doctor._user_id, slot.slot_id)

    def test_book_appointment_unavailable_doctor_raises(self):
        pat_svc, doc_svc, appt_svc = make_appt_service()
        patient = pat_svc.register_patient("PatC", "c@email.com")
        doctor = doc_svc.create_doctor("Dr Zola", "z@clinic.com", "GP")
        slot = appt_svc.create_slot(doctor._user_id, datetime.now() + timedelta(hours=1))
        doc_svc.set_unavailable(doctor._user_id)
        with pytest.raises(InvalidAppointmentError):
            appt_svc.book_appointment(patient._user_id, doctor._user_id, slot.slot_id)

    def test_cancel_appointment_releases_slot(self):
        pat_svc, doc_svc, appt_svc = make_appt_service()
        patient = pat_svc.register_patient("PatD", "d@email.com")
        doctor = doc_svc.create_doctor("Dr Adams", "a@clinic.com", "GP")
        slot = appt_svc.create_slot(doctor._user_id, datetime.now() + timedelta(hours=1))
        appt = appt_svc.book_appointment(patient._user_id, doctor._user_id, slot.slot_id)
        appt_svc.cancel_appointment(appt.appointment_id)
        updated_slot = appt_svc._slot_repo.find_by_id(slot.slot_id)
        assert updated_slot.status == SlotStatus.AVAILABLE

    def test_cancel_completed_appointment_raises(self):
        pat_svc, doc_svc, appt_svc = make_appt_service()
        patient = pat_svc.register_patient("PatE", "e@email.com")
        doctor = doc_svc.create_doctor("Dr Bosman", "b@clinic.com", "GP")
        slot = appt_svc.create_slot(doctor._user_id, datetime.now() + timedelta(hours=1))
        appt = appt_svc.book_appointment(patient._user_id, doctor._user_id, slot.slot_id)
        appt_svc.complete_appointment(appt.appointment_id, "All good.")
        with pytest.raises(InvalidAppointmentError):
            appt_svc.cancel_appointment(appt.appointment_id)

    def test_reschedule_appointment_success(self):
        pat_svc, doc_svc, appt_svc = make_appt_service()
        patient = pat_svc.register_patient("PatF", "f@email.com")
        doctor = doc_svc.create_doctor("Dr Carter", "c@clinic.com", "GP")
        slot1 = appt_svc.create_slot(doctor._user_id, datetime.now() + timedelta(hours=1))
        slot2 = appt_svc.create_slot(doctor._user_id, datetime.now() + timedelta(hours=2))
        appt = appt_svc.book_appointment(patient._user_id, doctor._user_id, slot1.slot_id)
        rescheduled = appt_svc.reschedule_appointment(appt.appointment_id, slot2.slot_id)
        assert rescheduled.slot_id == slot2.slot_id
        released = appt_svc._slot_repo.find_by_id(slot1.slot_id)
        assert released.status == SlotStatus.AVAILABLE

    def test_complete_appointment(self):
        pat_svc, doc_svc, appt_svc = make_appt_service()
        patient = pat_svc.register_patient("PatG", "g@email.com")
        doctor = doc_svc.create_doctor("Dr Dlamini", "d@clinic.com", "GP")
        slot = appt_svc.create_slot(doctor._user_id, datetime.now() + timedelta(hours=1))
        appt = appt_svc.book_appointment(patient._user_id, doctor._user_id, slot.slot_id)
        completed = appt_svc.complete_appointment(appt.appointment_id, "Patient reviewed.")
        assert completed.status == AppointmentStatus.COMPLETED
        assert completed.notes == "Patient reviewed."

    def test_get_available_slots(self):
        pat_svc, doc_svc, appt_svc = make_appt_service()
        patient = pat_svc.register_patient("PatH", "h@email.com")
        doctor = doc_svc.create_doctor("Dr Evans", "e@clinic.com", "GP")
        slot1 = appt_svc.create_slot(doctor._user_id, datetime.now() + timedelta(hours=1))
        slot2 = appt_svc.create_slot(doctor._user_id, datetime.now() + timedelta(hours=2))
        appt_svc.book_appointment(patient._user_id, doctor._user_id, slot1.slot_id)
        available = appt_svc.get_available_slots(doctor._user_id)
        assert len(available) == 1
        assert available[0].slot_id == slot2.slot_id

    def test_appointment_not_found_raises(self):
        _, _, appt_svc = make_appt_service()
        with pytest.raises(AppointmentNotFoundError):
            appt_svc.get_appointment("GHOST")