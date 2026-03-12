#!/bin/bash
echo "================================================"
echo "  ExamCoach - Ollama Edition (100% Local AI)"
echo "================================================"
echo ""
echo "Make sure Ollama is running: ollama serve"
echo "Pull model if needed:        ollama pull llama3"
echo ""
pip install -r requirements.txt
python main.py
