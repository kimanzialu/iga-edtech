
import json
import pytest
from app import create_app
from config import TestingConfig
from models import db as _db, User, OTPCode


@pytest.fixture(scope="function")
def app():
    application = create_app(TestingConfig)
    with application.app_context():
        _db.create_all()
        yield application
        _db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def student_payload():
    return {
        "full_name": "Alice Uwimana",
        "email": "alice@example.com",
        "password": "SecurePass1!",
    }


@pytest.fixture
def teacher_payload():
    return {
        "full_name": "Mr. Mugisha",
        "email": "mugisha@school.rw",
        "password": "TeachPass1@",
        "department": "Mathematics",
    }


def post(client, url, data):
    return client.post(url, json=data, content_type="application/json")


def _register_and_verify(client, payload, role="student"):
    url = f"/auth/register/{role}"
    r = post(client, url, payload)
    assert r.status_code == 201


    with client.application.app_context():
        user = User.query.filter_by(email=payload["email"]).first()
        otp = OTPCode.query.filter_by(
            user_id=user.id, purpose="email_verification", is_used=False
        ).first()
        code = otp.code

    post(client, "/auth/verify-email", {"email": payload["email"], "code": code})
    return payload["email"]


class TestStudentRegistration:
    def test_success(self, client, student_payload):
        r = post(client, "/auth/register/student", student_payload)
        assert r.status_code == 201
        data = r.get_json()
        assert data["success"] is True
        assert "email" in data["data"]

    def test_duplicate_email(self, client, student_payload):
        post(client, "/auth/register/student", student_payload)
        r = post(client, "/auth/register/student", student_payload)
        assert r.status_code == 409

    def test_weak_password(self, client, student_payload):
        student_payload["password"] = "weak"
        r = post(client, "/auth/register/student", student_payload)
        assert r.status_code == 422

    def test_invalid_email(self, client, student_payload):
        student_payload["email"] = "not-an-email"
        r = post(client, "/auth/register/student", student_payload)
        assert r.status_code == 422

    def test_missing_name(self, client):
        r = post(client, "/auth/register/student", {"email": "a@b.com", "password": "Abc1@xyz"})
        assert r.status_code == 422


class TestTeacherRegistration:
    def test_success(self, client, teacher_payload):
        r = post(client, "/auth/register/teacher", teacher_payload)
        assert r.status_code == 201
        assert r.get_json()["success"] is True

    def test_role_is_teacher(self, client, teacher_payload):
        post(client, "/auth/register/teacher", teacher_payload)
        with client.application.app_context():
            user = User.query.filter_by(email=teacher_payload["email"]).first()
            assert user.role == "teacher"


class TestEmailVerification:
    def test_verify_success(self, client, student_payload):
        post(client, "/auth/register/student", student_payload)
        with client.application.app_context():
            user = User.query.filter_by(email=student_payload["email"]).first()
            otp = OTPCode.query.filter_by(user_id=user.id, is_used=False).first()
            code = otp.code

        r = post(client, "/auth/verify-email", {
            "email": student_payload["email"], "code": code
        })
        assert r.status_code == 200
        assert r.get_json()["success"] is True

    def test_wrong_code(self, client, student_payload):
        post(client, "/auth/register/student", student_payload)
        r = post(client, "/auth/verify-email", {
            "email": student_payload["email"], "code": "000000"
        })
        assert r.status_code == 400

    def test_already_verified(self, client, student_payload):
        _register_and_verify(client, student_payload)
        r = post(client, "/auth/verify-email", {
            "email": student_payload["email"], "code": "anything"
        })
        assert r.status_code == 200  



class TestLogin:
    def test_success(self, client, student_payload):
        _register_and_verify(client, student_payload)
        r = post(client, "/auth/login", {
            "email": student_payload["email"], "password": student_payload["password"]
        })
        assert r.status_code == 200
        data = r.get_json()["data"]
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["user"]["role"] == "student"

    def test_wrong_password(self, client, student_payload):
        _register_and_verify(client, student_payload)
        r = post(client, "/auth/login", {
            "email": student_payload["email"], "password": "WrongPass1!"
        })
        assert r.status_code == 401

    def test_unverified_account(self, client, student_payload):
        post(client, "/auth/register/student", student_payload)
        r = post(client, "/auth/login", {
            "email": student_payload["email"], "password": student_payload["password"]
        })
        assert r.status_code == 403

    def test_account_lock_after_5_attempts(self, client, student_payload):
        _register_and_verify(client, student_payload)
        for _ in range(5):
            post(client, "/auth/login", {
                "email": student_payload["email"], "password": "WrongPass1!"
            })
        r = post(client, "/auth/login", {
            "email": student_payload["email"], "password": student_payload["password"]
        })
        assert r.status_code == 423

    def test_deactivated_account(self, client, student_payload):
        _register_and_verify(client, student_payload)
        with client.application.app_context():
            user = User.query.filter_by(email=student_payload["email"]).first()
            user.is_active = False
            _db.session.commit()
        r = post(client, "/auth/login", {
            "email": student_payload["email"], "password": student_payload["password"]
        })
        assert r.status_code == 403


class TestPasswordReset:
    def test_forgot_password_always_200(self, client):
        r = post(client, "/auth/forgot-password", {"email": "nonexistent@x.com"})
        assert r.status_code == 200  

    def test_full_reset_flow(self, client, student_payload):
        _register_and_verify(client, student_payload)
        post(client, "/auth/forgot-password", {"email": student_payload["email"]})

        with client.application.app_context():
            user = User.query.filter_by(email=student_payload["email"]).first()
            otp = OTPCode.query.filter_by(
                user_id=user.id, purpose="password_reset", is_used=False
            ).first()
            code = otp.code

        r = post(client, "/auth/reset-password", {
            "email": student_payload["email"],
            "code": code,
            "new_password": "NewSecure2@",
        })
        assert r.status_code == 200

        r = post(client, "/auth/login", {
            "email": student_payload["email"], "password": "NewSecure2@"
        })
        assert r.status_code == 200



class TestProfile:
    def _login_token(self, client, payload):
        _register_and_verify(client, payload)
        r = post(client, "/auth/login", {
            "email": payload["email"], "password": payload["password"]
        })
        return r.get_json()["data"]["access_token"]

    def test_get_me(self, client, student_payload):
        token = self._login_token(client, student_payload)
        r = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
        assert r.status_code == 200
        assert r.get_json()["data"]["email"] == student_payload["email"]

    def test_update_me(self, client, student_payload):
        token = self._login_token(client, student_payload)
        r = client.put(
            "/auth/me",
            json={"full_name": "Alice Updated", "grade_level": "S3"},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert r.status_code == 200
        assert r.get_json()["data"]["full_name"] == "Alice Updated"

    def test_deactivate_account(self, client, student_payload):
        token = self._login_token(client, student_payload)
        r = client.delete("/auth/me", headers={"Authorization": f"Bearer {token}"})
        assert r.status_code == 200
       
        r2 = post(client, "/auth/login", {
            "email": student_payload["email"], "password": student_payload["password"]
        })
        assert r2.status_code == 403
