import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.insert(0, PROJECT_ROOT)

import streamlit as st
import random

from src.assessment.reasoning_bank import load_reasoning_bank


st.set_page_config(page_title="Adaptive Reasoning Test", layout="wide")

# --------------------------------------------------
# CONSTANTS
# --------------------------------------------------
BATCH_SIZE = 4
PASS_THRESHOLD = 0.75
MAX_FAILS = 2
MAX_LEVEL = 5

# --------------------------------------------------
# SESSION INITIALIZATION
# --------------------------------------------------
if "initialized" not in st.session_state:
    st.session_state.initialized = True
    st.session_state.bank = load_reasoning_bank()
    st.session_state.current_level = 1
    st.session_state.batch_index = 1
    st.session_state.consecutive_fails = 0
    st.session_state.used_question_ids = set()
    st.session_state.current_questions = []
    st.session_state.answers = {}
    st.session_state.scores = []
    st.session_state.test_complete = False

# --------------------------------------------------
# LOAD NEW BATCH
# --------------------------------------------------
def load_new_batch():
    level_key = str(st.session_state.current_level)
    pool = st.session_state.bank[level_key]

    available = [
        q for q in pool
        if q["id"] not in st.session_state.used_question_ids
    ]

    if len(available) < BATCH_SIZE:
        st.error(
            f"❌ Not enough unused questions at Level {level_key}. "
            "Please regenerate the reasoning bank."
        )
        st.stop()

    batch = random.sample(available, BATCH_SIZE)

    for q in batch:
        st.session_state.used_question_ids.add(q["id"])

    st.session_state.current_questions = batch
    st.session_state.answers = {}

# --------------------------------------------------
# FIRST LOAD
# --------------------------------------------------
if not st.session_state.current_questions:
    load_new_batch()

# --------------------------------------------------
# UI HEADER
# --------------------------------------------------
st.title("🧠 Adaptive Reasoning Assessment")
st.subheader(
    f"Level {st.session_state.current_level} — "
    f"Batch {st.session_state.batch_index}"
)

st.markdown(
    "Answer all **4 questions**, then submit.\n\n"
    "You must score **at least 3/4** to advance."
)

st.write("---")

# --------------------------------------------------
# QUESTIONS
# --------------------------------------------------
for idx, q in enumerate(st.session_state.current_questions):
    st.markdown(f"### Q{idx + 1}. {q['question']}")
    st.session_state.answers[q["id"]] = st.radio(
        "Select one option:",
        q["options"],
        key=q["id"]
    )
    st.write("")

# --------------------------------------------------
# SUBMIT BATCH
# --------------------------------------------------
if st.button("Submit Batch"):
    correct = 0

    for q in st.session_state.current_questions:
        if st.session_state.answers.get(q["id"]) == q["answer"]:
            correct += 1

    score_ratio = correct / BATCH_SIZE
    st.session_state.scores.append(score_ratio)

    st.write("---")
    st.markdown(f"### ✅ You scored **{correct}/4**")

    # ---------------- PROMOTION LOGIC ----------------
    if score_ratio >= PASS_THRESHOLD:
        st.success("🎉 You passed this level!")
        st.session_state.consecutive_fails = 0

        if st.session_state.current_level < MAX_LEVEL:
            st.session_state.current_level += 1
            st.session_state.batch_index = 1
        else:
            st.success("🏆 You completed the highest difficulty!")
            st.session_state.test_complete = True

    else:
        st.warning("⚠️ You did not pass this batch.")
        st.session_state.consecutive_fails += 1
        st.session_state.batch_index += 1

    # ---------------- TERMINATION CHECK ----------------
    if st.session_state.consecutive_fails >= MAX_FAILS:
        st.error("❌ Test terminated due to repeated failures.")
        st.session_state.test_complete = True

    # ---------------- END OR CONTINUE ----------------
    if st.session_state.test_complete:
        st.write("---")
        st.subheader("📊 Final Result")

        avg_accuracy = round(
            sum(st.session_state.scores) / len(st.session_state.scores) * 100, 2
        )

        st.markdown(
            f"**Final Level Reached:** {st.session_state.current_level}\n\n"
            f"**Average Accuracy:** {avg_accuracy}%"
        )

        st.session_state.reasoning_result = {
            "final_level": st.session_state.current_level,
            "average_accuracy": avg_accuracy
        }

        st.info("Proceed to the **Insights** page.")
        st.stop()

    # Prepare next batch
    st.session_state.current_questions = []
    st.rerun()
