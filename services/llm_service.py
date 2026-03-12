"""services/llm_service.py — Ollama local LLM calls (replaces OpenAI + Gemini)"""
import json, re, requests
from config import OLLAMA_BASE_URL, OLLAMA_MODEL


def _chat(prompt: str, temperature: float = 0.3, max_tokens: int = 2048) -> str:
    """Send a prompt to Ollama and return the response text."""
    url = f"{OLLAMA_BASE_URL}/api/chat"
    payload = {
        "model": OLLAMA_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "stream": False,
        "options": {
            "temperature": temperature,
            "num_predict": max_tokens,
        },
    }
    try:
        r = requests.post(url, json=payload, timeout=120)
        r.raise_for_status()
        return r.json()["message"]["content"]
    except requests.exceptions.ConnectionError:
        raise RuntimeError(
            f"Cannot connect to Ollama at {OLLAMA_BASE_URL}.\n"
            "Make sure Ollama is running:  ollama serve\n"
            f"And the model is pulled:     ollama pull {OLLAMA_MODEL}"
        )


def _clean_json(text: str):
    """Strip markdown fences and parse JSON."""
    cleaned = re.sub(r"```(?:json)?|```", "", text).strip()
    match = re.search(r"(\{.*\}|\[.*\])", cleaned, re.DOTALL)
    if match:
        cleaned = match.group(1)
    return json.loads(cleaned)


def analyze_quiz_results(student_name, exam, answers: list) -> dict:
    wrong = [a for a in answers if not a.get("is_correct")]
    prompt = f"""You are an expert {exam} coach analyzing quiz performance for {student_name}.

Wrong answers: {json.dumps(wrong, indent=2)}

Return ONLY valid JSON with this exact structure (no extra text, no markdown):
{{
  "weak_topics": [{{"subject":"","topic":"","error_count":0,"root_cause":"","priority":"high|medium|low"}}],
  "error_patterns": ["..."],
  "coaching_tips": ["tip1", "tip2", "tip3"],
  "summary": "2-3 sentence encouraging coaching summary",
  "predicted_rank_improvement": "string estimate"
}}"""
    return _clean_json(_chat(prompt, temperature=0.3))


def generate_revision_plan(student_name, exam, weak_topics: list) -> dict:
    prompt = f"""Create a detailed 7-day revision plan for {student_name} preparing for {exam}.
Weak topics to address: {json.dumps(weak_topics, indent=2)}

Return ONLY valid JSON (no extra text, no markdown):
{{
  "student": "{student_name}", "exam": "{exam}",
  "weekly_goal": "string",
  "motivational_quote": "string",
  "plan": [{{
    "day": 1, "theme": "string",
    "sessions": [{{"slot":"Morning|Afternoon|Evening","subject":"","topic":"","duration_min":60,
                   "activities":["..."],"tip":"short tip"}}],
    "daily_quote": "short motivational quote"
  }}]
}}
Day 7 = full mock test simulation. Return ONLY valid JSON."""
    return _clean_json(_chat(prompt, temperature=0.5))


def get_study_materials(subject, topic, exam) -> list:
    prompt = f"""Recommend 4 study resources for {exam} — {subject} — {topic}.
Return ONLY a valid JSON array (no extra text, no markdown), each item:
{{"title":"","type":"video|article|practice|book","description":"1-2 sentences","url":"realistic URL","difficulty":"beginner|intermediate|advanced","time_min":30}}"""
    return _clean_json(_chat(prompt, temperature=0.4))


def get_ai_hint(question_text, subject, topic, exam) -> str:
    prompt = f"""Give a SHORT conceptual hint (2-3 sentences) for this {exam} {subject} question on topic '{topic}'.
Question: {question_text}
Do NOT give the answer directly — give a conceptual nudge only."""
    return _chat(prompt, temperature=0.4, max_tokens=200).strip()
