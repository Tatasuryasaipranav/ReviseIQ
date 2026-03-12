"""database.py — SQLite schema"""
import sqlite3
from config import DATABASE_PATH

def get_conn():
    conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db():
    conn = get_conn()
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS students(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL, email TEXT UNIQUE NOT NULL,
        exam_target TEXT NOT NULL, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)""")

    c.execute("""CREATE TABLE IF NOT EXISTS quiz_sessions(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER REFERENCES students(id),
        exam TEXT NOT NULL, subject TEXT,
        total_questions INTEGER, correct INTEGER, score_pct REAL,
        time_taken INTEGER, completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)""")

    c.execute("""CREATE TABLE IF NOT EXISTS quiz_answers(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id INTEGER REFERENCES quiz_sessions(id),
        question_id TEXT, subject TEXT, topic TEXT,
        selected TEXT, correct_answer TEXT, is_correct INTEGER,
        time_spent INTEGER DEFAULT 0)""")

    c.execute("""CREATE TABLE IF NOT EXISTS weak_topics(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER REFERENCES students(id),
        subject TEXT, topic TEXT, accuracy REAL,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(student_id, subject, topic))""")

    c.execute("""CREATE TABLE IF NOT EXISTS revision_plans(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER REFERENCES students(id),
        plan_json TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)""")

    c.execute("""CREATE TABLE IF NOT EXISTS daily_progress(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER REFERENCES students(id),
        date TEXT, subject TEXT, score REAL, notes TEXT,
        UNIQUE(student_id, date, subject))""")

    conn.commit(); conn.close()
    print("✅ DB ready")
