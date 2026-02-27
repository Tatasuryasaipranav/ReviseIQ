@echo off
title ExamCoach — Ollama AI Edition
color 0A

echo ============================================================
echo   ExamCoach — AI Exam Preparation (Ollama Edition)
echo ============================================================
echo.
echo STEP 1: Make sure Ollama is installed and running
echo   Download: https://ollama.com/download
echo   Then run in a SEPARATE terminal: ollama serve
echo.
echo STEP 2: Pull the AI model (first time only)
echo   ollama pull llama3.2
echo.
echo   Other fast models you can use:
echo   ollama pull mistral
echo   ollama pull phi3
echo   ollama pull gemma2
echo.
echo STEP 3: Starting ExamCoach backend...
echo ============================================================
echo.

cd /d "%~dp0"

echo Installing dependencies...
pip install -r requirements.txt

echo.
echo Starting server at http://localhost:8000
echo Press CTRL+C to stop.
echo.

uvicorn main:app --reload --host 0.0.0.0 --port 8000
pause
