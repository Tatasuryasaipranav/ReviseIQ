"""
routes/api.py — All REST endpoints
- Pure SQLAlchemy (no psycopg2)
- Ollama for all AI (local, no API keys)
- Quiz submit saves to DB FIRST, then calls AI (never blocks on AI)
- Full recording: quiz_sessions + quiz_answers + weak_topics updated every time
"""
from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from sqlalchemy import text
from database import get_db
from services.llm_service import (
    analyze_quiz_results, generate_revision_plan,
    get_study_materials, get_ai_hint,
)
from services.analytics import update_weak_topics, get_dashboard
from questions.question_bank import (
    get_questions_by_exam, get_questions_by_subject,
    get_all_exams, get_subjects_for_exam, get_topics_for_subject,
)
import json
import random

router = APIRouter()


# ── OLLAMA STATUS ─────────────────────────────────────────────────────────────

@router.get("/ollama/status")
def ollama_status():
    """Check if Ollama is reachable and which model is active."""
    import requests as req_lib
    import os
    url  = os.getenv("OLLAMA_URL", "http://localhost:11434")
    model = os.getenv("OLLAMA_MODEL", "llama3.2")
    try:
        r = req_lib.get(f"{url}/api/tags", timeout=3)
        models = [m["name"] for m in r.json().get("models", [])]
        return {"status": "online", "active_model": model, "available_models": models}
    except Exception as e:
        return {"status": "offline", "error": str(e), "fix": "Run: ollama serve"}


# ── STUDENTS ──────────────────────────────────────────────────────────────────

class StudentIn(BaseModel):
    name: str
    email: EmailStr
    exam_target: str


@router.post("/students")
def create_student(d: StudentIn, db: Session = Depends(get_db)):
    try:
        result = db.execute(
            text("INSERT INTO students(name,email,exam_target) VALUES(:name,:email,:exam_target) RETURNING id"),
            {"name": d.name, "email": d.email, "exam_target": d.exam_target},
        )
        db.commit()
        sid = result.fetchone()[0]
        return {"id": sid, "name": d.name, "exam_target": d.exam_target}
    except Exception as e:
        db.rollback()
        raise HTTPException(400, str(e))


@router.get("/students/{sid}")
def get_student(sid: int, db: Session = Depends(get_db)):
    row = db.execute(text("SELECT * FROM students WHERE id=:id"), {"id": sid}).mappings().fetchone()
    if not row:
        raise HTTPException(404, "Student not found")
    return dict(row)


@router.get("/students/by-email/{email}")
def get_by_email(email: str, db: Session = Depends(get_db)):
    row = db.execute(text("SELECT * FROM students WHERE email=:email"), {"email": email}).mappings().fetchone()
    if not row:
        raise HTTPException(404, "Student not found")
    return dict(row)


# ── QUESTIONS ─────────────────────────────────────────────────────────────────

@router.get("/questions/exams")
def list_exams():
    return get_all_exams()


@router.get("/questions/{exam}")
def get_quiz_questions(exam: str, subject: str = None, count: int = 10):
    qs = get_questions_by_subject(exam, subject) if subject else get_questions_by_exam(exam)
    random.shuffle(qs)
    return qs[:count]


@router.get("/questions/{exam}/subjects")
def get_subjects(exam: str):
    return get_subjects_for_exam(exam)


@router.get("/hint")
def get_hint(question_id: str, exam: str, subject: str, topic: str, question_text: str):
    try:
        hint = get_ai_hint(question_text, subject, topic, exam)
        return {"hint": hint}
    except Exception as e:
        return {"hint": f"Think about the core concept of {topic}. Review your notes carefully."}


# ── QUIZ SESSION ──────────────────────────────────────────────────────────────

class AnswerItem(BaseModel):
    question_id: str
    subject: str
    topic: str
    selected: str
    correct_answer: str
    is_correct: bool
    time_spent: int = 0


class SessionSubmit(BaseModel):
    student_id: int
    exam: str
    subject: str | None = None
    answers: list[AnswerItem]
    time_taken: int = 0


@router.post("/quiz/submit")
def submit_quiz(d: SessionSubmit, db: Session = Depends(get_db)):
    """
    STEP 1: Save quiz to DB immediately (fast)
    STEP 2: Update weak_topics (DB query, fast)
    STEP 3: Call Ollama for AI analysis (may take 5-20s)
    Always returns full result — AI failure never loses quiz data.
    """
    correct = sum(1 for a in d.answers if a.is_correct)
    total   = len(d.answers)
    score   = round(correct / total * 100, 1) if total else 0.0

    # ── STEP 1: Save quiz session ─────────────────────────────────────────
    result = db.execute(
        text("""INSERT INTO quiz_sessions
                    (student_id, exam, subject, total_questions, correct, score_pct, time_taken)
                VALUES (:student_id, :exam, :subject, :total, :correct, :score, :time_taken)
                RETURNING id"""),
        {"student_id": d.student_id, "exam": d.exam, "subject": d.subject,
         "total": total, "correct": correct, "score": score, "time_taken": d.time_taken},
    )
    session_id = result.fetchone()[0]

    # ── STEP 2: Save every individual answer ──────────────────────────────
    for a in d.answers:
        db.execute(
            text("""INSERT INTO quiz_answers
                        (session_id, question_id, subject, topic,
                         selected, correct_answer, is_correct, time_spent)
                    VALUES (:session_id, :question_id, :subject, :topic,
                            :selected, :correct_answer, :is_correct, :time_spent)"""),
            {"session_id": session_id, "question_id": a.question_id,
             "subject": a.subject, "topic": a.topic,
             "selected": a.selected, "correct_answer": a.correct_answer,
             "is_correct": 1 if a.is_correct else 0, "time_spent": a.time_spent},
        )
    db.commit()   # ← DB saved. Even if AI fails, quiz is permanently recorded.

    # ── STEP 3: Update weak_topics analytics (fast SQL aggregation) ───────
    weak = update_weak_topics(d.student_id, db)

    # ── STEP 4: Get student name ──────────────────────────────────────────
    row   = db.execute(text("SELECT name FROM students WHERE id=:id"), {"id": d.student_id}).fetchone()
    sname = row[0] if row else "Student"

    # ── STEP 5: AI analysis via Ollama (graceful fallback on failure) ─────
    try:
        analysis = analyze_quiz_results(sname, d.exam, [a.model_dump() for a in d.answers])
    except Exception as e:
        analysis = {
            "summary": f"Good effort {sname}! You scored {score}%. Review your weak topics below.",
            "weak_topics": weak,
            "error_patterns": ["Check the flagged topics"],
            "coaching_tips": [
                "Review all wrong answers in the session review below",
                "Focus daily practice on your lowest-accuracy topics",
                "Take another quiz on weak subjects to build confidence",
            ],
            "predicted_rank_improvement": "Consistent practice leads to rank improvement",
            "ai_note": f"Ollama unavailable ({str(e)[:80]}). Make sure Ollama is running: ollama serve",
        }

    return {
        "session_id":         session_id,
        "score":              score,
        "correct":            correct,
        "total":              total,
        "analysis":           analysis,
        "weak_topics_updated": weak,
    }


@router.get("/quiz/history/{student_id}")
def quiz_history(student_id: int, db: Session = Depends(get_db)):
    rows = db.execute(
        text("SELECT * FROM quiz_sessions WHERE student_id=:sid ORDER BY completed_at DESC"),
        {"sid": student_id},
    ).mappings().fetchall()
    return [dict(r) for r in rows]


@router.get("/quiz/session/{session_id}/answers")
def session_answers(session_id: int, db: Session = Depends(get_db)):
    rows = db.execute(
        text("SELECT * FROM quiz_answers WHERE session_id=:sid"),
        {"sid": session_id},
    ).mappings().fetchall()
    return [dict(r) for r in rows]


# ── DASHBOARD ─────────────────────────────────────────────────────────────────

@router.get("/dashboard/{student_id}")
def dashboard(student_id: int, db: Session = Depends(get_db)):
    return get_dashboard(student_id, db)


@router.get("/dashboard/{student_id}/weak-topics")
def weak_topics_endpoint(student_id: int, db: Session = Depends(get_db)):
    rows = db.execute(
        text("SELECT * FROM weak_topics WHERE student_id=:sid ORDER BY accuracy ASC"),
        {"sid": student_id},
    ).mappings().fetchall()
    return [dict(r) for r in rows]


# ── REVISION PLAN ─────────────────────────────────────────────────────────────

@router.post("/plan/{student_id}/generate")
def gen_plan(student_id: int, db: Session = Depends(get_db)):
    student = db.execute(
        text("SELECT * FROM students WHERE id=:id"), {"id": student_id}
    ).mappings().fetchone()
    if not student:
        raise HTTPException(404, "Student not found")

    weak_rows = db.execute(
        text("SELECT subject, topic, accuracy FROM weak_topics WHERE student_id=:sid ORDER BY accuracy ASC LIMIT 8"),
        {"sid": student_id},
    ).mappings().fetchall()
    weak = [dict(r) for r in weak_rows]

    if not weak:
        raise HTTPException(400, "Complete at least one quiz first to generate your revision plan!")

    plan = generate_revision_plan(student["name"], student["exam_target"], weak)
    db.execute(
        text("INSERT INTO revision_plans(student_id, plan_json) VALUES(:sid, :plan)"),
        {"sid": student_id, "plan": json.dumps(plan)},
    )
    db.commit()
    return plan


@router.get("/plan/{student_id}/latest")
def latest_plan(student_id: int, db: Session = Depends(get_db)):
    row = db.execute(
        text("SELECT plan_json FROM revision_plans WHERE student_id=:sid ORDER BY created_at DESC LIMIT 1"),
        {"sid": student_id},
    ).fetchone()
    if not row:
        raise HTTPException(404, "No plan yet — complete a quiz first!")
    return json.loads(row[0])


# ── STUDY MATERIALS ───────────────────────────────────────────────────────────

@router.get("/materials")
def materials(exam: str, subject: str, topic: str):
    try:
        return get_study_materials(subject, topic, exam)
    except Exception as e:
        return [
            {"title": f"{topic} on YouTube", "type": "video",
             "description": f"Search YouTube for {exam} {subject} {topic} lectures.",
             "url": f"https://www.youtube.com/results?search_query={exam}+{subject}+{topic}",
             "difficulty": "beginner", "time_min": 30},
        ]


# ── PROGRESS ──────────────────────────────────────────────────────────────────

class ProgressIn(BaseModel):
    student_id: int
    date: str
    subject: str
    score: float
    notes: str = ""


@router.post("/progress")
def log_progress(d: ProgressIn, db: Session = Depends(get_db)):
    db.execute(
        text("""INSERT INTO daily_progress(student_id, date, subject, score, notes)
                VALUES (:student_id, :date, :subject, :score, :notes)
                ON CONFLICT(student_id, date, subject)
                DO UPDATE SET score=EXCLUDED.score, notes=EXCLUDED.notes"""),
        {"student_id": d.student_id, "date": d.date, "subject": d.subject,
         "score": d.score, "notes": d.notes},
    )
    db.commit()
    return {"ok": True}


@router.get("/progress/{student_id}")
def get_progress(student_id: int, db: Session = Depends(get_db)):
    rows = db.execute(
        text("SELECT * FROM daily_progress WHERE student_id=:sid ORDER BY date ASC"),
        {"sid": student_id},
    ).mappings().fetchall()
    return [dict(r) for r in rows]
