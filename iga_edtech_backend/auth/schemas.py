
import re
from marshmallow import Schema, fields, validate, validates, ValidationError, validates_schema


PASSWORD_REGEX = re.compile(
    r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&_#\-])[A-Za-z\d@$!%*?&_#\-]{8,}$"
)
PHONE_REGEX = re.compile(r"^\+?[0-9\s\-]{7,15}$")


def _validate_password(value: str):
    if not PASSWORD_REGEX.match(value):
        raise ValidationError(

        )


class StudentRegisterSchema(Schema):
    full_name = fields.Str(required=True, validate=validate.Length(min=2, max=120))
    email = fields.Email(required=True)
    phone = fields.Str(load_default=None, validate=validate.Regexp(PHONE_REGEX))
    password = fields.Str(required=True, load_only=True)
    receive_promotions = fields.Bool(load_default=False)

    @validates("password")
    def validate_password(self, value):
        _validate_password(value)

    @validates_schema
    def require_email_or_phone(self, data, **kwargs):
        if not data.get("email") and not data.get("phone"):
            raise ValidationError("Either email or phone number is required.", "email")


class TeacherRegisterSchema(Schema):
    full_name = fields.Str(required=True, validate=validate.Length(min=2, max=120))
    email = fields.Email(required=True)
    phone = fields.Str(load_default=None, validate=validate.Regexp(PHONE_REGEX))
    password = fields.Str(required=True, load_only=True)
    department = fields.Str(load_default=None, validate=validate.Length(max=100))
    qualification = fields.Str(load_default=None, validate=validate.Length(max=200))
    receive_promotions = fields.Bool(load_default=False)

    @validates("password")
    def validate_password(self, value):
        _validate_password(value)


class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)


class VerifyEmailSchema(Schema):
    email = fields.Email(required=True)
    code = fields.Str(required=True, validate=validate.Length(equal=6))


class ResendOTPSchema(Schema):
    email = fields.Email(required=True)
    purpose = fields.Str(
        required=True,
        validate=validate.OneOf(["email_verification", "password_reset"]),
    )


class ForgotPasswordSchema(Schema):
    email = fields.Email(required=True)


class ResetPasswordSchema(Schema):
    email = fields.Email(required=True)
    code = fields.Str(required=True, validate=validate.Length(equal=6))
    new_password = fields.Str(required=True, load_only=True)

    @validates("new_password")
    def validate_new_password(self, value):
        _validate_password(value)


class UpdateProfileSchema(Schema):
    full_name = fields.Str(validate=validate.Length(min=2, max=120))
    phone = fields.Str(validate=validate.Regexp(PHONE_REGEX), allow_none=True)
    receive_promotions = fields.Bool()


    grade_level = fields.Str(validate=validate.Length(max=50))
    school_name = fields.Str(validate=validate.Length(max=200))
    language_preference = fields.Str(validate=validate.OneOf(["en", "rw"]))
    bio = fields.Str(validate=validate.Length(max=1000))

    department = fields.Str(validate=validate.Length(max=100))
    qualification = fields.Str(validate=validate.Length(max=200))
