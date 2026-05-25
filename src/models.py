"""
src/models.py - Appointment, TimeSlot, Notification, MedicalRecord, MedicationReminder
"""
from datetime import datetime, timedelta
from enum import Enum
from typing import List, Optional
import copy


# ─────────────────────────────────────────
# ENUMS
# ─────────────────────────────────────────

class AppointmentStatus(Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    RESCHEDULED = "rescheduled"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    NO_SHOW = "no_show"
    EXPIRED = "expired"


class SlotStatus(Enum):
    AVAILABLE = "available"
    RESERVED = "reserved"
    BOOKED = "booked"
    BLOCKED = "blocked"
    COMPLETED = "completed"
    EXPIRED = "expired"


class NotificationType(Enum):
    APPOINTMENT_CONFIRMATION = "appointment_confirmation"
    APPOINTMENT_REMINDER = "appointment_reminder"
    CANCELLATION = "cancellation"
    MEDICATION_REMINDER = "medication_reminder"
    REFILL_ALERT = "refill_alert"
    PROCEDURE_REMINDER = "procedure_reminder"


class NotificationStatus(Enum):
    QUEUED = "queued"
    SENDING = "sending"
    DELIVERED = "delivered"
    FAILED = "failed"
    RETRYING = "retrying"
    PERMANENT_FAILURE = "permanent_failure"
    READ = "read"
    ARCHIVED = "archived"


class ReminderStatus(Enum):
    SCHEDULED = "scheduled"
    ACTIVE = "active"
    PAUSED = "paused"
    CANCELLED = "cancelled"


# ─────────────────────────────────────────
# TIME SLOT
# ─────────────────────────────────────────

class TimeSlot:
    def __init__(self, slot_id: str, doctor_id: str,
                 start_time: datetime, end_time: datetime):
        self._slot_id = slot_id
        self._doctor_id = doctor_id
        self._start_time = start_time
        self._end_time = end_time
        self._status = SlotStatus.AVAILABLE
        self._duration_minutes = int((end_time - start_time).seconds / 60)

    @property
    def slot_id(self): return self._slot_id

    @property
    def doctor_id(self): return self._doctor_id

    @property
    def start_time(self): return self._start_time

    @property
    def status(self): return self._status

    @property
    def duration_minutes(self): return self._duration_minutes

    def is_available(self) -> bool:
        return self._status == SlotStatus.AVAILABLE

    def mark_reserved(self):
        if self._status != SlotStatus.AVAILABLE:
            raise ValueError(f"Slot {self._slot_id} is not available.")
        self._status = SlotStatus.RESERVED

    def mark_booked(self):
        self._status = SlotStatus.BOOKED

    def mark_available(self):
        self._status = SlotStatus.AVAILABLE

    def mark_blocked(self):
        self._status = SlotStatus.BLOCKED

    def mark_expired(self):
        self._status = SlotStatus.EXPIRED

    def mark_completed(self):
        self._status = SlotStatus.COMPLETED

    def __repr__(self):
        return f"<TimeSlot id={self._slot_id} start={self._start_time} status={self._status.value}>"


# ─────────────────────────────────────────
# APPOINTMENT
# ─────────────────────────────────────────

class Appointment:
    def __init__(self, appointment_id: str, patient_id: str,
                 doctor_id: str, slot_id: str):
        self._appointment_id = appointment_id
        self._patient_id = patient_id
        self._doctor_id = doctor_id
        self._slot_id = slot_id
        self._status = AppointmentStatus.PENDING
        self._created_at = datetime.now()
        self._updated_at = datetime.now()
        self._notes = ""
        self._notifications: List[str] = []

    @property
    def appointment_id(self): return self._appointment_id

    @property
    def patient_id(self): return self._patient_id

    @property
    def doctor_id(self): return self._doctor_id

    @property
    def slot_id(self): return self._slot_id

    @property
    def status(self): return self._status

    @property
    def notes(self): return self._notes

    def confirm(self):
        if self._status != AppointmentStatus.PENDING:
            raise ValueError("Only pending appointments can be confirmed.")
        self._status = AppointmentStatus.CONFIRMED
        self._updated_at = datetime.now()

    def cancel(self):
        if self._status in (AppointmentStatus.COMPLETED, AppointmentStatus.CANCELLED):
            raise ValueError("Cannot cancel a completed or already cancelled appointment.")
        self._status = AppointmentStatus.CANCELLED
        self._updated_at = datetime.now()

    def reschedule(self, new_slot_id: str):
        if self._status in (AppointmentStatus.COMPLETED, AppointmentStatus.CANCELLED):
            raise ValueError("Cannot reschedule a completed or cancelled appointment.")
        self._slot_id = new_slot_id
        self._status = AppointmentStatus.RESCHEDULED
        self._updated_at = datetime.now()

    def mark_in_progress(self):
        self._status = AppointmentStatus.IN_PROGRESS
        self._updated_at = datetime.now()

    def mark_completed(self, notes: str = ""):
        self._status = AppointmentStatus.COMPLETED
        self._notes = notes
        self._updated_at = datetime.now()

    def mark_no_show(self):
        self._status = AppointmentStatus.NO_SHOW
        self._updated_at = datetime.now()

    def send_confirmation_email(self) -> str:
        return f"Confirmation email queued for appointment {self._appointment_id}"

    def schedule_reminders(self) -> str:
        return f"Reminders scheduled for appointment {self._appointment_id}"

    def __repr__(self):
        return f"<Appointment id={self._appointment_id} status={self._status.value}>"


# ─────────────────────────────────────────
# NOTIFICATION
# ─────────────────────────────────────────

class Notification:
    MAX_RETRIES = 3

    def __init__(self, notification_id: str, recipient_id: str,
                 notification_type: NotificationType, message: str,
                 channel: str = "email"):
        self._notification_id = notification_id
        self._recipient_id = recipient_id
        self._type = notification_type
        self._message = message
        self._channel = channel
        self._status = NotificationStatus.QUEUED
        self._sent_at: Optional[datetime] = None
        self._retry_count = 0

    @property
    def notification_id(self): return self._notification_id

    @property
    def status(self): return self._status

    @property
    def retry_count(self): return self._retry_count

    @property
    def message(self): return self._message

    def send(self) -> bool:
        self._status = NotificationStatus.SENDING
        # Simulate delivery (in real system: call SMTP service)
        self._status = NotificationStatus.DELIVERED
        self._sent_at = datetime.now()
        return True

    def retry(self) -> bool:
        if self._retry_count >= self.MAX_RETRIES:
            self._status = NotificationStatus.PERMANENT_FAILURE
            return False
        self._retry_count += 1
        self._status = NotificationStatus.RETRYING
        return self.send()

    def mark_failed(self):
        self._status = NotificationStatus.FAILED

    def mark_delivered(self):
        self._status = NotificationStatus.DELIVERED
        self._sent_at = datetime.now()

    def mark_read(self):
        self._status = NotificationStatus.READ

    def archive(self):
        self._status = NotificationStatus.ARCHIVED

    def __repr__(self):
        return f"<Notification id={self._notification_id} type={self._type.value} status={self._status.value}>"


# ─────────────────────────────────────────
# MEDICAL RECORD
# ─────────────────────────────────────────

class MedicalRecord:
    def __init__(self, record_id: str, patient_id: str,
                 doctor_id: str, appointment_id: str):
        self._record_id = record_id
        self._patient_id = patient_id
        self._doctor_id = doctor_id
        self._appointment_id = appointment_id
        self._consultation_date = datetime.now()
        self._diagnosis = ""
        self._notes = ""
        self._prescriptions: List[str] = []
        self._test_results: List[dict] = []
        self._status = "active"

    @property
    def record_id(self): return self._record_id

    @property
    def patient_id(self): return self._patient_id

    @property
    def status(self): return self._status

    @property
    def diagnosis(self): return self._diagnosis

    @property
    def prescriptions(self): return list(self._prescriptions)

    def add_consultation_notes(self, diagnosis: str, notes: str):
        self._diagnosis = diagnosis
        self._notes = notes

    def add_prescription(self, prescription: str):
        self._prescriptions.append(prescription)

    def add_test_result(self, result: dict):
        self._test_results.append(result)

    def archive(self):
        self._status = "archived"

    def request_deletion(self):
        self._status = "pending_deletion"

    def get_full_history(self) -> dict:
        return {
            "record_id": self._record_id,
            "patient_id": self._patient_id,
            "diagnosis": self._diagnosis,
            "notes": self._notes,
            "prescriptions": self._prescriptions,
            "test_results": self._test_results,
            "status": self._status
        }

    def __repr__(self):
        return f"<MedicalRecord id={self._record_id} patient={self._patient_id} status={self._status}>"


# ─────────────────────────────────────────
# MEDICATION REMINDER
# ─────────────────────────────────────────

class MedicationReminder:
    REFILL_ALERT_THRESHOLD = 7  # days

    def __init__(self, reminder_id: str, patient_id: str,
                 medication_name: str, dosage: str,
                 frequency_per_day: int, supply_days: int):
        self._reminder_id = reminder_id
        self._patient_id = patient_id
        self._medication_name = medication_name
        self._dosage = dosage
        self._frequency_per_day = frequency_per_day
        self._supply_days = supply_days
        self._reminder_times: List[str] = []
        self._start_date = datetime.now()
        self._status = ReminderStatus.SCHEDULED

    @property
    def reminder_id(self): return self._reminder_id

    @property
    def medication_name(self): return self._medication_name

    @property
    def status(self): return self._status

    @property
    def supply_days(self): return self._supply_days

    def add_reminder_time(self, time_str: str):
        self._reminder_times.append(time_str)

    def schedule(self):
        self._status = ReminderStatus.SCHEDULED

    def pause(self):
        self._status = ReminderStatus.PAUSED

    def resume(self):
        self._status = ReminderStatus.SCHEDULED

    def cancel(self):
        self._status = ReminderStatus.CANCELLED

    def calculate_days_remaining(self) -> int:
        days_elapsed = (datetime.now() - self._start_date).days
        return max(0, self._supply_days - days_elapsed)

    def needs_refill_alert(self) -> bool:
        return self.calculate_days_remaining() <= self.REFILL_ALERT_THRESHOLD

    def trigger_reminder(self) -> str:
        self._status = ReminderStatus.ACTIVE
        return f"Reminder: Take {self._dosage} of {self._medication_name}"

    def send_refill_alert(self) -> str:
        days_left = self.calculate_days_remaining()
        return f"Refill alert: {self._medication_name} has {days_left} days remaining."

    def clone(self) -> "MedicationReminder":
        """Used by Prototype pattern."""
        return copy.deepcopy(self)

    def __repr__(self):
        return f"<MedicationReminder id={self._reminder_id} med={self._medication_name} status={self._status.value}>"