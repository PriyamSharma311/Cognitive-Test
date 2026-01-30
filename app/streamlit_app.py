# app/streamlit_app.py
# =====================================================
# MAIN ENTRY POINT (DO NOT PUT LOGIC HERE)
# =====================================================

from dotenv import load_dotenv

import os
# app/streamlit_app.py

# ==================================================
# 🔒 CRASH PREVENTION (VERY TOP OF FILE)
# ==================================================
import torch
torch.set_num_threads(1)


# ==================================================
# ENV SETUP
# ==================================================

os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["VECLIB_MAXIMUM_THREADS"] = "1"
os.environ["NUMEXPR_NUM_THREADS"] = "1"
os.environ["FAISS_NO_GPU"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
import streamlit as st

# --------------------------------------------------
# ♿ ACCESSIBILITY MODE (SIDEBAR)
# --------------------------------------------------
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


# -----------------------------------------------------
# LOAD ENV (REQUIRED FOR OPENAI / GEMINI)
# -----------------------------------------------------
load_dotenv()

# -----------------------------------------------------
# PAGE CONFIG (MUST BE FIRST STREAMLIT CALL)
# -----------------------------------------------------
st.set_page_config(
    page_title="GenAI Multimodal Cognitive Assessment",
    layout="centered",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------
# TITLE
# -----------------------------------------------------
st.title("🧠 GenAI Multimodal Cognitive Assessment")

st.markdown("""
### 🚀 How to use this prototype

➡️ Use the **left sidebar** to navigate between pages:

1️⃣ **Audio Capture** – Record your voice  
2️⃣ **Text Test** – Answer cognitive questions  
3️⃣ **Insights** – View AI-generated guidance  

⬅️ The sidebar is the **main navigation** for this app.
""")

st.info("📌 If you don’t see the sidebar, click the ☰ icon in the top-left.")

st.divider()

# -----------------------------------------------------
# GLOBAL SESSION STATE (SHARED ACROSS ALL PAGES)
# -----------------------------------------------------
DEFAULTS = {
    # Audio
    "raw_audio_bytes": None,
    "transcript": "",
    "audio_emotion": None,
    "emotion_history": [],

    # Text test
    "responses": {},
    "text_scores": None,
    "text_emotion": {},

    # RAG / context
    "rag_context": "",

    # Safety
    "risk_level": "SAFE"
}

for key, value in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value

# -----------------------------------------------------
# DEBUG (REMOVE BEFORE SUBMISSION)
# -----------------------------------------------------
with st.expander("🔍 Debug: Session State"):
    st.json({
        k: ("<hidden>" if "audio" in k else v)
        for k, v in st.session_state.items()
    })
