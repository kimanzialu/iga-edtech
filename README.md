# Iga EdTech LMS
**Rwanda's Digital Learning Management System**

A full-stack web-based Learning Management System (LMS) built for Rwandan students and teachers. Students can register, enroll in courses, access learning materials, take assessments, and track their progress. Teachers can create and manage courses, upload content, build assessments, and grade students — all in both **Kinyarwanda** and **English**.

> Built by Yannick Kenny Imanzi — African Leadership University (ALU), 2026

---

## Live Demo
**[https://iga-edtech.vercel.app](https://iga-edtech.vercel.app)**

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | HTML, CSS, Vanilla JavaScript |
| Backend | Python / Flask |
| Database | SQLite via SQLAlchemy |
| Authentication | JWT (Flask-JWT-Extended) + Email OTP (Flask-Mail) |
| PDF Reports | ReportLab |
| Deployment | Render (backend) · Vercel (frontend) |

---

## Project Structure

```
iga-edtech/
├── README.md
│
├── iga_edtech_backend/          # Flask backend
│   ├── app.py                   # App factory + blueprint registration
│   ├── config.py                # Dev / Prod / Test configs
│   ├── requirements.txt
│   ├── migrate_lockout.py       # DB migration script
│   ├── delete_user.py           # Delete a specific user by email
│   ├── models/
│   │   ├── base.py
│   │   ├── user.py              # User, StudentProfile, TeacherProfile, OTPCode, TokenBlacklist
│   │   └── course.py            # Course, Module, Lesson, Enrollment, Assessment, Question, Submission, LessonCompletion
│   ├── auth/
│   │   ├── routes.py            # /auth/* endpoints (login, register, OTP, profile, deactivate)
│   │   ├── schemas.py
│   │   └── utils.py
│   ├── courses/
│   │   ├── routes.py            # /courses/* endpoints (CRUD, enroll, grade, export)
│   │   └── schemas.py
│   ├── utils/
│   │   └── decorators.py        # student_required, teacher_required, admin_required
│   └── uploads/
│       └── lessons/             # Uploaded lesson files saved here
│
└── iga_edtech_frontend/         # Frontend
    ├── index.html               # Homepage
    ├── css/
    │   ├── main.css
    │   └── shared-auth.css
    ├── js/
    │   ├── api.js               # API client + Auth session helpers
    │   ├── components.js        # Navbar + Footer injection
    │   └── i18n.js              # EN/RW translations (332 keys)
    ├── pages/
    │   ├── login.html
    │   ├── register.html
    │   ├── teacher-login.html
    │   ├── teacher-register.html
    │   ├── student-dashboard.html
    │   └── teacher-dashboard.html
    └── assets/
        └── home_books.jpg
```

---

## Local Setup Instructions

### Prerequisites
- Python 3.10+
- Git
- A Gmail account (for OTP emails)
- VS Code with the Live Server extension (recommended)

---

### Step 1 — Clone the repository

```bash
git clone https://github.com/kimanzialu/iga-edtech.git
cd iga-edtech
```

---

### Step 2 — Set up the backend

```bash
cd iga_edtech_backend
```

**Create and activate a virtual environment:**
```bash
python -m venv venv

# Mac/Linux:
source venv/bin/activate

# Windows:
venv\Scripts\activate
```

**Install dependencies:**
```bash
pip install -r requirements.txt
```

**Create a `.env` file** inside `iga_edtech_backend/`:
```env
SECRET_KEY=change-this-to-a-random-string
JWT_SECRET_KEY=change-this-to-another-random-string

MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-gmail@gmail.com
MAIL_PASSWORD=your-16-character-app-password
```

> **How to get a Gmail App Password:**
> 1. Enable 2-Step Verification on your Google account
> 2. Go to [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)
> 3. Generate a password for "Mail" → copy the 16-character code
> 4. Paste it as `MAIL_PASSWORD` in your `.env`

**Initialize and migrate the database:**
```bash
python app.py
# Flask creates instance/iga_edtech_dev.db on first run
# Press Ctrl+C to stop, then run:

python migrate_lockout.py
```

**Start the backend:**
```bash
python app.py
```
Backend runs at `http://127.0.0.1:5000`

---

### Step 3 — Run the frontend

The frontend is plain HTML/CSS/JS — no build step required.

Open `iga_edtech_frontend/index.html` with **Live Server** in VS Code (right-click → Open with Live Server), or open it directly in your browser.

> Make sure the Flask backend is running on port 5000 first.

---

### Step 4 — Create test accounts

1. Go to `pages/register.html` → register a **Student** account
2. Go to `pages/teacher-register.html` → register a **Teacher** account
3. Log in and explore

---

## Language Support

Full **English and Kinyarwanda** switching is supported across all pages. Click the globe icon in the navbar or the language toggle in the sidebar. All 332 UI strings are translated.

---

## SRS Document
https://docs.google.com/document/d/1GRkbGOEaSuGxWcceyBDCPUMX2m1WsFxt57og5NL-7I4/edit?usp=sharing

## Video Link
https://www.boomshare.ai/shared/01KN1SZ0AS6SCW8M8Y0PA50RK8

