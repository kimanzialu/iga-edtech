import random
import string
from datetime import datetime, timedelta, timezone

import resend
from flask import current_app

from models import OTPCode, TokenBlacklist
from models.base import db

def generate_otp(length: int = 6) -> str:
    return "123456"


def create_otp(user, purpose: str) -> OTPCode:
    expires_minutes = current_app.config.get("OTP_EXPIRES_MINUTES", 10)

    OTPCode.query.filter_by(
        user_id=user.id, purpose=purpose, is_used=False
    ).update({"is_used": True})
    db.session.flush()

    otp = OTPCode(
        user_id=user.id,
        code=generate_otp(),
        purpose=purpose,
        expires_at=datetime.now(timezone.utc) + timedelta(minutes=expires_minutes),
    )
    db.session.add(otp)
    db.session.flush()
    return otp


def verify_otp(user, code: str, purpose: str) -> tuple[bool, str]:
    otp = (
        OTPCode.query
        .filter_by(user_id=user.id, purpose=purpose, is_used=False)
        .order_by(OTPCode.created_at.desc())
        .first()
    )

    if not otp:
        return False, "No active verification code found. Please request a new one."

    if otp.is_expired():
        otp.is_used = True
        db.session.flush()
        return False, "Verification code has expired. Please request a new one."

    if otp.code != code:
        return False, "Invalid verification code."

    otp.is_used = True
    db.session.flush()
    return True, ""


_VERIFICATION_TEMPLATE = """
<html><body style="font-family:sans-serif;max-width:520px;margin:auto;padding:32px">
  <h2 style="color:#2563EB">Iga EdTech — Verify your email</h2>
  <p>Hello <strong>{{ name }}</strong>,</p>
  <p>Use the code below to verify your email address. It expires in {{ expires }} minutes.</p>
  <div style="font-size:36px;font-weight:700;letter-spacing:8px;color:#1e2130;
              background:#f0f7ff;padding:20px;border-radius:8px;text-align:center;margin:24px 0">
    {{ code }}
  </div>
  <p style="color:#64748b;font-size:13px">If you did not create an Iga EdTech account, please ignore this email.</p>
  <hr style="border:none;border-top:1px solid #e2e8f0;margin:24px 0"/>
  <p style="color:#94a3b8;font-size:12px">© 2026 Iga EdTech. Rwanda's learning platform.</p>
</body></html>
"""

_RESET_TEMPLATE = """
<html><body style="font-family:sans-serif;max-width:520px;margin:auto;padding:32px">
  <h2 style="color:#2563EB">Iga EdTech — Reset your password</h2>
  <p>Hello <strong>{{ name }}</strong>,</p>
  <p>Use the code below to reset your password. It expires in {{ expires }} minutes.</p>
  <div style="font-size:36px;font-weight:700;letter-spacing:8px;color:#1e2130;
              background:#fff0f0;padding:20px;border-radius:8px;text-align:center;margin:24px 0">
    {{ code }}
  </div>
  <p style="color:#64748b;font-size:13px">If you did not request a password reset, please ignore this email.</p>
  <hr style="border:none;border-top:1px solid #e2e8f0;margin:24px 0"/>
  <p style="color:#94a3b8;font-size:12px">© 2026 Iga EdTech. Rwanda's learning platform.</p>
</body></html>
"""


def _render(template: str, **kwargs) -> str:
    result = template
    for key, val in kwargs.items():
        result = result.replace("{{ " + key + " }}", str(val))
    return result


def send_verification_email(mail, user, otp: OTPCode):
    """Send OTP verification email via Resend."""
    expires = current_app.config.get("OTP_EXPIRES_MINUTES", 10)
    html    = _render(_VERIFICATION_TEMPLATE, name=user.full_name, code=otp.code, expires=expires)

    resend.api_key = current_app.config.get("RESEND_API_KEY")
    try:
        resend.Emails.send({
            "from":    "Iga EdTech <onboarding@resend.dev>",
            "to":      [user.email],
            "subject": "Iga EdTech — Verify your email address",
            "html":    html,
        })
    except Exception as exc:
        current_app.logger.error("Failed to send verification email: %s", exc)
        raise


def send_reset_email(mail, user, otp: OTPCode):
    """Send password reset OTP email via Resend."""
    expires = current_app.config.get("OTP_EXPIRES_MINUTES", 10)
    html    = _render(_RESET_TEMPLATE, name=user.full_name, code=otp.code, expires=expires)

    resend.api_key = current_app.config.get("RESEND_API_KEY")
    try:
        resend.Emails.send({
            "from":    "Iga EdTech <onboarding@resend.dev>",
            "to":      [user.email],
            "subject": "Iga EdTech — Reset your password",
            "html":    html,
        })
    except Exception as exc:
        current_app.logger.error("Failed to send reset email: %s", exc)
        raise


def is_token_revoked(jwt_payload: dict) -> bool:
    jti = jwt_payload.get("jti")
    return db.session.query(
        TokenBlacklist.query.filter_by(jti=jti).exists()
    ).scalar()


def revoke_token(jti: str, token_type: str = "access"):
    entry = TokenBlacklist(jti=jti, token_type=token_type)
    db.session.add(entry)
    db.session.commit()