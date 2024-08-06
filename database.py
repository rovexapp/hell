import sqlite3

conn = sqlite3.connect('bot_database.db')
cursor = conn.cursor()

# إنشاء جدول المستخدمين
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    clicks INTEGER DEFAULT 0,
    invites INTEGER DEFAULT 0,
    currency INTEGER DEFAULT 0
)''')

# إنشاء جدول الدعوات
cursor.execute('''CREATE TABLE IF NOT EXISTS invites (
    user_id INTEGER,
    invited_user_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (invited_user_id) REFERENCES users(user_id)
)''')

conn.commit()
conn.close()
