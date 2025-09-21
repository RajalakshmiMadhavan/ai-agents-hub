import streamlit as st
import requests
import json

# Ollama API helper
def query_ollama(prompt, model="llama3"):
    url = "http://localhost:11434/api/generate"
    response = requests.post(url, json={"model": model, "prompt": prompt, "stream": False})
    data = response.json()
    output = data.get("response", "⚠️ No response from model.")
    return output

# Initialize session state
if "topics" not in st.session_state:
    st.session_state.topics = []
if "quiz" not in st.session_state:
    st.session_state.quiz = []
if "answers" not in st.session_state:
    st.session_state.answers = {}
if "weak_areas" not in st.session_state:
    st.session_state.weak_areas = []

# App UI
st.title("📚 AI Study Buddy Agent")
st.write("Learn topics, take quizzes, and track weak areas with AI help.")

# Input topics
topic = st.text_input("Enter a topic you want to study:")
if st.button("Add Topic") and topic:
    st.session_state.topics.append(topic)

if st.session_state.topics:
    st.subheader("Your Topics")
    for t in st.session_state.topics:
        st.markdown(f"- {t}")

# Explain concepts
if st.button("Explain Topics"):
    for t in st.session_state.topics:
        st.subheader(f"📖 {t}")
        explanation = query_ollama(f"Explain {t} in simple terms for a student.")
        st.write(explanation)

# Generate quiz
if st.button("Generate Quiz"):
    st.session_state.quiz = []
    for t in st.session_state.topics:
        quiz_text = query_ollama(
            f"Generate 3 multiple-choice questions on {t}. "
            f"Output strictly in JSON format like this:\n"
            f"""{{
              "questions": [
                {{
                  "question": "What is photosynthesis?",
                  "options": ["A) Process by which plants make food", "B) Human digestion", "C) Water cycle", "D) Respiration"],
                  "answer": "A"
                }}
              ]
            }}"""
        )
        try:
            cleaned = quiz_text.strip().strip("`").replace("json", "").strip()
            cleaned = cleaned[cleaned.find("{"):]
            quiz_data = json.loads(cleaned)       # now parse
            for q in quiz_data["questions"]:
                st.session_state.quiz.append({"topic": t, **q})
        except Exception:
            st.error("❌ Failed to parse quiz. Try regenerating.")

# Display quiz
if st.session_state.quiz:
    st.subheader("📝 Quiz")
    for i, q in enumerate(st.session_state.quiz):
        st.markdown(f"**Q{i+1}: {q['question']}**")
        for opt in q["options"]:
            st.write(opt)
        key = f"ans_{i}"
        ans = st.text_input(f"Your Answer for Q{i+1} (A/B/C/D):", key=f"ans_{i}")
    if ans:
        st.session_state.answers[f"Q{i+1}"] = ans

# Evaluate answers
if st.button("Evaluate Quiz"):
    incorrect = []
    for i, q in enumerate(st.session_state.quiz):
        topic = q["topic"]
        question = q["question"]
        correct_answer = q["answer"]
        ans = st.session_state.answers.get(f"Q{i+1}", "")
        ans = st.session_state.answers.get(f"{topic}_Q{i+1}", "")
        evaluation = query_ollama(
            f"Question: {question}\n"
            f"Options: {q['options']}\n"
            f"Correct Answer: {correct_answer}\n"
            f"Student's Answer: {ans}\n"
            f"Tell if correct or wrong. If wrong, explain why in 2 lines."
        )
        st.markdown(f"**Evaluation for {topic} Q{i+1}:** {evaluation}")
        if "wrong" in evaluation.lower():
            incorrect.append(topic)

    # Track weak areas
    st.session_state.weak_areas = list(set(incorrect))

# Suggest revision
if st.session_state.weak_areas:
    st.subheader("📌 Suggested Revision Plan")
    revision_plan = query_ollama(
        f"The student is weak in these topics: {st.session_state.weak_areas}. "
        f"Create a simple 3-day revision schedule with 2 focus sessions per day."
    )
    st.write(revision_plan)
