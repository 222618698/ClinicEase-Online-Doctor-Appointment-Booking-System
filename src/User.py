"""
src/user.py - Base User class for ClinicEase
"""
from datetime import datetime
from enum import Enum
import bcrypt


class UserRole(Enum):
    PATIENT = "patient"
    DOCTOR = "doctor"
    RECEPTIONIST = "receptionist"
    ADMIN = "admin"


class UserStatus(Enum):
    UNVERIFIED = "unverified"
    ACTIVE = "active"
    LOCKED = "locked"
    SUSPENDED = "suspended"
    DEACTIVATED = "deactivated"
    DELETED = "deleted"


class User:
    def __init__(self, user_id: str, name: str, email: str, role: UserRole):
        self._user_id = user_id
        self._name = name
        self._email = email
        self._password_hash = ""
        self._role = role
        self._status = UserStatus.UNVERIFIED
        self._created_at = datetime.now()
        self._last_login_at = None
        self._failed_login_attempts = 0

    # ── Getters ──
    @property
    def user_id(self): return self._user_id

    @property
    def name(self): return self._name

    @property
    def email(self): return self._email

    @property
    def role(self): return self._role

    @property
    def status(self): return self._status

    @property
    def created_at(self): return self._created_at

    # ── Methods ──
    def register(self, password: str) -> bool:
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters.")
        salt = bcrypt.gensalt(rounds=12)
        self._password_hash = bcrypt.hashpw(password.encode(), salt).decode()
        self._status = UserStatus.UNVERIFIED
        return True

    def login(self, password: str) -> bool:
        if self._status == UserStatus.LOCKED:
            raise PermissionError("Account is locked. Please try again later.")
        if self._status in (UserStatus.SUSPENDED, UserStatus.DEACTIVATED, UserStatus.DELETED):
            raise PermissionError(f"Account is {self._status.value}.")
        if bcrypt.checkpw(password.encode(), self._password_hash.encode()):
            self._failed_login_attempts = 0
            self._last_login_at = datetime.now()
            self._status = UserStatus.ACTIVE
            return True
        else:
            self._failed_login_attempts += 1
            if self._failed_login_attempts >= 5:
                self._status = UserStatus.LOCKED
            return False

    def logout(self):
        self._last_login_at = datetime.now()

    def update_profile(self, name: str = None, email: str = None):
        if name:
            self._name = name
        if email:
            self._email = email

    def change_password(self, old_password: str, new_password: str) -> bool:
        if not bcrypt.checkpw(old_password.encode(), self._password_hash.encode()):
            return False
        if len(new_password) < 8:
            raise ValueError("Password must be at least 8 characters.")
        salt = bcrypt.gensalt(rounds=12)
        self._password_hash = bcrypt.hashpw(new_password.encode(), salt).decode()
        return True

    def activate(self):
        self._status = UserStatus.ACTIVE

    def deactivate(self):
        self._status = UserStatus.DEACTIVATED

    def unlock(self):
        self._failed_login_attempts = 0
        self._status = UserStatus.ACTIVE

    def __repr__(self):
        return f"<User id={self._user_id} name={self._name} role={self._role.value} status={self._status.value}>"