"""
config.py — Central configuration (Ollama edition)
No API keys needed — runs 100% locally via Ollama.
"""
import os
from dotenv import load_dotenv
load_dotenv()

# --- Ollama settings ---
# Make sure Ollama is running: `ollama serve`
# Pull a model first:         `ollama pull llama3`
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL    = os.getenv("OLLAMA_MODEL", "llama3")   # or mistral, phi3, gemma2, etc.

# --- Database (SQLite — no setup needed) ---
DATABASE_PATH   = os.getenv("DATABASE_PATH", "examcoach.db")

# --- Thresholds ---
WEAK_THRESHOLD  = 60   # % below which topic is weak
PLAN_DAYS       = 7
