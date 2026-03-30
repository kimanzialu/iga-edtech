import sqlite3
import os

DB_PATH = 'instance/iga_edtech_dev.db'

if not os.path.exists(DB_PATH):
    print(f"❌  Database not found at {DB_PATH}")
    print("    Make sure you run this from the backend root folder.")
    exit(1)

conn = sqlite3.connect(DB_PATH)
cur  = conn.cursor()

tables = [
    'lesson_completions',
    'submissions',
    'enrollments',
    'otp_codes',
    'token_blacklist',
    'student_profiles',
    'teacher_profiles',
    'users',
]

print("Clearing demo data...")
for table in tables:
    try:
        cur.execute(f"DELETE FROM {table}")
        print(f"  ✓ Cleared {table}")
    except Exception as e:
        print(f"  ⚠  {table}: {e}")

conn.commit()
conn.close()
print("\nDone. Database is clean")