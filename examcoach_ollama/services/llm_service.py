"""
services/llm_service.py
ALL AI calls go through local Ollama — no OpenAI, no Gemini, no internet required.
Ollama must be running:  ollama serve
Model must be pulled:    ollama pull llama3.2   (or mistral, gemma2, etc.)
"""
import json
import re
import requests
import os

OLLAMA_URL   = os.getenv("OLLAMA_URL",   "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")   # change to any model you have pulled


# ── INTERNAL HELPERS ──────────────────────────────────────────────────────────

def _ollama_chat(prompt: str, temperature: float = 0.3) -> str:
    """Send a prompt to Ollama and return the response text."""
    try:
        resp = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json={
                "model":  OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False,
                "options": {"temperature": temperature},
            },
            timeout=120,   # 2-minute timeout — enough for local models
        )
        resp.raise_for_status()
        return resp.json().get("response", "")
    except requests.exceptions.ConnectionError:
        raise RuntimeError(
            f"Cannot reach Ollama at {OLLAMA_URL}. "
            "Make sure Ollama is running:  ollama serve"
        )
    except requests.exceptions.Timeout:
        raise RuntimeError("Ollama took too long to respond. Try a smaller/faster model.")


def _extract_json(text: str):
    """Extract JSON from model response even if wrapped in markdown fences."""
    # Remove markdown code fences
    clean = re.sub(r"```(?:json)?|```", "", text).strip()
    # Find first { or [ and last } or ]
    start = min(
        (clean.find("{") if clean.find("{") != -1 else len(clean)),
        (clean.find("[") if clean.find("[") != -1 else len(clean)),
    )
    end = max(clean.rfind("}"), clean.rfind("]"))
    if start == len(clean) or end == -1:
        raise ValueError(f"No JSON found in model response:\n{text[:300]}")
    return json.loads(clean[start:end+1])


def _safe_call(prompt: str, fallback, temperature: float = 0.3):
    """Call Ollama and parse JSON. Returns fallback on any error."""
    try:
        text = _ollama_chat(prompt, temperature)
        return _extract_json(text)
    except Exception as e:
        print(f"[llm_service] Ollama error: {e}")
        return fallback


# ── PUBLIC FUNCTIONS ──────────────────────────────────────────────────────────

def analyze_quiz_results(student_name: str, exam: str, answers: list) -> dict:
    """Analyze quiz answers using Ollama. Returns coaching feedback JSON."""
    wrong = [a for a in answers if not a.get("is_correct")]

    if not wrong:
        return {
            "weak_topics": [],
            "error_patterns": ["No errors — perfect score!"],
            "coaching_tips": ["Great job! Keep practicing to maintain your accuracy."],
            "summary": f"Excellent work {student_name}! You got everything correct. Keep it up!",
            "predicted_rank_improvement": "Strong performance — maintain consistency",
        }

    prompt = f"""You are an expert {exam} exam coach analyzing quiz performance for student {student_name}.

Wrong answers (JSON):
{json.dumps(wrong, indent=2)}

Analyze the mistakes and return ONLY a JSON object (no explanation, no markdown):
{{
  "weak_topics": [
    {{"subject": "Physics", "topic": "Kinematics", "error_count": 2, "root_cause": "sign convention confusion", "priority": "high"}}
  ],
  "error_patterns": ["List 2-3 recurring mistake patterns"],
  "coaching_tips": ["Tip 1: specific action", "Tip 2: specific action", "Tip 3: specific action"],
  "summary": "2-3 encouraging sentences addressing {student_name} directly",
  "predicted_rank_improvement": "brief estimate like top 10% if improved"
}}

Return ONLY the JSON object. No text before or after."""

    fallback = {
        "weak_topics": [{"subject": w.get("subject","General"), "topic": w.get("topic","Mixed"),
                          "error_count": 1, "root_cause": "needs review", "priority": "medium"}
                        for w in wrong[:3]],
        "error_patterns": ["Some questions were answered incorrectly", "Review the flagged topics"],
        "coaching_tips": ["Review your wrong answers carefully",
                          "Focus on the topics listed as weak",
                          "Practice similar questions daily"],
        "summary": f"Keep going {student_name}! You got {len(answers)-len(wrong)}/{len(answers)} correct. Review the weak topics and you'll improve quickly.",
        "predicted_rank_improvement": "Consistent practice will improve your rank",
    }
    return _safe_call(prompt, fallback, temperature=0.3)


def generate_revision_plan(student_name: str, exam: str, weak_topics: list) -> dict:
    """Generate a 7-day revision plan using Ollama."""
    prompt = f"""Create a 7-day study revision plan for {student_name} preparing for {exam}.
Weak topics that need focus: {json.dumps(weak_topics, indent=2)}

Return ONLY a JSON object (no markdown, no explanation):
{{
  "student": "{student_name}",
  "exam": "{exam}",
  "weekly_goal": "one sentence goal",
  "motivational_quote": "an inspiring quote",
  "plan": [
    {{
      "day": 1,
      "theme": "Day theme",
      "daily_quote": "short motivational quote",
      "sessions": [
        {{
          "slot": "Morning",
          "subject": "Physics",
          "topic": "Kinematics",
          "duration_min": 60,
          "activities": ["Read chapter summary", "Solve 10 practice problems"],
          "tip": "Focus on sign conventions"
        }},
        {{
          "slot": "Afternoon",
          "subject": "Chemistry",
          "topic": "Mole Concept",
          "duration_min": 60,
          "activities": ["Practice calculations"],
          "tip": "Write formulas before solving"
        }},
        {{
          "slot": "Evening",
          "subject": "Mathematics",
          "topic": "Algebra",
          "duration_min": 45,
          "activities": ["Revision and self-test"],
          "tip": "Review mistakes"
        }}
      ]
    }}
  ]
}}

Create exactly 7 days. Day 7 must be a full mock test day.
Return ONLY the JSON. No text before or after."""

    fallback = {
        "student": student_name,
        "exam": exam,
        "weekly_goal": f"Master weak topics and improve {exam} score by 15%",
        "motivational_quote": "Success is the sum of small efforts repeated daily.",
        "plan": [
            {
                "day": d,
                "theme": "Mock Test" if d == 7 else f"Day {d} — Focus Study",
                "daily_quote": "Keep pushing forward!",
                "sessions": [
                    {"slot": "Morning", "subject": weak_topics[0]["subject"] if weak_topics else "Core Subject",
                     "topic": weak_topics[0]["topic"] if weak_topics else "Review",
                     "duration_min": 60, "activities": ["Study and practice"], "tip": "Be consistent"},
                    {"slot": "Afternoon", "subject": "Practice",
                     "topic": "Mixed Questions", "duration_min": 60,
                     "activities": ["Solve past papers"], "tip": "Time yourself"},
                    {"slot": "Evening", "subject": "Revision",
                     "topic": "Daily Recap", "duration_min": 30,
                     "activities": ["Review mistakes"], "tip": "Write down errors"},
                ]
            }
            for d in range(1, 8)
        ]
    }
    return _safe_call(prompt, fallback, temperature=0.5)


def get_study_materials(subject: str, topic: str, exam: str) -> list:
    """Get study material recommendations using Ollama."""
    prompt = f"""Recommend 4 study resources for exam: {exam}, subject: {subject}, topic: {topic}.

Return ONLY a JSON array (no markdown):
[
  {{
    "title": "Resource title",
    "type": "video",
    "description": "1-2 sentence description of what this covers",
    "url": "https://www.youtube.com/results?search_query={exam}+{subject}+{topic}",
    "difficulty": "beginner",
    "time_min": 30
  }}
]

Include exactly 4 items. Types must be one of: video, article, practice, book.
Difficulty must be: beginner, intermediate, or advanced.
Return ONLY the JSON array."""

    fallback = [
        {"title": f"{topic} — Video Lecture ({exam})", "type": "video",
         "description": f"Comprehensive video covering {topic} for {exam} preparation.",
         "url": f"https://www.youtube.com/results?search_query={exam}+{subject}+{topic}+lecture",
         "difficulty": "beginner", "time_min": 45},
        {"title": f"{topic} — Practice Problems", "type": "practice",
         "description": f"Curated {topic} practice questions with step-by-step solutions.",
         "url": f"https://www.khanacademy.org/search?page_search_query={topic}",
         "difficulty": "intermediate", "time_min": 60},
        {"title": f"{topic} — Concept Notes", "type": "article",
         "description": f"Clear written explanation of {topic} concepts and formulas.",
         "url": f"https://www.toppr.com/guides/{subject.lower()}/{topic.lower().replace(' ','-')}/",
         "difficulty": "beginner", "time_min": 20},
        {"title": f"{subject} Reference Book ({exam})", "type": "book",
         "description": f"Standard reference book covering {subject} topics for {exam}.",
         "url": f"https://www.amazon.in/s?k={exam}+{subject}+book",
         "difficulty": "advanced", "time_min": 120},
    ]
    return _safe_call(prompt, fallback, temperature=0.4)


def get_ai_hint(question_text: str, subject: str, topic: str, exam: str) -> str:
    """Get a conceptual hint for a quiz question using Ollama."""
    prompt = f"""You are an {exam} exam tutor. Give a SHORT conceptual hint (2-3 sentences) for this question.
Do NOT reveal the answer directly — give a conceptual nudge only.

Subject: {subject}
Topic: {topic}
Question: {question_text}

Reply with ONLY the hint text, no labels or prefixes."""

    try:
        hint = _ollama_chat(prompt, temperature=0.4)
        # Clean up any prefixes the model might add
        hint = re.sub(r"^(hint|answer|tip|note)\s*:\s*", "", hint, flags=re.IGNORECASE).strip()
        return hint[:400] if hint else "Think about the fundamental concept behind this topic."
    except Exception as e:
        return f"Think carefully about the core concept of {topic}. Review your {subject} notes."
