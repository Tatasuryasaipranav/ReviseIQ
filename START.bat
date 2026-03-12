@echo off
echo ================================================
echo   ExamCoach - Ollama Edition (100% Local AI)
echo ================================================
echo.
echo Step 1: Make sure Ollama is running
echo   Download from: https://ollama.com
echo   Then run: ollama serve
echo   Pull model: ollama pull llama3
echo.
echo Step 2: Starting ExamCoach...
echo.
pip install -r requirements.txt
python main.py
pause
