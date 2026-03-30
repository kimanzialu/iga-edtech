from datetime import datetime, timezone
from .base import db


class User(db.Model):
    
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    phone = db.Column(db.String(20), unique=True, nullable=True, index=True)

   
    password_hash = db.Column(db.String(255), nullable=False)

   
    role = db.Column(db.String(20), nullable=False, default="student")

  
    is_verified = db.Column(db.Boolean, default=False, nullable=False)

  
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    is_locked = db.Column(db.Boolean, default=False, nullable=False)
    locked_until = db.Column(db.DateTime(timezone=True), nullable=True)

    
    failed_login_attempts = db.Column(db.Integer, default=0, nullable=False)

    
    receive_promotions = db.Column(db.Boolean, default=False, nullable=False)

    created_at = db.Column(
        db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

   
    student_profile = db.relationship(
        "StudentProfile", back_populates="user", uselist=False, cascade="all, delete-orphan"
    )
    teacher_profile = db.relationship(
        "TeacherProfile", back_populates="user", uselist=False, cascade="all, delete-orphan"
    )
    otps = db.relationship("OTPCode", back_populates="user", cascade="all, delete-orphan")



    def is_account_locked(self):
        
        if not self.is_locked:
            return False
        if self.locked_until:
            locked_until = self.locked_until
            if locked_until.tzinfo is None:
                locked_until = locked_until.replace(tzinfo=timezone.utc)
            if datetime.now(timezone.utc) > locked_until:
                self.is_locked = False
                self.failed_login_attempts = 0
                self.locked_until = None
                db.session.commit()
                return False
        return True

    def to_dict(self):
        return {
            "id": self.id,
            "full_name": self.full_name,
            "email": self.email,
            "phone": self.phone,
            "role": self.role,
            "is_verified": self.is_verified,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

    def __repr__(self):
        return f"<User {self.email} [{self.role}]>"


class StudentProfile(db.Model):
   
    __tablename__ = "student_profiles"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=True, nullable=False)
    grade_level = db.Column(db.String(50), nullable=True)
    language_preference = db.Column(db.String(10), default="en")  
    school_name = db.Column(db.String(200), nullable=True)
    bio = db.Column(db.Text, nullable=True)

    user = db.relationship("User", back_populates="student_profile")

    def to_dict(self):
        return {
            "grade_level": self.grade_level,
            "language_preference": self.language_preference,
            "school_name": self.school_name,
            "bio": self.bio,
        }


class TeacherProfile(db.Model):
   
    __tablename__ = "teacher_profiles"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=True, nullable=False)
    department = db.Column(db.String(100), nullable=True)
    qualification = db.Column(db.String(200), nullable=True)
    bio = db.Column(db.Text, nullable=True)
    language_preference = db.Column(db.String(10), default="en")

    user = db.relationship("User", back_populates="teacher_profile")

    def to_dict(self):
        return {
            "department": self.department,
            "qualification": self.qualification,
            "bio": self.bio,
            "language_preference": self.language_preference,
        }


class OTPCode(db.Model):
    
    __tablename__ = "otp_codes"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    code = db.Column(db.String(6), nullable=False)
    purpose = db.Column(db.String(30), nullable=False)

    is_used = db.Column(db.Boolean, default=False)
    expires_at = db.Column(db.DateTime(timezone=True), nullable=False)
    created_at = db.Column(
        db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    user = db.relationship("User", back_populates="otps")

    def is_expired(self):
        expires = self.expires_at
        if expires.tzinfo is None:
            expires = expires.replace(tzinfo=timezone.utc)
        return datetime.now(timezone.utc) > expires

    def __repr__(self):
        return f"<OTP user={self.user_id} purpose={self.purpose} used={self.is_used}>"


class TokenBlacklist(db.Model):
   
    __tablename__ = "token_blacklist"

    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), unique=True, nullable=False, index=True)
    token_type = db.Column(db.String(10), nullable=False)   
    revoked_at = db.Column(
        db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    def __repr__(self):
        return f"<BlacklistedToken jti={self.jti}>"