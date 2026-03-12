# ExamCoach — Ollama AI Edition

## ✅ What Changed (vs OpenAI version)
- **ALL AI now runs locally via Ollama** — no OpenAI key, no Gemini key, no internet needed for AI
- Quiz results save to Supabase DB immediately (AI analysis comes after, never blocks save)
- Dashboard shows both API status AND Ollama AI status in real time
- If Ollama is offline, quiz still saves and you get smart fallback feedback

---

## 🚀 Quick Start

### 1. Install Ollama
Download from: https://ollama.com/download  
Install and run it.

### 2. Pull a model (one-time setup)
Open a terminal and run ONE of these:
```
ollama pull llama3.2      ← recommended (fast + smart)
ollama pull mistral       ← alternative (very fast)
ollama pull phi3          ← smallest (runs on low-RAM machines)
ollama pull gemma2        ← Google's model
```

### 3. Start Ollama (keep this running)
```
ollama serve
```

### 4. Start ExamCoach (separate terminal)
```
pip install -r requirements.txt
uvicorn main:app --reload
```

### 5. Open browser
```
http://localhost:8000
```

---

## 🔧 Change the AI Model
Edit `.env` and change `OLLAMA_MODEL`:
```
OLLAMA_MODEL=mistral
```
Then restart the server.

---

## 📊 What Gets Recorded After Every Quiz
1. **quiz_sessions** — exam, subject, score%, total questions, time taken
2. **quiz_answers** — every individual answer with correct/wrong, time spent
3. **weak_topics** — accuracy per topic updated automatically (used for dashboard + revision plan)
4. **Dashboard** — updates immediately after quiz
5. **History page** — shows all past quiz sessions
6. **Revision Plan** — uses updated weak topics to generate AI plan

---

## ⚡ Performance Tips
- `phi3` or `mistral` are fastest for low-RAM machines (8GB)
- `llama3.2` is best balance of speed + quality
- AI hint and analysis take 5-20 seconds depending on model + hardware
- Quiz save to DB is instant (< 1 second) regardless of AI speed

---

## 🐛 Troubleshooting

| Error | Fix |
|-------|-----|
| "Cannot reach Ollama" | Run `ollama serve` in a terminal |
| "AI Offline" badge in app | Ollama not running — run `ollama serve` |
| Quiz saves but no AI analysis | Ollama running but slow — wait 20-30s |
| "localhost not responding" | Run `uvicorn main:app --reload` |
| DB connection error | Check `.env` DATABASE_URL is correct |
