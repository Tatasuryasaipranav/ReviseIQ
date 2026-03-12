"""services/analytics.py"""
from database import get_conn

def update_weak_topics(student_id):
    conn = get_conn()
    c = conn.cursor()
    c.execute("""
        SELECT qa.subject, qa.topic,
               COUNT(*) as total, SUM(qa.is_correct) as correct
        FROM quiz_answers qa
        JOIN quiz_sessions qs ON qs.id = qa.session_id
        WHERE qs.student_id=? GROUP BY qa.subject, qa.topic
    """, (student_id,))
    rows = c.fetchall()
    weak = []
    for r in rows:
        acc = (r["correct"] or 0) / r["total"]
        c.execute("""INSERT INTO weak_topics(student_id,subject,topic,accuracy)
            VALUES(?,?,?,?) ON CONFLICT(student_id,subject,topic)
            DO UPDATE SET accuracy=excluded.accuracy, updated_at=CURRENT_TIMESTAMP
        """, (student_id, r["subject"], r["topic"], acc))
        if acc * 100 < 60:
            weak.append({"subject":r["subject"],"topic":r["topic"],"accuracy":round(acc,3)})
    conn.commit(); conn.close()
    return weak

def get_dashboard(student_id):
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT COUNT(*) as cnt FROM quiz_sessions WHERE student_id=?", (student_id,))
    total_tests = c.fetchone()["cnt"]
    c.execute("SELECT AVG(score_pct) as avg FROM quiz_sessions WHERE student_id=?", (student_id,))
    avg_score = round(c.fetchone()["avg"] or 0, 1)
    c.execute("SELECT COUNT(*) as cnt FROM weak_topics WHERE student_id=?", (student_id,))
    weak_count = c.fetchone()["cnt"]
    c.execute("""SELECT subject, ROUND(AVG(score_pct)*100)/100 as avg
        FROM quiz_sessions WHERE student_id=? GROUP BY subject ORDER BY avg DESC LIMIT 1""", (student_id,))
    best = c.fetchone()
    c.execute("""SELECT subject, ROUND(AVG(is_correct)*100,1) as acc
        FROM quiz_answers qa JOIN quiz_sessions qs ON qs.id=qa.session_id
        WHERE qs.student_id=? GROUP BY subject""", (student_id,))
    subject_acc = {r["subject"]: r["acc"] for r in c.fetchall()}
    c.execute("""SELECT qs.completed_at as date, qs.subject, qs.score_pct as score
        FROM quiz_sessions qs WHERE qs.student_id=? ORDER BY date ASC""", (student_id,))
    trend = [dict(r) for r in c.fetchall()]
    c.execute("SELECT subject,topic,accuracy FROM weak_topics WHERE student_id=? ORDER BY accuracy ASC LIMIT 8", (student_id,))
    weak_topics = [dict(r) for r in c.fetchall()]
    conn.close()
    return {"total_tests":total_tests,"avg_score":avg_score,"weak_count":weak_count,
            "best_subject":dict(best) if best else {},"subject_accuracy":subject_acc,
            "trend":trend,"weak_topics":weak_topics}
