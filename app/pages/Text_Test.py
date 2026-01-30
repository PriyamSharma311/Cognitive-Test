import os
import sys

# --------------------------------------------------
# ♿ ACCESSIBILITY MODE (SIDEBAR)
# --------------------------------------------------

import streamlit as st
import json
if st.sidebar.checkbox("♿ Accessibility Mode"):
    st.markdown("""
    <style>
    html, body, [class*="css"] {
        font-size: 22px !important;
        line-height: 1.8;
    }
    button {
        font-size: 20px !important;
    }
    </style>
    """, unsafe_allow_html=True)




PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)
sys.path.append(PROJECT_ROOT)

from dotenv import load_dotenv
load_dotenv()


import streamlit as st
import json

st.markdown(
    """
<style>
html, body, [class*="css"] {
    font-size: 18px !important;
    line-height: 1.6;
}
button {
    font-size: 18px !important;
}
</style>
""",
    unsafe_allow_html=True
)

from src.inputs.text_tests.scoring_rules import score_responses

st.set_page_config(page_title="Text Test")
st.title("📝 Text-Based Cognitive Test")

st.session_state.setdefault("responses", {})
st.session_state.setdefault("text_scores", None)

QUESTIONS_PATH = os.path.join(
    os.getcwd(), "src", "inputs", "text_tests", "questions.json"
)

QUESTIONS = json.load(open(QUESTIONS_PATH))["questions"]

domains = sorted(set(q["domain"] for q in QUESTIONS))
selected_domain = st.selectbox("Select cognitive domain", domains)

for q in QUESTIONS:
    if q["domain"] != selected_domain:
        continue

    st.markdown(f"**{q['question_id']}**")
    if "options" in q:
        ans = st.radio(q["question"], q["options"], key=q["question_id"])
    else:
        ans = st.text_input(q["question"], key=q["question_id"])

    if ans:
        st.session_state.responses[q["question_id"]] = {"answer": ans}

if st.button("📊 Score Text Test"):
    st.session_state.text_scores = score_responses(
        st.session_state.responses,
        {"questions": QUESTIONS}
    )
    st.success("Text test scored!")

    st.json(st.session_state.text_scores["normalized_scores"])
