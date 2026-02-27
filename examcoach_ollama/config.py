"""
config.py — Central configuration (Ollama version)
All AI runs locally via Ollama — no OpenAI or Gemini keys needed.
"""
import os
from dotenv import load_dotenv
load_dotenv()

# Ollama settings (local AI — free, no API key needed)
OLLAMA_URL   = os.getenv("OLLAMA_URL",   "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")

# Legacy keys — no longer used, kept to avoid import errors
OPENAI_API_KEY = ""
GEMINI_API_KEY = ""
OPENAI_MODEL   = OLLAMA_MODEL
GEMINI_MODEL   = OLLAMA_MODEL

WEAK_THRESHOLD = 60    # % below which topic is "weak"
PLAN_DAYS      = 7
