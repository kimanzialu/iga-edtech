import sqlite3

conn = sqlite3.connect('instance/iga_edtech_dev.db')
cur  = conn.cursor()

try:
    cur.execute('ALTER TABLE submissions ADD COLUMN manual_scores TEXT DEFAULT "{}"')
    print('Added manual_scores')
except Exception as e:
    print(f'manual_scores: {e}')

try:
    cur.execute('ALTER TABLE submissions ADD COLUMN manual_comments TEXT DEFAULT "{}"')
    print('Added manual_comments')
except Exception as e:
    print(f'manual_comments: {e}')

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
    print('Created lesson_completions table')
except Exception as e:
    print(f'lesson_completions: {e}')

conn.commit()
conn.close()
print('Migration complete.')