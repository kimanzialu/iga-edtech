# Iga EdTech LMS — Auth Module

## Project Structure
```
iga_edtech/
├── app.py                  # Flask app factory + entry point
├── config.py               # Config classes (Dev / Prod / Test)
├── .env.example            # Environment variables template
├── requirements.txt        # All dependencies
│
├── models/
│   ├── __init__.py
│   ├── base.py             # SQLAlchemy db instance
│   └── user.py             # User, StudentProfile, TeacherProfile models
│
├── auth/
│   ├── __init__.py
│   ├── routes.py           # All /auth/* endpoints
│   ├── schemas.py          # Marshmallow validation schemas
│   └── utils.py            # OTP generation, email helpers
│
└── utils/
    ├── __init__.py
    └── decorators.py       # role_required, jwt wrappers
```

## Auth Endpoints
| Method | Endpoint                    | Description                        |
|--------|-----------------------------|------------------------------------|
| POST   | /auth/register/student      | Register new student               |
| POST   | /auth/register/teacher      | Register new teacher               |
| POST   | /auth/login                 | Login (both roles)                 |
| POST   | /auth/verify-email          | Verify OTP sent to email           |
| POST   | /auth/resend-otp            | Resend verification OTP            |
| POST   | /auth/forgot-password       | Request password reset             |
| POST   | /auth/reset-password        | Reset password with token          |
| POST   | /auth/refresh               | Refresh JWT access token           |
| POST   | /auth/logout                | Logout (blacklist token)           |
| GET    | /auth/me                    | Get current user profile           |
| PUT    | /auth/me                    | Update current user profile        |
| DELETE | /auth/me                    | Deactivate account (REQ-8)         |
