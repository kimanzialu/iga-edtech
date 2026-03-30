from datetime import datetime, timedelta, timezone

from flask import Blueprint, current_app, jsonify, request
from flask_bcrypt import Bcrypt
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt,
    get_jwt_identity,
    jwt_required,
)
from marshmallow import ValidationError

from models import OTPCode, StudentProfile, TeacherProfile, TokenBlacklist, User
from models.base import db

from .schemas import (
    ForgotPasswordSchema,
    LoginSchema,
    ResendOTPSchema,
    ResetPasswordSchema,
    StudentRegisterSchema,
    TeacherRegisterSchema,
    UpdateProfileSchema,
    VerifyEmailSchema,
)
from .utils import (
    create_otp,
    revoke_token,
    send_reset_email,
    send_verification_email,
    verify_otp,
)

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

bcrypt = Bcrypt()

def _json_error(message, status=400, errors=None):
    body = {"success": False, "message": message}
    if errors:
        body["errors"] = errors
    return jsonify(body), status


def _json_ok(message, data=None, status=200, **extra):
    body = {"success": True, "message": message}
    if data is not None:
        body["data"] = data
    body.update(extra)
    return jsonify(body), status


def _load_json(schema_cls):
    raw = request.get_json(silent=True) or {}
    schema = schema_cls()
    try:
        return schema.load(raw), None
    except ValidationError as exc:
        return None, exc.messages


def _get_mail():
    from flask_mail import Mail
    return current_app.extensions.get("mail") or Mail(current_app)


def _safe_send_verification(mail, user, otp):
    """Send verification email without crashing the request on failure."""
    try:
        send_verification_email(mail, user, otp)
    except Exception as e:
        current_app.logger.error(
            "Failed to send verification email to %s: %s", user.email, e
        )


def _safe_send_reset(mail, user, otp):
    """Send reset email without crashing the request on failure."""
    try:
        send_reset_email(mail, user, otp)
    except Exception as e:
        current_app.logger.error(
            "Failed to send reset email to %s: %s", user.email, e
        )


@auth_bp.route("/register/student", methods=["POST"])
def register_student():
    data, errors = _load_json(StudentRegisterSchema)
    if errors:
        return _json_error("Validation failed.", 422, errors)

    user = User(
        full_name=data["full_name"],
        email=data["email"],
        phone=data.get("phone"),
        password_hash=bcrypt.generate_password_hash(data["password"]).decode("utf-8"),
        role="student",
        receive_promotions=data.get("receive_promotions", False),
    )
    db.session.add(user)
    db.session.flush()

    profile = StudentProfile(user_id=user.id)
    db.session.add(profile)

    otp = create_otp(user, "email_verification")
    db.session.commit()

    _safe_send_verification(_get_mail(), user, otp)

    return _json_ok(
        "Account created! Please check your email for a verification code.",
        data={"user_id": user.id, "email": user.email},
        status=201,
    )


@auth_bp.route("/register/teacher", methods=["POST"])
def register_teacher():
    data, errors = _load_json(TeacherRegisterSchema)
    if errors:
        return _json_error("Validation failed.", 422, errors)

    user = User(
        full_name=data["full_name"],
        email=data["email"],
        phone=data.get("phone"),
        password_hash=bcrypt.generate_password_hash(data["password"]).decode("utf-8"),
        role="teacher",
        receive_promotions=data.get("receive_promotions", False),
    )
    db.session.add(user)
    db.session.flush()

    profile = TeacherProfile(
        user_id=user.id,
        department=data.get("department"),
        qualification=data.get("qualification"),
    )
    db.session.add(profile)

    otp = create_otp(user, "email_verification")
    user.is_verified = True
    db.session.commit()

    _safe_send_verification(_get_mail(), user, otp)

    return _json_ok(
        "Teacher account created! Please verify your email.",
        data={"user_id": user.id, "email": user.email},
        status=201,
    )


@auth_bp.route("/verify-email", methods=["POST"])
def verify_email():
    data, errors = _load_json(VerifyEmailSchema)
    if errors:
        return _json_error("Validation failed.", 422, errors)

    user = User.query.filter_by(email=data["email"]).first()
    if not user:
        return _json_error("No account found with this email address.", 404)

    if user.is_verified:
        return _json_ok("Email already verified. You can log in.")

    ok, msg = verify_otp(user, data["code"], "email_verification")
    if not ok:
        return _json_error(msg, 400)

    user.is_verified = True
    db.session.commit()

    return _json_ok("Email verified successfully. You can now log in.")


@auth_bp.route("/resend-otp", methods=["POST"])
def resend_otp():
    data, errors = _load_json(ResendOTPSchema)
    if errors:
        return _json_error("Validation failed.", 422, errors)

    user = User.query.filter_by(email=data["email"]).first()

    if not user:
        return _json_ok("If that email exists, a new code has been sent.")

    otp = create_otp(user, data["purpose"])
    db.session.commit()

    if data["purpose"] == "email_verification":
        _safe_send_verification(_get_mail(), user, otp)
    else:
        _safe_send_reset(_get_mail(), user, otp)

    return _json_ok("A new verification code has been sent to your email.")


@auth_bp.route("/login", methods=["POST"])
def login():
    data, errors = _load_json(LoginSchema)
    if errors:
        return _json_error("Validation failed.", 422, errors)

    user = User.query.filter_by(email=data["email"]).first()

    _bad_creds = lambda: _json_error("Invalid email or password.", 401)

    if not user:
        return _bad_creds()

    if not user.is_active:
        return _json_error(
            "This account has been deactivated. Contact support to reactivate.", 403
        )

    if user.is_account_locked():
        unlock_time = user.locked_until.strftime("%H:%M UTC") if user.locked_until else "soon"
        return _json_error(
            f"Account locked due to too many failed attempts. Try again after {unlock_time}.",
            423,
        )

    if not bcrypt.check_password_hash(user.password_hash, data["password"]):
        user.failed_login_attempts += 1
        max_attempts = current_app.config.get("MAX_LOGIN_ATTEMPTS", 5)
        lock_minutes = current_app.config.get("ACCOUNT_LOCK_MINUTES", 30)

        if user.failed_login_attempts >= max_attempts:
            user.is_locked = True
            user.locked_until = datetime.now(timezone.utc) + timedelta(minutes=lock_minutes)
            db.session.commit()
            return _json_error(
                f"Too many failed attempts. Your account has been locked for "
                f"{lock_minutes} minutes. A notification has been sent to your email.",
                423,
            )

        remaining = max_attempts - user.failed_login_attempts
        db.session.commit()
        return _json_error(
            f"Invalid email or password. {remaining} attempt(s) remaining.", 401
        )

    if not user.is_verified:
        return _json_error(
            "Please verify your email address before logging in. "
            "Check your inbox or request a new code.",
            403,
        )

    user.failed_login_attempts = 0
    user.is_locked = False
    db.session.commit()

    additional_claims = {"role": user.role, "full_name": user.full_name}
    access_token = create_access_token(
        identity=str(user.id), additional_claims=additional_claims
    )
    refresh_token = create_refresh_token(identity=str(user.id))

    return _json_ok(
        "Logged in successfully.",
        data={
            "user": user.to_dict(),
            "access_token": access_token,
            "refresh_token": refresh_token,
        },
    )


@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    user_id = get_jwt_identity()
    user = db.session.get(User, int(user_id))
    if not user or not user.is_active:
        return _json_error("User not found or deactivated.", 404)

    additional_claims = {"role": user.role, "full_name": user.full_name}
    new_access = create_access_token(
        identity=user_id, additional_claims=additional_claims
    )
    return _json_ok("Token refreshed.", data={"access_token": new_access})


@auth_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    jwt_data = get_jwt()
    revoke_token(jwt_data["jti"], "access")
    return _json_ok("Logged out successfully.")


@auth_bp.route("/forgot-password", methods=["POST"])
def forgot_password():
    data, errors = _load_json(ForgotPasswordSchema)
    if errors:
        return _json_error("Validation failed.", 422, errors)

    user = User.query.filter_by(email=data["email"]).first()
    if user and user.is_active:
        otp = create_otp(user, "password_reset")
        db.session.commit()
        _safe_send_reset(_get_mail(), user, otp)

    return _json_ok(
        "If an account exists with that email, a password reset code has been sent."
    )


@auth_bp.route("/reset-password", methods=["POST"])
def reset_password():
    data, errors = _load_json(ResetPasswordSchema)
    if errors:
        return _json_error("Validation failed.", 422, errors)

    user = User.query.filter_by(email=data["email"]).first()
    if not user:
        return _json_error("No account found with this email address.", 404)

    ok, msg = verify_otp(user, data["code"], "password_reset")
    if not ok:
        return _json_error(msg, 400)

    user.password_hash = bcrypt.generate_password_hash(data["new_password"]).decode("utf-8")
    user.is_locked = False
    user.failed_login_attempts = 0
    user.locked_until = None
    db.session.commit()

    return _json_ok("Password reset successfully. You can now log in with your new password.")


@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def get_me():
    user_id = get_jwt_identity()
    user = db.session.get(User, int(user_id))
    if not user or not user.is_active:
        return _json_error("User not found.", 404)

    profile_data = {}
    if user.role == "student" and user.student_profile:
        profile_data = user.student_profile.to_dict()
    elif user.role == "teacher" and user.teacher_profile:
        profile_data = user.teacher_profile.to_dict()

    return _json_ok("Profile retrieved.", data={**user.to_dict(), "profile": profile_data})


@auth_bp.route("/me", methods=["PUT"])
@jwt_required()
def update_me():
    user_id = get_jwt_identity()
    user = db.session.get(User, int(user_id))
    if not user or not user.is_active:
        return _json_error("User not found.", 404)

    data, errors = _load_json(UpdateProfileSchema)
    if errors:
        return _json_error("Validation failed.", 422, errors)

    if "full_name" in data:
        user.full_name = data["full_name"]
    if "phone" in data:
        if data["phone"] != user.phone:
            conflict = User.query.filter_by(phone=data["phone"]).first()
            if conflict:
                return _json_error("That phone number is already in use.", 409)
        user.phone = data["phone"]
    if "receive_promotions" in data:
        user.receive_promotions = data["receive_promotions"]

    STUDENT_FIELDS = ["grade_level", "school_name", "language_preference", "bio"]
    TEACHER_FIELDS = ["department", "qualification", "bio", "language_preference"]

    if user.role == "student" and user.student_profile:
        profile = user.student_profile
        for field in STUDENT_FIELDS:
            if field in data:
                setattr(profile, field, data[field])

    elif user.role == "teacher" and user.teacher_profile:
        profile = user.teacher_profile
        for field in TEACHER_FIELDS:
            if field in data:
                setattr(profile, field, data[field])

    db.session.commit()
    return _json_ok("Profile updated successfully.", data=user.to_dict())


@auth_bp.route("/me", methods=["DELETE"])
@jwt_required()
def deactivate_account():
    user_id = get_jwt_identity()
    user = db.session.get(User, int(user_id))
    if not user:
        return _json_error("User not found.", 404)

    user.is_active = False
    jwt_data = get_jwt()
    revoke_token(jwt_data["jti"], "access")
    db.session.commit()

    return _json_ok("Account deactivated. Contact support if you wish to reactivate.")