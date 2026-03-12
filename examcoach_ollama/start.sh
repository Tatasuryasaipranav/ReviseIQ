#!/bin/bash
echo ""
echo "╔══════════════════════════════════════╗"
echo "║     🎓 ExamCoach - AI Exam Prep      ║"
echo "╚══════════════════════════════════════╝"
echo ""
echo "[1/2] Installing dependencies..."
pip install -r requirements.txt --quiet
echo "[2/2] Starting server..."
echo ""
echo "✅ Open your browser at: http://localhost:8000"
echo ""
python main.py
