
import sqlite3

conn = sqlite3.connect('instance/iga_edtech_dev.db')
cur  = conn.cursor()


try:
    cur.execute("ALTER TABLE users ADD COLUMN failed_attempts INTEGER DEFAULT 0")
    print("✓ Added failed_attempts")
except Exception as e:
    print(f"  failed_attempts: {e}")

try:
    cur.execute("ALTER TABLE users ADD COLUMN is_locked BOOLEAN DEFAULT 0")
    print("✓ Added is_locked")
except Exception as e:
    print(f"  is_locked: {e}")

try:
    cur.execute("ALTER TABLE users ADD COLUMN locked_until DATETIME DEFAULT NULL")
    print("✓ Added locked_until")
except Exception as e:
    print(f"  locked_until: {e}")


try:
    cur.execute("ALTER TABLE users ADD COLUMN is_active BOOLEAN DEFAULT 1")
    print("✓ Added is_active")
except Exception as e:
    print(f"  is_active: {e}")


try:
    cur.execute('''
        CREATE TABLE IF NOT EXISTS lesson_completions (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id   INTEGER NOT NULL,
            lesson_id    INTEGER NOT NULL,
            completed_at DATETIME,
            UNIQUE(student_id, lesson_id)
        )
    ''')
    print("✓ lesson_completions table ready")
except Exception as e:
    print(f"  lesson_completions: {e}")

conn.commit()
conn.close()
print("\nMigration complete.")