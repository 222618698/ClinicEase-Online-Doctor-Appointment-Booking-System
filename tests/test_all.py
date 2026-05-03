"""
tests/test_all.py
Unit tests for all six creational patterns and core ClinicEase classes.
Run with: pytest tests/ -v --tb=short
"""

import pytest
import threading
from datetime import datetime, timedelta

from src.user import UserStatus, UserRole
from src.users import Patient, Doctor, Receptionist, Administrator
from src.models import (
    Appointment, AppointmentStatus,
    TimeSlot, SlotStatus,
    Notification, NotificationType, NotificationStatus,
    MedicalRecord,
    MedicationReminder, ReminderStatus
)
from creational_patterns.patterns import (
    UserFactory,
    AppointmentConfirmationCreator,
    MedicationReminderCreator,
    CancellationNotificationCreator,
    RefillAlertCreator,
    StandardSchedulingFactory,
    UrgentSchedulingFactory,
    MedicalRecordBuilder,
    MedicationReminderPrototype,
    DatabaseConnection
)


# ══════════════════════════════════════════════════════════════
# CORE CLASS TESTS
# ══════════════════════════════════════════════════════════════

class TestUser:
    def test_register_hashes_password(self):
        patient = Patient("P001", "Sipho Dlamini", "sipho@email.com")
        patient.register("SecurePass123")
        assert patient._password_hash != "SecurePass123"
        assert patient._password_hash.startswith("$2b$")

    def test_register_rejects_short_password(self):
        patient = Patient("P002", "Amara Nkosi", "amara@email.com")
        with pytest.raises(ValueError, match="at least 8 characters"):
            patient.register("short")

    def test_login_success_sets_active(self):
        patient = Patient("P003", "Fatima Adams", "fatima@email.com")
        patient.register("ValidPass99")
        result = patient.login("ValidPass99")
        assert result is True
        assert patient.status == UserStatus.ACTIVE

    def test_login_wrong_password_returns_false(self):
        patient = Patient("P004", "Thabo Mokoena", "thabo@email.com")
        patient.register("CorrectPass1")
        result = patient.login("WrongPass!")
        assert result is False

    def test_account_locks_after_5_failed_attempts(self):
        patient = Patient("P005", "Zanele Khumalo", "zanele@email.com")
        patient.register("PasswordABC1")
        for _ in range(5):
            patient.login("wrongpassword")
        assert patient.status == UserStatus.LOCKED

    def test_locked_account_raises_on_login(self):
        patient = Patient("P006", "Nomsa Sithole", "nomsa@email.com")
        patient.register("TestPassword1")
        patient._status = UserStatus.LOCKED
        with pytest.raises(PermissionError, match="locked"):
            patient.login("TestPassword1")

    def test_unlock_resets_status(self):
        patient = Patient("P007", "Keamo Tau", "keamo@email.com")
        patient.register("UnlockTest12")
        patient._status = UserStatus.LOCKED
        patient.unlock()
        assert patient.status == UserStatus.ACTIVE


class TestTimeSlot:
    def test_new_slot_is_available(self):
        slot = TimeSlot("S001", "D001",
                        datetime.now(), datetime.now() + timedelta(minutes=30))
        assert slot.is_available() is True
        assert slot.status == SlotStatus.AVAILABLE

    def test_mark_reserved(self):
        slot = TimeSlot("S002", "D001",
                        datetime.now(), datetime.now() + timedelta(minutes=30))
        slot.mark_reserved()
        assert slot.status == SlotStatus.RESERVED

    def test_mark_reserved_when_not_available_raises(self):
        slot = TimeSlot("S003", "D001",
                        datetime.now(), datetime.now() + timedelta(minutes=30))
        slot.mark_blocked()
        with pytest.raises(ValueError):
            slot.mark_reserved()

    def test_mark_booked(self):
        slot = TimeSlot("S004", "D001",
                        datetime.now(), datetime.now() + timedelta(minutes=30))
        slot.mark_reserved()
        slot.mark_booked()
        assert slot.status == SlotStatus.BOOKED

    def test_duration_calculated_correctly(self):
        start = datetime.now()
        end = start + timedelta(minutes=45)
        slot = TimeSlot("S005", "D001", start, end)
        assert slot.duration_minutes == 45


class TestAppointment:
    def test_new_appointment_is_pending(self):
        appt = Appointment("A001", "P001", "D001", "S001")
        assert appt.status == AppointmentStatus.PENDING

    def test_confirm_changes_status(self):
        appt = Appointment("A002", "P001", "D001", "S001")
        appt.confirm()
        assert appt.status == AppointmentStatus.CONFIRMED

    def test_cancel_confirmed_appointment(self):
        appt = Appointment("A003", "P001", "D001", "S001")
        appt.confirm()
        appt.cancel()
        assert appt.status == AppointmentStatus.CANCELLED

    def test_cannot_cancel_completed_appointment(self):
        appt = Appointment("A004", "P001", "D001", "S001")
        appt.confirm()
        appt.mark_in_progress()
        appt.mark_completed("Patient reviewed.")
        with pytest.raises(ValueError, match="Cannot cancel"):
            appt.cancel()

    def test_reschedule_updates_slot(self):
        appt = Appointment("A005", "P001", "D001", "S001")
        appt.confirm()
        appt.reschedule("S002")
        assert appt.slot_id == "S002"
        assert appt.status == AppointmentStatus.RESCHEDULED

    def test_mark_no_show(self):
        appt = Appointment("A006", "P001", "D001", "S001")
        appt.confirm()
        appt.mark_no_show()
        assert appt.status == AppointmentStatus.NO_SHOW

    def test_completed_appointment_has_notes(self):
        appt = Appointment("A007", "P001", "D001", "S001")
        appt.confirm()
        appt.mark_in_progress()
        appt.mark_completed("Hypertension diagnosed.")
        assert appt.notes == "Hypertension diagnosed."


class TestNotification:
    def test_new_notification_is_queued(self):
        notif = Notification("N001", "P001",
                             NotificationType.APPOINTMENT_CONFIRMATION,
                             "Your appointment is confirmed.")
        assert notif.status == NotificationStatus.QUEUED

    def test_send_delivers_notification(self):
        notif = Notification("N002", "P001",
                             NotificationType.MEDICATION_REMINDER,
                             "Time to take your tablets.")
        result = notif.send()
        assert result is True
        assert notif.status == NotificationStatus.DELIVERED

    def test_retry_increments_count(self):
        notif = Notification("N003", "P001",
                             NotificationType.REFILL_ALERT,
                             "Refill needed.")
        notif.mark_failed()
        notif.retry()
        assert notif.retry_count == 1

    def test_permanent_failure_after_max_retries(self):
        notif = Notification("N004", "P001",
                             NotificationType.CANCELLATION,
                             "Appointment cancelled.")
        notif._retry_count = 3
        result = notif.retry()
        assert result is False
        assert notif.status == NotificationStatus.PERMANENT_FAILURE

    def test_mark_read(self):
        notif = Notification("N005", "P001",
                             NotificationType.APPOINTMENT_REMINDER,
                             "Reminder: appointment tomorrow.")
        notif.send()
        notif.mark_read()
        assert notif.status == NotificationStatus.READ


class TestMedicalRecord:
    def test_add_diagnosis(self):
        record = MedicalRecord("R001", "P001", "D001", "A001")
        record.add_consultation_notes("Hypertension", "Patient reports headaches.")
        assert record.diagnosis == "Hypertension"

    def test_add_prescription(self):
        record = MedicalRecord("R002", "P001", "D001", "A001")
        record.add_prescription("Amlodipine 5mg daily")
        assert "Amlodipine 5mg daily" in record.prescriptions

    def test_archive_changes_status(self):
        record = MedicalRecord("R003", "P001", "D001", "A001")
        record.archive()
        assert record.status == "archived"

    def test_request_deletion_changes_status(self):
        record = MedicalRecord("R004", "P001", "D001", "A001")
        record.request_deletion()
        assert record.status == "pending_deletion"


class TestMedicationReminder:
    def test_days_remaining_calculated(self):
        reminder = MedicationReminder("M001", "P001",
                                      "Metformin", "500mg", 2, 30)
        days = reminder.calculate_days_remaining()
        assert days == 30  # just created, no days elapsed

    def test_needs_refill_alert_when_low(self):
        reminder = MedicationReminder("M002", "P001",
                                      "Lisinopril", "10mg", 1, 5)
        assert reminder.needs_refill_alert() is True

    def test_no_refill_alert_when_sufficient(self):
        reminder = MedicationReminder("M003", "P001",
                                      "Aspirin", "100mg", 1, 60)
        assert reminder.needs_refill_alert() is False

    def test_cancel_changes_status(self):
        reminder = MedicationReminder("M004", "P001",
                                      "Vitamin D", "1000IU", 1, 30)
        reminder.cancel()
        assert reminder.status == ReminderStatus.CANCELLED

    def test_pause_and_resume(self):
        reminder = MedicationReminder("M005", "P001",
                                      "Iron", "65mg", 1, 30)
        reminder.pause()
        assert reminder.status == ReminderStatus.PAUSED
        reminder.resume()
        assert reminder.status == ReminderStatus.SCHEDULED


# ══════════════════════════════════════════════════════════════
# PATTERN TESTS
# ══════════════════════════════════════════════════════════════

class TestSimpleFactory:
    """Tests for UserFactory (Simple Factory pattern)."""

    def test_creates_patient(self):
        user = UserFactory.create_user("patient", "P100", "Sipho", "sipho@test.com")
        assert isinstance(user, Patient)
        assert user.role == UserRole.PATIENT

    def test_creates_doctor(self):
        user = UserFactory.create_user("doctor", "D100", "Dr Nkosi", "nkosi@test.com",
                                       specialisation="Cardiology")
        assert isinstance(user, Doctor)
        assert user.specialisation == "Cardiology"

    def test_creates_receptionist(self):
        user = UserFactory.create_user("receptionist", "R100", "Aisha", "aisha@test.com")
        assert isinstance(user, Receptionist)

    def test_creates_admin(self):
        user = UserFactory.create_user("admin", "A100", "SuperUser", "admin@test.com")
        assert isinstance(user, Administrator)

    def test_invalid_role_raises_error(self):
        with pytest.raises(ValueError, match="Unknown role"):
            UserFactory.create_user("manager", "X100", "John", "john@test.com")

    def test_case_insensitive_role(self):
        user = UserFactory.create_user("PATIENT", "P101", "Thandi", "thandi@test.com")
        assert isinstance(user, Patient)


class TestFactoryMethod:
    """Tests for NotificationCreator subclasses (Factory Method pattern)."""

    def test_appointment_confirmation_creator(self):
        creator = AppointmentConfirmationCreator("A001", "Dr Mokoena", "2026-04-01 09:00")
        notif = creator.create_notification("N001", "P001")
        assert notif._type == NotificationType.APPOINTMENT_CONFIRMATION
        assert "Dr Mokoena" in notif.message
        assert "confirmed" in notif.message

    def test_medication_reminder_creator(self):
        creator = MedicationReminderCreator("Aspirin", "100mg")
        notif = creator.create_notification("N002", "P002")
        assert notif._type == NotificationType.MEDICATION_REMINDER
        assert "Aspirin" in notif.message
        assert "100mg" in notif.message

    def test_cancellation_creator(self):
        creator = CancellationNotificationCreator("A005")
        notif = creator.create_notification("N003", "P003")
        assert notif._type == NotificationType.CANCELLATION
        assert "cancelled" in notif.message.lower()

    def test_refill_alert_creator(self):
        creator = RefillAlertCreator("Metformin", 5)
        notif = creator.create_notification("N004", "P004")
        assert notif._type == NotificationType.REFILL_ALERT
        assert "5" in notif.message
        assert "Metformin" in notif.message

    def test_notify_sends_notification(self):
        creator = AppointmentConfirmationCreator("A002", "Dr Sithole", "2026-04-02 10:00")
        notif = creator.notify("N005", "P005")
        assert notif.status == NotificationStatus.DELIVERED


class TestAbstractFactory:
    """Tests for StandardSchedulingFactory and UrgentSchedulingFactory."""

    def test_standard_factory_creates_30_min_slot(self):
        factory = StandardSchedulingFactory()
        slot = factory.create_time_slot("S001", "D001")
        assert slot.duration_minutes == 30

    def test_standard_factory_creates_confirmed_appointment(self):
        factory = StandardSchedulingFactory()
        appt = factory.create_appointment("A001", "P001", "D001", "S001")
        assert appt.status == AppointmentStatus.CONFIRMED

    def test_urgent_factory_creates_15_min_slot(self):
        factory = UrgentSchedulingFactory()
        slot = factory.create_time_slot("S002", "D001")
        assert slot.duration_minutes == 15

    def test_urgent_factory_creates_in_progress_appointment(self):
        factory = UrgentSchedulingFactory()
        appt = factory.create_appointment("A002", "P001", "D001", "S002")
        assert appt.status == AppointmentStatus.IN_PROGRESS

    def test_factories_produce_different_slot_durations(self):
        standard = StandardSchedulingFactory()
        urgent = UrgentSchedulingFactory()
        s_slot = standard.create_time_slot("S003", "D001")
        u_slot = urgent.create_time_slot("S004", "D001")
        assert s_slot.duration_minutes != u_slot.duration_minutes


class TestBuilder:
    """Tests for MedicalRecordBuilder (Builder pattern)."""

    def test_build_basic_record(self):
        record = (MedicalRecordBuilder("R001", "P001", "D001", "A001")
                  .build())
        assert isinstance(record, MedicalRecord)
        assert record.patient_id == "P001"

    def test_build_with_diagnosis(self):
        record = (MedicalRecordBuilder("R002", "P001", "D001", "A001")
                  .with_diagnosis("Type 2 Diabetes", "Patient has elevated glucose.")
                  .build())
        assert record.diagnosis == "Type 2 Diabetes"

    def test_build_with_prescription(self):
        record = (MedicalRecordBuilder("R003", "P001", "D001", "A001")
                  .with_prescription("Metformin 500mg twice daily")
                  .build())
        assert "Metformin 500mg twice daily" in record.prescriptions

    def test_build_with_multiple_prescriptions(self):
        record = (MedicalRecordBuilder("R004", "P001", "D001", "A001")
                  .with_prescription("Metformin 500mg")
                  .with_prescription("Aspirin 100mg")
                  .build())
        assert len(record.prescriptions) == 2

    def test_build_with_test_result(self):
        record = (MedicalRecordBuilder("R005", "P001", "D001", "A001")
                  .with_test_result("HbA1c", "7.2%", "2026-03-01")
                  .build())
        history = record.get_full_history()
        assert len(history["test_results"]) == 1
        assert history["test_results"][0]["test_name"] == "HbA1c"

    def test_builder_chaining(self):
        """Full chain: diagnosis + prescriptions + test result."""
        record = (MedicalRecordBuilder("R006", "P001", "D001", "A001")
                  .with_diagnosis("Hypertension", "BP 145/95")
                  .with_prescription("Amlodipine 5mg daily")
                  .with_prescription("Lisinopril 10mg daily")
                  .with_test_result("Blood Pressure", "145/95", "2026-03-15")
                  .build())
        assert record.diagnosis == "Hypertension"
        assert len(record.prescriptions) == 2
        history = record.get_full_history()
        assert len(history["test_results"]) == 1


class TestPrototype:
    """Tests for MedicationReminderPrototype (Prototype pattern)."""

    def setup_method(self):
        """Register a prototype before each test."""
        MedicationReminderPrototype._prototypes.clear()
        template = MedicationReminder(
            "TEMPLATE_001", "TEMPLATE_PATIENT",
            "Amlodipine", "5mg", 1, 90
        )
        template.add_reminder_time("08:00")
        MedicationReminderPrototype.register("amlodipine_5mg", template)

    def test_clone_creates_new_instance(self):
        cloned = MedicationReminderPrototype.clone(
            "amlodipine_5mg", "M100", "P001"
        )
        assert cloned is not MedicationReminderPrototype._prototypes["amlodipine_5mg"]

    def test_clone_copies_medication_name(self):
        cloned = MedicationReminderPrototype.clone(
            "amlodipine_5mg", "M101", "P002"
        )
        assert cloned.medication_name == "Amlodipine"

    def test_clone_assigns_new_patient_id(self):
        cloned = MedicationReminderPrototype.clone(
            "amlodipine_5mg", "M102", "P003"
        )
        assert cloned._patient_id == "P003"

    def test_clone_assigns_new_reminder_id(self):
        cloned = MedicationReminderPrototype.clone(
            "amlodipine_5mg", "M103", "P004"
        )
        assert cloned.reminder_id == "M103"

    def test_modifying_clone_does_not_affect_prototype(self):
        cloned = MedicationReminderPrototype.clone(
            "amlodipine_5mg", "M104", "P005"
        )
        cloned.cancel()
        original = MedicationReminderPrototype._prototypes["amlodipine_5mg"]
        assert original.status == ReminderStatus.SCHEDULED

    def test_unknown_prototype_raises_key_error(self):
        with pytest.raises(KeyError):
            MedicationReminderPrototype.clone("unknown_med", "M999", "P999")

    def test_list_prototypes(self):
        prototypes = MedicationReminderPrototype.list_prototypes()
        assert "amlodipine_5mg" in prototypes


class TestSingleton:
    """Tests for DatabaseConnection (Singleton pattern)."""

    def setup_method(self):
        """Reset singleton before each test."""
        DatabaseConnection.reset_instance()

    def test_same_instance_returned(self):
        db1 = DatabaseConnection()
        db2 = DatabaseConnection()
        assert db1 is db2

    def test_connect_sets_connected(self):
        db = DatabaseConnection()
        db.connect()
        assert db.is_connected is True

    def test_execute_query_increments_count(self):
        db = DatabaseConnection()
        db.connect()
        db.execute_query("SELECT 1")
        db.execute_query("SELECT 2")
        assert db.query_count == 2

    def test_execute_without_connect_raises(self):
        db = DatabaseConnection()
        with pytest.raises(ConnectionError, match="not connected"):
            db.execute_query("SELECT 1")

    def test_disconnect_sets_not_connected(self):
        db = DatabaseConnection()
        db.connect()
        db.disconnect()
        assert db.is_connected is False

    def test_thread_safety(self):
        """Multiple threads should get the same singleton instance."""
        instances = []

        def get_instance():
            instances.append(DatabaseConnection())

        threads = [threading.Thread(target=get_instance) for _ in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        # All instances must be the same object
        first = instances[0]
        assert all(inst is first for inst in instances)

    def test_host_default_value(self):
        db = DatabaseConnection()
        assert db.host == "localhost"