"""
models.py — SQLAlchemy ORM models.
Base.metadata.create_all(bind=engine) in main.py creates all tables.
"""
from sqlalchemy import Column, Integer, String, Float, Text, DateTime, UniqueConstraint, ForeignKey
from sqlalchemy.sql import func
from database import Base


class Student(Base):
    __tablename__ = "students"
    id           = Column(Integer, primary_key=True, index=True)
    name         = Column(String, nullable=False)
    email        = Column(String, unique=True, nullable=False, index=True)
    exam_target  = Column(String, nullable=False)
    created_at   = Column(DateTime, server_default=func.now())


class QuizSession(Base):
    __tablename__ = "quiz_sessions"
    id              = Column(Integer, primary_key=True, index=True)
    student_id      = Column(Integer, ForeignKey("students.id"))
    exam            = Column(String, nullable=False)
    subject         = Column(String)
    total_questions = Column(Integer)
    correct         = Column(Integer)
    score_pct       = Column(Float)
    time_taken      = Column(Integer)
    completed_at    = Column(DateTime, server_default=func.now())


class QuizAnswer(Base):
    __tablename__ = "quiz_answers"
    id             = Column(Integer, primary_key=True, index=True)
    session_id     = Column(Integer, ForeignKey("quiz_sessions.id"))
    question_id    = Column(String)
    subject        = Column(String)
    topic          = Column(String)
    selected       = Column(String)
    correct_answer = Column(String)
    is_correct     = Column(Integer)
    time_spent     = Column(Integer, default=0)


class WeakTopic(Base):
    __tablename__ = "weak_topics"
    __table_args__ = (UniqueConstraint("student_id", "subject", "topic"),)
    id         = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    subject    = Column(String)
    topic      = Column(String)
    accuracy   = Column(Float)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class RevisionPlan(Base):
    __tablename__ = "revision_plans"
    id         = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    plan_json  = Column(Text)
    created_at = Column(DateTime, server_default=func.now())


class DailyProgress(Base):
    __tablename__ = "daily_progress"
    __table_args__ = (UniqueConstraint("student_id", "date", "subject"),)
    id         = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    date       = Column(String)
    subject    = Column(String)
    score      = Column(Float)
    notes      = Column(String, default="")
