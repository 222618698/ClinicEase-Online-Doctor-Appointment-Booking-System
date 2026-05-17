"""
tests/test_api.py
Integration tests for all REST API endpoints using FastAPI TestClient.
Tests the full stack: API -> Service -> Repository
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pytest
from fastapi.testclient import TestClient
from api.main import app, patient_service, doctor_service, appointment_service

client = TestClient(app)


# ── Helpers ──────────────────────────────────────────────────

def create_test_patient(name="Test Patient", email="test@email.com"):
    return client.post("/api/patients", json={"name": name, "email": email})

def create_test_doctor(name="Dr Test", email="drtest@clinic.com", specialisation="GP"):
    return client.post("/api/doctors", json={
        "name": name, "email": email, "specialisation": specialisation
    })


# ── Reset state between tests ─────────────────────────────────

@pytest.fixture(autouse=True)
def reset_repos():
    """Clear all in-memory storage before each test."""
    patient_service._repo._storage.clear()
    patient_service._id_counter = 1
    doctor_service._repo._storage.clear()
    doctor_service._id_counter = 1
    appointment_service._appt_repo._storage.clear()
    appointment_service._slot_repo._storage.clear()
    appointment_service._id_counter = 1
    yield


# ══════════════════════════════════════════════════════════════
# HEALTH CHECK
# ══════════════════════════════════════════════════════════════

class TestHealthCheck:
    def test_root_returns_200(self):
        r = client.get("/")
        assert r.status_code == 200
        assert r.json()["status"] == "running"

    def test_root_contains_entities(self):
        r = client.get("/")
        assert "patients" in r.json()["entities"]


# ══════════════════════════════════════════════════════════════
# PATIENT API TESTS
# ══════════════════════════════════════════════════════════════

class TestPatientAPI:

    def test_create_patient_201(self):
        r = create_test_patient()
        assert r.status_code == 201
        assert r.json()["name"] == "Test Patient"
        assert r.json()["email"] == "test@email.com"
        assert "patient_id" in r.json()

    def test_create_patient_duplicate_email_409(self):
        create_test_patient()
        r = create_test_patient()
        assert r.status_code == 409
        assert "already registered" in r.json()["detail"]

    def test_create_patient_invalid_name_422(self):
        r = client.post("/api/patients", json={"name": "A", "email": "valid@email.com"})
        assert r.status_code == 422

    def test_create_patient_invalid_email_422(self):
        r = client.post("/api/patients", json={"name": "Valid Name", "email": "notanemail"})
        assert r.status_code == 422

    def test_get_all_patients_200(self):
        create_test_patient("P1", "p1@email.com")
        create_test_patient("P2", "p2@email.com")
        r = client.get("/api/patients")
        assert r.status_code == 200
        assert len(r.json()) == 2

    def test_get_patient_by_id_200(self):
        created = create_test_patient().json()
        r = client.get(f"/api/patients/{created['patient_id']}")
        assert r.status_code == 200
        assert r.json()["patient_id"] == created["patient_id"]

    def test_get_patient_not_found_404(self):
        r = client.get("/api/patients/GHOST")
        assert r.status_code == 404

    def test_update_patient_200(self):
        created = create_test_patient().json()
        r = client.put(f"/api/patients/{created['patient_id']}",
                       json={"name": "Updated Name"})
        assert r.status_code == 200
        assert r.json()["name"] == "Updated Name"

    def test_update_patient_not_found_404(self):
        r = client.put("/api/patients/GHOST", json={"name": "Name"})
        assert r.status_code == 404

    def test_delete_patient_204(self):
        created = create_test_patient().json()
        r = client.delete(f"/api/patients/{created['patient_id']}")
        assert r.status_code == 204

    def test_delete_patient_not_found_404(self):
        r = client.delete("/api/patients/GHOST")
        assert r.status_code == 404


# ══════════════════════════════════════════════════════════════
# DOCTOR API TESTS
# ══════════════════════════════════════════════════════════════

class TestDoctorAPI:

    def test_create_doctor_201(self):
        r = create_test_doctor()
        assert r.status_code == 201
        assert r.json()["specialisation"] == "GP"
        assert r.json()["profile_status"] == "active"

    def test_create_doctor_missing_specialisation_422(self):
        r = client.post("/api/doctors", json={
            "name": "Dr Valid", "email": "v@clinic.com", "specialisation": ""
        })
        assert r.status_code == 422

    def test_get_all_doctors_200(self):
        create_test_doctor("Dr A", "a@clinic.com", "GP")
        create_test_doctor("Dr B", "b@clinic.com", "Cardiology")
        r = client.get("/api/doctors")
        assert r.status_code == 200
        assert len(r.json()) == 2

    def test_get_available_doctors(self):
        d1 = create_test_doctor("Dr A", "a@clinic.com", "GP").json()
        d2 = create_test_doctor("Dr B", "b@clinic.com", "GP").json()
        client.patch(f"/api/doctors/{d2['doctor_id']}/unavailable")
        r = client.get("/api/doctors/available")
        assert r.status_code == 200
        assert len(r.json()) == 1

    def test_search_by_specialisation(self):
        create_test_doctor("Dr A", "a@clinic.com", "Cardiology")
        create_test_doctor("Dr B", "b@clinic.com", "GP")
        r = client.get("/api/doctors/search?specialisation=Cardiology")
        assert r.status_code == 200
        assert len(r.json()) == 1
        assert r.json()[0]["specialisation"] == "Cardiology"

    def test_get_doctor_by_id_200(self):
        created = create_test_doctor().json()
        r = client.get(f"/api/doctors/{created['doctor_id']}")
        assert r.status_code == 200

    def test_get_doctor_not_found_404(self):
        r = client.get("/api/doctors/GHOST")
        assert r.status_code == 404

    def test_set_doctor_unavailable(self):
        created = create_test_doctor().json()
        r = client.patch(f"/api/doctors/{created['doctor_id']}/unavailable")
        assert r.status_code == 200
        assert r.json()["profile_status"] == "unavailable"

    def test_set_doctor_available_again(self):
        created = create_test_doctor().json()
        client.patch(f"/api/doctors/{created['doctor_id']}/unavailable")
        r = client.patch(f"/api/doctors/{created['doctor_id']}/available")
        assert r.status_code == 200
        assert r.json()["profile_status"] == "active"

    def test_delete_doctor_204(self):
        created = create_test_doctor().json()
        r = client.delete(f"/api/doctors/{created['doctor_id']}")
        assert r.status_code == 204

    def test_delete_doctor_not_found_404(self):
        r = client.delete("/api/doctors/GHOST")
        assert r.status_code == 404


# ══════════════════════════════════════════════════════════════
# APPOINTMENT API TESTS
# ══════════════════════════════════════════════════════════════

class TestAppointmentAPI:

    def setup(self):
        """Create patient, doctor, slot for each test."""
        self.patient = create_test_patient("Sipho", "sipho@email.com").json()
        self.doctor = create_test_doctor("Dr K", "k@clinic.com", "GP").json()
        from datetime import datetime, timedelta
        slot_resp = client.post("/api/slots", json={
            "doctor_id": self.doctor["doctor_id"],
            "start_time": (datetime.now() + timedelta(hours=1)).isoformat(),
            "duration_minutes": 30
        })
        self.slot = slot_resp.json()

    def test_create_slot_201(self):
        self.setup()
        assert "slot_id" in self.slot
        assert self.slot["status"] == "available"

    def test_get_available_slots(self):
        self.setup()
        r = client.get(f"/api/doctors/{self.doctor['doctor_id']}/slots")
        assert r.status_code == 200
        assert len(r.json()) == 1

    def test_book_appointment_201(self):
        self.setup()
        r = client.post("/api/appointments", json={
            "patient_id": self.patient["patient_id"],
            "doctor_id": self.doctor["doctor_id"],
            "slot_id": self.slot["slot_id"]
        })
        assert r.status_code == 201
        assert r.json()["status"] == "confirmed"

    def test_book_appointment_double_booking_409(self):
        self.setup()
        p2 = create_test_patient("P2", "p2@email.com").json()
        client.post("/api/appointments", json={
            "patient_id": self.patient["patient_id"],
            "doctor_id": self.doctor["doctor_id"],
            "slot_id": self.slot["slot_id"]
        })
        r = client.post("/api/appointments", json={
            "patient_id": p2["patient_id"],
            "doctor_id": self.doctor["doctor_id"],
            "slot_id": self.slot["slot_id"]
        })
        assert r.status_code == 409

    def test_get_all_appointments(self):
        self.setup()
        client.post("/api/appointments", json={
            "patient_id": self.patient["patient_id"],
            "doctor_id": self.doctor["doctor_id"],
            "slot_id": self.slot["slot_id"]
        })
        r = client.get("/api/appointments")
        assert r.status_code == 200
        assert len(r.json()) == 1

    def test_cancel_appointment(self):
        self.setup()
        appt = client.post("/api/appointments", json={
            "patient_id": self.patient["patient_id"],
            "doctor_id": self.doctor["doctor_id"],
            "slot_id": self.slot["slot_id"]
        }).json()
        r = client.patch(f"/api/appointments/{appt['appointment_id']}/cancel")
        assert r.status_code == 200
        assert r.json()["status"] == "cancelled"

    def test_complete_appointment(self):
        self.setup()
        appt = client.post("/api/appointments", json={
            "patient_id": self.patient["patient_id"],
            "doctor_id": self.doctor["doctor_id"],
            "slot_id": self.slot["slot_id"]
        }).json()
        r = client.patch(
            f"/api/appointments/{appt['appointment_id']}/complete",
            json={"notes": "Patient is well."}
        )
        assert r.status_code == 200
        assert r.json()["status"] == "completed"

    def test_get_appointment_not_found_404(self):
        r = client.get("/api/appointments/GHOST")
        assert r.status_code == 404