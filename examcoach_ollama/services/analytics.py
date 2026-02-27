"""services/analytics.py — Pure SQLAlchemy, no psycopg2"""
from sqlalchemy.orm import Session
from sqlalchemy import text


def update_weak_topics(student_id: int, db: Session) -> list:
    rows = db.execute(
        text("""
            SELECT qa.subject, qa.topic,
                   COUNT(*)          AS total,
                   SUM(qa.is_correct) AS correct
            FROM quiz_answers qa
            JOIN quiz_sessions qs ON qs.id = qa.session_id
            WHERE qs.student_id = :sid
            GROUP BY qa.subject, qa.topic
        """),
        {"sid": student_id},
    ).fetchall()

    weak = []
    for r in rows:
        acc = (r.correct or 0) / r.total
        db.execute(
            text("""
                INSERT INTO weak_topics(student_id, subject, topic, accuracy)
                VALUES (:sid, :subject, :topic, :accuracy)
                ON CONFLICT(student_id, subject, topic)
                DO UPDATE SET accuracy = EXCLUDED.accuracy,
                              updated_at = CURRENT_TIMESTAMP
            """),
            {"sid": student_id, "subject": r.subject, "topic": r.topic, "accuracy": acc},
        )
        if acc * 100 < 60:
            weak.append({"subject": r.subject, "topic": r.topic, "accuracy": round(acc, 3)})

    db.commit()
    return weak


def get_dashboard(student_id: int, db: Session) -> dict:
    total_tests = db.execute(
        text("SELECT COUNT(*) FROM quiz_sessions WHERE student_id=:sid"),
        {"sid": student_id},
    ).scalar()

    avg_score = db.execute(
        text("SELECT AVG(score_pct) FROM quiz_sessions WHERE student_id=:sid"),
        {"sid": student_id},
    ).scalar()
    avg_score = round(avg_score or 0, 1)

    weak_count = db.execute(
        text("SELECT COUNT(*) FROM weak_topics WHERE student_id=:sid"),
        {"sid": student_id},
    ).scalar()

    best = db.execute(
        text("""SELECT subject, ROUND(AVG(score_pct)::numeric, 2) AS avg
                FROM quiz_sessions WHERE student_id=:sid
                GROUP BY subject ORDER BY avg DESC LIMIT 1"""),
        {"sid": student_id},
    ).mappings().fetchone()

    subject_rows = db.execute(
        text("""SELECT subject, ROUND(AVG(is_correct::numeric) * 100, 1) AS acc
                FROM quiz_answers qa
                JOIN quiz_sessions qs ON qs.id = qa.session_id
                WHERE qs.student_id = :sid
                GROUP BY subject"""),
        {"sid": student_id},
    ).fetchall()
    subject_acc = {r.subject: r.acc for r in subject_rows}

    trend_rows = db.execute(
        text("""SELECT completed_at AS date, subject, score_pct AS score
                FROM quiz_sessions WHERE student_id=:sid ORDER BY completed_at ASC"""),
        {"sid": student_id},
    ).mappings().fetchall()
    trend = [dict(r) for r in trend_rows]

    weak_rows = db.execute(
        text("SELECT subject, topic, accuracy FROM weak_topics WHERE student_id=:sid ORDER BY accuracy ASC LIMIT 8"),
        {"sid": student_id},
    ).mappings().fetchall()
    weak_topics = [dict(r) for r in weak_rows]

    return {
        "total_tests":     total_tests,
        "avg_score":       avg_score,
        "weak_count":      weak_count,
        "best_subject":    dict(best) if best else {},
        "subject_accuracy": subject_acc,
        "trend":           trend,
        "weak_topics":     weak_topics,
    }
