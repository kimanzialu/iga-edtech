# Iga EdTech LMS — Auth Module Setup

## Quick Start

```bash
# 1. Clone / unzip the project
cd iga_edtech

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment variables
cp .env.example .env
# Edit .env with your SMTP credentials and secret keys

# 5. Run the development server
python app.py
```

The server starts at http://localhost:5000

## Running Tests

```bash
pip install pytest
python -m pytest test_auth.py -v
```

## API Reference

### Register Student
```
POST /auth/register/student
{
  "full_name": "Alice Uwimana",
  "email": "alice@example.com",
  "password": "SecurePass1!",
  "receive_promotions": false
}
```

### Register Teacher
```
POST /auth/register/teacher
{
  "full_name": "Mr. Mugisha",
  "email": "mugisha@school.rw",
  "password": "TeachPass1@",
  "department": "Mathematics"
}
```

### Verify Email (OTP)
```
POST /auth/verify-email
{ "email": "alice@example.com", "code": "482917" }
```

### Login
```
POST /auth/login
{ "email": "alice@example.com", "password": "SecurePass1!" }
```
Response includes `access_token` and `refresh_token`.

### Forgot Password
```
POST /auth/forgot-password
{ "email": "alice@example.com" }
```

### Reset Password
```
POST /auth/reset-password
{ "email": "alice@example.com", "code": "391827", "new_password": "NewPass1!" }
```

### Get My Profile
```
GET /auth/me
Authorization: Bearer <access_token>
```

### Update My Profile
```
PUT /auth/me
Authorization: Bearer <access_token>
{ "full_name": "Alice K. Uwimana", "grade_level": "S3", "language_preference": "rw" }
```

### Deactivate Account
```
DELETE /auth/me
Authorization: Bearer <access_token>
```

### Logout
```
POST /auth/logout
Authorization: Bearer <access_token>
```

### Refresh Token
```
POST /auth/refresh
Authorization: Bearer <refresh_token>
```

## Password Rules
- Minimum 8 characters
- At least one uppercase letter
- At least one lowercase letter
- At least one digit
- At least one special character: `@$!%*?&_#-`

## Security Features (SRS §5.1)
- **bcrypt** password hashing (never stored plain-text)
- **JWT** access tokens (30 min) + refresh tokens (30 days)
- **Token blacklist** — logout truly invalidates tokens
- **OTP email verification** — 6-digit, 10-minute expiry
- **Account lock** after 5 failed login attempts (REQ-4)
- **No user enumeration** — forgot-password always returns 200
- **Role-based access control** — student / teacher / admin (REQ-2)
- **Account deactivation** — soft delete, reactivatable by admin (REQ-8)
