📚 AI Study Buddy Agent

## 🚀 Overview
An AI-powered learning assistant built with Python, Streamlit, and Ollama.
The Study Buddy helps students learn topics, explains concepts in simple terms, generates quizzes, evaluates answers, tracks weak areas, and suggests personalized revision schedules.

🚀 Features
✏️ Add Topics – Enter topics you want to study.
📖 Explain Concepts – AI explains in simple, easy-to-understand terms.
📝 Generate Quizzes – Get 3 MCQs per topic with answer options.
✅ Evaluate Answers – AI checks if answers are correct or wrong and explains mistakes.
📊 Track Weak Areas – Identifies difficult topics based on quiz performance.
📅 Revision Plan – Suggests a 3-day structured revision schedule.

## 🛠️ Tech Stack
Python 3.9+
Streamlit – Interactive UI
Ollama – Local AI model inference (default: llama3)

## ⚡ Setup Instructions 
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
2. Install Ollama and run a model (e.g. llama3): `ollama run llama3`
3. Start the app: `streamlit run app.py`