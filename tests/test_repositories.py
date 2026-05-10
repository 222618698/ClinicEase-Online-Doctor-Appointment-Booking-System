"""
tests/test_repositories.py
Unit tests for all in-memory repository implementations and the RepositoryFactory.
Run with: pytest tests/test_repositories.py -v
"""
import pytest
from datetime import datetime, timedelta

from src.users import Patient, Doctor
from src.models import (
    Appointment, AppointmentStatus,
    TimeSlot, SlotStatus,
    MedicalRecord,
    MedicationReminder, ReminderStatus,
    Notification, NotificationType, NotificationStatus
)
from repositories.inmemory.implementations import (
    InMemoryPatientRepository,
    InMemoryDoctorRepository,
    InMemoryAppointmentRepository,
    InMemoryTimeSlotRepository,
    InMemoryMedicalRecordRepository,
    InMemoryMedicationReminderRepository,
    InMemoryNotificationRepository,
)
from factories.repository_factory import RepositoryFactory


# ── Helpers ──────────────────────────────────────────────────

def make_patient(pid="P001", email="patient@test.com"):
    p = Patient(pid, "Test Patient", email)
    return p

def make_doctor(did="D001", specialisation="General"):
    d = Doctor(did, "Dr Test", "doc@test.com", specialisation=specialisation)
    d.publish_profile()
    return d

def make_appointment(aid="A001", pid="P001", did="D001", sid="S001"):
    return Appointment(aid, pid, did, sid)

def make_slot(sid="S001", did="D001"):
    start = datetime.now()
    end = start + timedelta(minutes=30)
    return TimeSlot(sid, did, start, end)

def make_record(rid="R001", pid="P001", did="D001", aid="A001"):
    return MedicalRecord(rid, pid, did, aid)

def make_reminder(mid="M001", pid="P001"):
    return MedicationReminder(mid, pid, "Aspirin", "100mg", 1, 30)

def make_notification(nid="N001", rid="P001"):
    return Notification(nid, rid, NotificationType.APPOINTMENT_CONFIRMATION, "Test msg")


# ══════════════════════════════════════════════════════════════
# PATIENT REPOSITORY TESTS
# ══════════════════════════════════════════════════════════════

class TestInMemoryPatientRepository:

    def setup_method(self):
        self.repo = InMemoryPatientRepository()

    def test_save_and_find_by_id(self):
        p = make_patient("P001")
        self.repo.save(p)
        result = self.repo.find_by_id("P001")
        assert result is p

    def test_find_by_id_returns_none_if_missing(self):
        assert self.repo.find_by_id("MISSING") is None

    def test_find_all_returns_all_patients(self):
        self.repo.save(make_patient("P001", "a@test.com"))
        self.repo.save(make_patient("P002", "b@test.com"))
        assert len(self.repo.find_all()) == 2

    def test_delete_removes_patient(self):
        p = make_patient("P001")
        self.repo.save(p)
        self.repo.delete("P001")
        assert self.repo.find_by_id("P001") is None

    def test_delete_nonexistent_raises(self):
        with pytest.raises(KeyError):
            self.repo.delete("GHOST")

    def test_exists_true(self):
        self.repo.save(make_patient("P001"))
        assert self.repo.exists("P001") is True

    def test_exists_false(self):
        assert self.repo.exists("NONE") is False

    def test_count(self):
        self.repo.save(make_patient("P001", "a@test.com"))
        self.repo.save(make_patient("P002", "b@test.com"))
        assert self.repo.count() == 2

    def test_save_overwrites_existing(self):
        p1 = make_patient("P001", "old@test.com")
        self.repo.save(p1)
        p2 = make_patient("P001", "new@test.com")
        self.repo.save(p2)
        assert self.repo.count() == 1
        assert self.repo.find_by_id("P001").email == "new@test.com"

    def test_find_by_email(self):
        p = make_patient("P001", "find@test.com")
        self.repo.save(p)
        result = self.repo.find_by_email("find@test.com")
        assert result is p

    def test_find_by_email_case_insensitive(self):
        p = make_patient("P001", "Case@Test.com")
        self.repo.save(p)
        result = self.repo.find_by_email("case@test.com")
        assert result is p

    def test_find_by_email_not_found_returns_none(self):
        assert self.repo.find_by_email("ghost@test.com") is None

    def test_find_by_caregiver_id(self):
        p = make_patient("P001")
        p.link_caregiver("CG001")
        self.repo.save(p)
        results = self.repo.find_by_caregiver_id("CG001")
        assert len(results) == 1
        assert results[0] is p


# ══════════════════════════════════════════════════════════════
# DOCTOR REPOSITORY TESTS
# ══════════════════════════════════════════════════════════════

class TestInMemoryDoctorRepository:

    def setup_method(self):
        self.repo = InMemoryDoctorRepository()

    def test_save_and_find_by_id(self):
        d = make_doctor("D001")
        self.repo.save(d)
        assert self.repo.find_by_id("D001") is d

    def test_find_by_specialisation(self):
        self.repo.save(make_doctor("D001", "Cardiology"))
        self.repo.save(make_doctor("D002", "General"))
        results = self.repo.find_by_specialisation("Cardiology")
        assert len(results) == 1
        assert results[0].specialisation == "Cardiology"

    def test_find_by_specialisation_case_insensitive(self):
        self.repo.save(make_doctor("D001", "Cardiology"))
        results = self.repo.find_by_specialisation("cardiology")
        assert len(results) == 1

    def test_find_available_returns_active_doctors(self):
        active = make_doctor("D001")
        unavailable = make_doctor("D002")
        unavailable.set_unavailable()
        self.repo.save(active)
        self.repo.save(unavailable)
        results = self.repo.find_available()
        assert len(results) == 1
        assert results[0] is active

    def test_delete_doctor(self):
        self.repo.save(make_doctor("D001"))
        self.repo.delete("D001")
        assert self.repo.find_by_id("D001") is None


# ══════════════════════════════════════════════════════════════
# APPOINTMENT REPOSITORY TESTS
# ══════════════════════════════════════════════════════════════

class TestInMemoryAppointmentRepository:

    def setup_method(self):
        self.repo = InMemoryAppointmentRepository()

    def test_save_and_find_by_id(self):
        a = make_appointment("A001")
        self.repo.save(a)
        assert self.repo.find_by_id("A001") is a

    def test_find_by_patient_id(self):
        self.repo.save(make_appointment("A001", pid="P001"))
        self.repo.save(make_appointment("A002", pid="P002"))
        results = self.repo.find_by_patient_id("P001")
        assert len(results) == 1

    def test_find_by_doctor_id(self):
        self.repo.save(make_appointment("A001", did="D001"))
        self.repo.save(make_appointment("A002", did="D002"))
        results = self.repo.find_by_doctor_id("D001")
        assert len(results) == 1

    def test_find_by_status_confirmed(self):
        a = make_appointment("A001")
        a.confirm()
        self.repo.save(a)
        results = self.repo.find_by_status("confirmed")
        assert len(results) == 1

    def test_find_by_slot_id(self):
        a = make_appointment("A001", sid="S999")
        self.repo.save(a)
        result = self.repo.find_by_slot_id("S999")
        assert result is a

    def test_find_by_slot_id_not_found(self):
        assert self.repo.find_by_slot_id("NOSLOT") is None

    def test_count_appointments(self):
        self.repo.save(make_appointment("A001"))
        self.repo.save(make_appointment("A002"))
        assert self.repo.count() == 2


# ══════════════════════════════════════════════════════════════
# TIME SLOT REPOSITORY TESTS
# ══════════════════════════════════════════════════════════════

class TestInMemoryTimeSlotRepository:

    def setup_method(self):
        self.repo = InMemoryTimeSlotRepository()

    def test_save_and_find_by_id(self):
        s = make_slot("S001")
        self.repo.save(s)
        assert self.repo.find_by_id("S001") is s

    def test_find_by_doctor_id(self):
        self.repo.save(make_slot("S001", "D001"))
        self.repo.save(make_slot("S002", "D002"))
        results = self.repo.find_by_doctor_id("D001")
        assert len(results) == 1

    def test_find_available_by_doctor(self):
        available = make_slot("S001", "D001")
        booked = make_slot("S002", "D001")
        booked.mark_reserved()
        booked.mark_booked()
        self.repo.save(available)
        self.repo.save(booked)
        results = self.repo.find_available_by_doctor("D001")
        assert len(results) == 1
        assert results[0] is available

    def test_delete_slot(self):
        self.repo.save(make_slot("S001"))
        self.repo.delete("S001")
        assert self.repo.exists("S001") is False


# ══════════════════════════════════════════════════════════════
# MEDICAL RECORD REPOSITORY TESTS
# ══════════════════════════════════════════════════════════════

class TestInMemoryMedicalRecordRepository:

    def setup_method(self):
        self.repo = InMemoryMedicalRecordRepository()

    def test_save_and_find_by_id(self):
        r = make_record("R001")
        self.repo.save(r)
        assert self.repo.find_by_id("R001") is r

    def test_find_by_patient_id(self):
        self.repo.save(make_record("R001", pid="P001"))
        self.repo.save(make_record("R002", pid="P002"))
        results = self.repo.find_by_patient_id("P001")
        assert len(results) == 1

    def test_find_all(self):
        self.repo.save(make_record("R001"))
        self.repo.save(make_record("R002"))
        assert len(self.repo.find_all()) == 2


# ══════════════════════════════════════════════════════════════
# MEDICATION REMINDER REPOSITORY TESTS
# ══════════════════════════════════════════════════════════════

class TestInMemoryMedicationReminderRepository:

    def setup_method(self):
        self.repo = InMemoryMedicationReminderRepository()

    def test_save_and_find_by_id(self):
        m = make_reminder("M001")
        self.repo.save(m)
        assert self.repo.find_by_id("M001") is m

    def test_find_by_patient_id(self):
        self.repo.save(make_reminder("M001", "P001"))
        self.repo.save(make_reminder("M002", "P002"))
        results = self.repo.find_by_patient_id("P001")
        assert len(results) == 1

    def test_find_active(self):
        active = make_reminder("M001", "P001")
        cancelled = make_reminder("M002", "P002")
        cancelled.cancel()
        self.repo.save(active)
        self.repo.save(cancelled)
        results = self.repo.find_active()
        assert len(results) == 1
        assert results[0] is active


# ══════════════════════════════════════════════════════════════
# NOTIFICATION REPOSITORY TESTS
# ══════════════════════════════════════════════════════════════

class TestInMemoryNotificationRepository:

    def setup_method(self):
        self.repo = InMemoryNotificationRepository()

    def test_save_and_find_by_id(self):
        n = make_notification("N001")
        self.repo.save(n)
        assert self.repo.find_by_id("N001") is n

    def test_find_by_recipient_id(self):
        self.repo.save(make_notification("N001", "P001"))
        self.repo.save(make_notification("N002", "P002"))
        results = self.repo.find_by_recipient_id("P001")
        assert len(results) == 1

    def test_find_by_status_queued(self):
        n = make_notification("N001")
        self.repo.save(n)
        results = self.repo.find_by_status("queued")
        assert len(results) == 1

    def test_find_by_status_delivered(self):
        n = make_notification("N001")
        n.send()
        self.repo.save(n)
        results = self.repo.find_by_status("delivered")
        assert len(results) == 1


# ══════════════════════════════════════════════════════════════
# REPOSITORY FACTORY TESTS
# ══════════════════════════════════════════════════════════════

class TestRepositoryFactory:

    def test_get_patient_repository_memory(self):
        repo = RepositoryFactory.get_patient_repository("MEMORY")
        assert isinstance(repo, InMemoryPatientRepository)

    def test_get_doctor_repository_memory(self):
        repo = RepositoryFactory.get_doctor_repository("MEMORY")
        assert isinstance(repo, InMemoryDoctorRepository)

    def test_get_appointment_repository_memory(self):
        repo = RepositoryFactory.get_appointment_repository("MEMORY")
        assert isinstance(repo, InMemoryAppointmentRepository)

    def test_get_time_slot_repository_memory(self):
        repo = RepositoryFactory.get_time_slot_repository("MEMORY")
        assert isinstance(repo, InMemoryTimeSlotRepository)

    def test_get_medical_record_repository_memory(self):
        repo = RepositoryFactory.get_medical_record_repository("MEMORY")
        assert isinstance(repo, InMemoryMedicalRecordRepository)

    def test_get_notification_repository_memory(self):
        repo = RepositoryFactory.get_notification_repository("MEMORY")
        assert isinstance(repo, InMemoryNotificationRepository)

    def test_invalid_storage_type_raises(self):
        with pytest.raises(ValueError, match="Unsupported storage type"):
            RepositoryFactory.get_patient_repository("CLOUD")

    def test_factory_returns_independent_instances(self):
        repo1 = RepositoryFactory.get_patient_repository("MEMORY")
        repo2 = RepositoryFactory.get_patient_repository("MEMORY")
        repo1.save(make_patient("P001"))
        assert repo2.count() == 0  # independent instances