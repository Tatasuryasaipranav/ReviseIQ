"""routes/api.py — All REST endpoints"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from database import get_conn
from services.llm_service import analyze_quiz_results, generate_revision_plan, get_study_materials, get_ai_hint
from services.analytics import update_weak_topics, get_dashboard
from questions.question_bank import (get_questions_by_exam, get_questions_by_subject,
                                      get_all_exams, get_subjects_for_exam, get_topics_for_subject)
import json, random, threading

router = APIRouter()

# ── STUDENTS ────────────────────────────────────────────────
class StudentIn(BaseModel):
    name: str; email: EmailStr; exam_target: str

@router.post("/students")
def create_student(d: StudentIn):
    conn = get_conn()
    try:
        c = conn.cursor()
        c.execute("INSERT INTO students(name,email,exam_target) VALUES(?,?,?)",
                  (d.name, d.email, d.exam_target))
        conn.commit()
        sid = c.lastrowid
        conn.close()
        return {"id": sid, "name": d.name, "exam_target": d.exam_target}
    except Exception as e:
        conn.close()
        raise HTTPException(400, str(e))

@router.get("/students/{sid}")
def get_student(sid: int):
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT * FROM students WHERE id=?", (sid,))
    r = c.fetchone(); conn.close()
    if not r: raise HTTPException(404, "Not found")
    return dict(r)

@router.get("/students/by-email/{email}")
def get_by_email(email: str):
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT * FROM students WHERE email=?", (email,))
    r = c.fetchone(); conn.close()
    if not r: raise HTTPException(404, "Not found")
    return dict(r)

# ── QUESTIONS ────────────────────────────────────────────────
@router.get("/questions/exams")
def list_exams():
    return get_all_exams()

@router.get("/questions/{exam}")
def get_quiz_questions(exam: str, subject: str = None, count: int = 10):
    if subject:
        qs = get_questions_by_subject(exam, subject)
    else:
        qs = get_questions_by_exam(exam)
    random.shuffle(qs)
    return qs[:count]

@router.get("/questions/{exam}/subjects")
def get_subjects(exam: str):
    return get_subjects_for_exam(exam)

@router.get("/hint")
def get_hint(question_id: str, exam: str, subject: str, topic: str, question_text: str):
    hint = get_ai_hint(question_text, subject, topic, exam)
    return {"hint": hint}

# ── QUIZ SESSION ────────────────────────────────────────────
class AnswerItem(BaseModel):
    question_id: str; subject: str; topic: str
    selected: str; correct_answer: str; is_correct: bool; time_spent: int = 0

class SessionSubmit(BaseModel):
    student_id: int; exam: str; subject: str | None = None
    answers: list[AnswerItem]; time_taken: int = 0

@router.post("/quiz/submit")
def submit_quiz(d: SessionSubmit):
    conn = get_conn()
    c = conn.cursor()
    correct = sum(1 for a in d.answers if a.is_correct)
    total = len(d.answers)
    score = round(correct / total * 100, 1) if total else 0

    c.execute("""INSERT INTO quiz_sessions(student_id,exam,subject,total_questions,correct,score_pct,time_taken)
                 VALUES(?,?,?,?,?,?,?)""",
              (d.student_id, d.exam, d.subject, total, correct, score, d.time_taken))
    sid = c.lastrowid

    for a in d.answers:
        c.execute("""INSERT INTO quiz_answers(session_id,question_id,subject,topic,selected,correct_answer,is_correct,time_spent)
                     VALUES(?,?,?,?,?,?,?,?)""",
                  (sid, a.question_id, a.subject, a.topic, a.selected, a.correct_answer,
                   1 if a.is_correct else 0, a.time_spent))
    conn.commit(); conn.close()

    # Update weak topics immediately (fast — pure DB)
    weak = update_weak_topics(d.student_id)

    # Run AI analysis in background so response is instant
    answers_dict = [a.model_dump() for a in d.answers]
    def run_analysis():
        try:
            sc = get_conn().cursor()
            sc.execute("SELECT name FROM students WHERE id=?", (d.student_id,))
            row = sc.fetchone()
            sname = row["name"] if row else "Student"
            analyze_quiz_results(sname, d.exam, answers_dict)
        except Exception as e:
            print(f"[AI Analysis background error] {e}")

    threading.Thread(target=run_analysis, daemon=True).start()

    return {"session_id": sid, "score": score, "correct": correct, "total": total,
            "analysis": {"summary": "✅ Quiz saved! AI analysis is running in the background.",
                         "coaching_tips": [], "weak_topics": [], "error_patterns": []},
            "weak_topics_updated": weak}

@router.get("/quiz/history/{student_id}")
def quiz_history(student_id: int):
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT * FROM quiz_sessions WHERE student_id=? ORDER BY completed_at DESC", (student_id,))
    rows = [dict(r) for r in c.fetchall()]; conn.close()
    return rows

@router.get("/quiz/session/{session_id}/answers")
def session_answers(session_id: int):
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT * FROM quiz_answers WHERE session_id=?", (session_id,))
    rows = [dict(r) for r in c.fetchall()]; conn.close()
    return rows

# ── DASHBOARD ────────────────────────────────────────────────
@router.get("/dashboard/{student_id}")
def dashboard(student_id: int):
    update_weak_topics(student_id)   # always recalculate before serving
    return get_dashboard(student_id)

@router.get("/dashboard/{student_id}/weak-topics")
def weak_topics(student_id: int):
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT * FROM weak_topics WHERE student_id=? ORDER BY accuracy ASC", (student_id,))
    rows = [dict(r) for r in c.fetchall()]; conn.close()
    return rows

# ── REVISION PLAN ────────────────────────────────────────────
@router.post("/plan/{student_id}/generate")
def gen_plan(student_id: int):
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT * FROM students WHERE id=?", (student_id,))
    s = c.fetchone()
    if not s: conn.close(); raise HTTPException(404, "Student not found")
    c.execute("SELECT subject,topic,accuracy FROM weak_topics WHERE student_id=? ORDER BY accuracy ASC LIMIT 8", (student_id,))
    weak = [dict(r) for r in c.fetchall()]; conn.close()
    if not weak:
        raise HTTPException(400, "Take at least one quiz first to generate your plan!")
    plan = generate_revision_plan(s["name"], s["exam_target"], weak)
    conn2 = get_conn()
    conn2.execute("INSERT INTO revision_plans(student_id,plan_json) VALUES(?,?)",
                  (student_id, json.dumps(plan)))
    conn2.commit(); conn2.close()
    return plan

@router.get("/plan/{student_id}/latest")
def latest_plan(student_id: int):
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT plan_json FROM revision_plans WHERE student_id=? ORDER BY created_at DESC LIMIT 1", (student_id,))
    r = c.fetchone(); conn.close()
    if not r: raise HTTPException(404, "No plan yet")
    return json.loads(r["plan_json"])

# ── STUDY MATERIALS ─────────────────────────────────────────
@router.get("/materials")
def materials(exam: str, subject: str, topic: str):
    mats = get_study_materials(subject, topic, exam)
    return mats

# ── PROGRESS ────────────────────────────────────────────────
class ProgressIn(BaseModel):
    student_id: int; date: str; subject: str; score: float; notes: str = ""

@router.post("/progress")
def log_progress(d: ProgressIn):
    conn = get_conn()
    conn.execute("""INSERT INTO daily_progress(student_id,date,subject,score,notes) VALUES(?,?,?,?,?)
        ON CONFLICT(student_id,date,subject) DO UPDATE SET score=excluded.score,notes=excluded.notes""",
        (d.student_id, d.date, d.subject, d.score, d.notes))
    conn.commit(); conn.close()
    return {"ok": True}

@router.get("/progress/{student_id}")
def get_progress(student_id: int):
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT * FROM daily_progress WHERE student_id=? ORDER BY date ASC", (student_id,))
    rows = [dict(r) for r in c.fetchall()]; conn.close()
    return rows
