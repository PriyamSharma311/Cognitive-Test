# app/pages/Insights.py
import os, sys, time
import streamlit as st
import pandas as pd
from openai import RateLimitError

# --------------------------------------------------
# ♿ ACCESSIBILITY MODE
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

# --------------------------------------------------
# DEMO MODE (NO LLM CALLS)
# --------------------------------------------------
DEMO_MODE = st.sidebar.toggle("🎥 Demo Mode (Disable AI calls)", value=False)

# --------------------------------------------------
# PATH FIX
# --------------------------------------------------
PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../..")
)
sys.path.append(PROJECT_ROOT)

# --------------------------------------------------
# IMPORTS
# --------------------------------------------------
from src.llm.llm_orchestrator import generate_final_response
from src.career.career_mapper import recommend_career_fields
from src.learning.learning_roadmap import generate_learning_roadmap
from src.assessment.scoring_engine import (
    compute_domain_scores,
    build_cognitive_profile
)

# --------------------------------------------------
# BASE STYLES
# --------------------------------------------------
st.markdown("""
<style>
html, body, [class*="css"] {
    font-size: 18px !important;
    line-height: 1.6;
}
button {
    font-size: 18px !important;
}
</style>
""", unsafe_allow_html=True)

st.title("💡 Insights & Career Guidance")

# --------------------------------------------------
# SESSION STATE INPUTS
# --------------------------------------------------
transcript = st.session_state.get("transcript")
audio_emotion = st.session_state.get("audio_emotion")
text_scores = st.session_state.get("text_scores")
answers = st.session_state.get("answers")

if not transcript and not text_scores and not answers:
    st.info("ℹ️ Please complete an assessment first.")
    st.stop()

# ==================================================
# 🧠 COGNITIVE PERFORMANCE SUMMARY (TEXT TEST)
# ==================================================
scores = {}

if text_scores:
    scores = text_scores.get("normalized_scores", {})

    strengths = [k for k, v in scores.items() if v >= 70]
    moderate = [k for k, v in scores.items() if 40 <= v < 70]
    weaknesses = [k for k, v in scores.items() if v < 40]

    st.subheader("🧠 Cognitive Performance Summary (Text-Based)")
    st.markdown(f"""
- **Strengths:** {', '.join(strengths) or 'None'}
- **Moderate areas:** {', '.join(moderate) or 'None'}
- **Needs support:** {', '.join(weaknesses) or 'None'}
""")

# --------------------------------------------------
# 📊 COGNITIVE PROFILE CHART
# --------------------------------------------------
if scores:
    df = pd.DataFrame(scores.items(), columns=["Cognitive Domain", "Score"])
    st.subheader("📊 Cognitive Strength Profile (Text-Based)")
    st.bar_chart(df.set_index("Cognitive Domain"))

# ==================================================
# 🧩 ADAPTIVE ASSESSMENT INSIGHTS
# ==================================================
if answers:
    st.subheader("🧩 Adaptive Assessment Insights")

    # 1. Compute raw adaptive statistics
    domain_stats = compute_domain_statistics(answers)

    # 2. Build unified cognitive profile using ability (theta)
    theta = st.session_state.get("cog_state", {}).theta if "cog_state" in st.session_state else 0.0

    adaptive_profile = build_profile_from_adaptive_test(
        domain_stats=domain_stats,
        theta=theta
    )

    st.session_state.cognitive_profile = adaptive_profile

    # 3. Display results
    for domain, score in adaptive_profile["cognitive_profile"].items():
        explanation = adaptive_profile["explanations"].get(domain, "")

        st.markdown(f"""
**{domain.upper()}**  
Score: **{score}%**  
_{explanation}_
""")
        st.progress(score / 100)


# ==================================================
# 🎯 CAREER FIELD RECOMMENDATIONS
# ==================================================
if scores:
    career_output = recommend_career_fields(scores)

    st.subheader("🎯 Career Field Recommendations")

    for item in career_output.get("recommended_fields", []):
        roles_text = "\n".join([f"- {r}" for r in item["roles"]])
        st.markdown(f"""
### 🔹 {item['field']}
**Why this fits you:**  
{item['why']}

**Example roles:**  
{roles_text}
""")

    confidence = career_output.get("confidence")
    if confidence is not None:
        st.subheader("📈 Career Readiness Confidence")
        st.progress(confidence / 100)
    else:
        st.caption("ℹ️ Confidence score not available.")

# ==================================================
# 🎯 PERSONALIZED LEARNING ROADMAP
# ==================================================
st.subheader("🎯 Personalized Learning Roadmap")

if DEMO_MODE:
    st.info("Demo mode enabled. Learning roadmap is disabled.")
elif scores:
    if "learning_roadmap" not in st.session_state:
        if st.button("📘 Generate Learning Roadmap"):
            with st.spinner("Creating your personalized roadmap..."):
                try:
                    roadmap = generate_learning_roadmap(scores)
                    st.session_state.learning_roadmap = roadmap
                    st.write(roadmap)
                except RateLimitError:
                    st.error("⚠️ AI rate-limited. Please wait and retry.")
    else:
        st.write(st.session_state.learning_roadmap)
else:
    st.info("ℹ️ Complete the text test to generate a learning roadmap.")

# ==================================================
# 💬 FINAL GUIDANCE (COOLDOWN + CACHE)
# ==================================================
st.subheader("💬 AI Career Guidance")

if DEMO_MODE:
    st.info("Demo mode enabled. AI guidance is disabled.")
elif st.button("🧠 Generate Final Guidance"):

    last_call = st.session_state.get("final_guidance_time", 0)
    now = time.time()

    if now - last_call < 30:
        st.warning("⏳ Please wait 30 seconds before generating again.")
    else:
        try:
            with st.spinner("Generating guidance..."):
                response = generate_final_response(
                    user_text=transcript or "User completed assessments.",
                    rag_context=st.session_state.get("rag_context", ""),
                    text_emotion=st.session_state.get("text_emotion", {}),
                    audio_emotion=audio_emotion,
                    cognitive_profile=st.session_state.get("cognitive_profile", {}),
                    risk_level="SAFE",
                    mode="🎯 Career Guidance"
                )
                st.session_state.final_guidance = response
                st.session_state.final_guidance_time = now
                st.write(response)

        except RateLimitError:
            st.error("⚠️ AI rate-limited. Please wait 30–60 seconds and retry.")
