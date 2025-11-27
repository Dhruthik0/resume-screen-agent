import streamlit as st
import pandas as pd

from parser import parse_resume
from embedder import get_embedding
from ranker import score_candidates
from llm import get_explanation
from agent import (
    analyze_jd,
    classify_candidates,
    agent_recommendation,
    make_hr_email_draft,
)

st.set_page_config(page_title="AI Resume Screening Agent", layout="wide")
st.title("🤖 AI Resume Screening Agent")


if "has_run" not in st.session_state:
    st.session_state.has_run = False
if "jd_analysis" not in st.session_state:
    st.session_state.jd_analysis = None
if "sorted_results" not in st.session_state:
    st.session_state.sorted_results = None
if "df_results" not in st.session_state:
    st.session_state.df_results = None
if "classified" not in st.session_state:
    st.session_state.classified = None
if "role_title" not in st.session_state:
    st.session_state.role_title = "This Role"




st.subheader("1️⃣ Job Description & Criteria")

jd_text = st.text_area("Paste Job Description", height=200)

col1, col2 = st.columns(2)
with col1:
    required_skills = st.text_input("Required Skills (comma separated, optional)", value="")
with col2:
    required_years = st.number_input("Required Years of Experience (optional)", 0, 50, value=0)

st.subheader("2️⃣ Upload Resumes")
uploaded_files = st.file_uploader(
    "Upload resumes (PDF / DOCX / TXT)",
    type=["pdf", "docx", "txt"],
    accept_multiple_files=True,
)


st.subheader("3️⃣ Agent Thresholds (Optional)")
col_thr1, col_thr2 = st.columns(2)
with col_thr1:
    strong_threshold = st.slider("Strong match threshold", 0.0, 100.0, 75.0)
with col_thr2:
    borderline_threshold = st.slider("Borderline threshold", 0.0, 100.0, 55.0)



if st.button("🚀 Run Screening Agent"):
    if not jd_text or not uploaded_files:
        st.warning("⚠ Please provide both a Job Description and at least one resume.")
        st.stop()

    
    jd_analysis = analyze_jd(
        jd_text,
        required_skills.split(",") if required_skills else [],
        required_years if required_years > 0 else None,
    )
    st.session_state.jd_analysis = jd_analysis

    
    candidates = []
    st.info("📄 Parsing resumes...")
    for f in uploaded_files:
        cand = parse_resume(f)
        candidates.append(cand)

    
    st.info("🔢 Embedding Job Description (local model, no API key)...")
    jd_emb = get_embedding(jd_text)

    
    st.info("📊 Scoring candidates...")
    results = score_candidates(
        candidates,
        jd_text,
        jd_emb,
        required_skills.split(",") if required_skills else [],
        required_years,
        {"w_sem": 0.5, "w_skill": 0.35, "w_exp": 0.15},
    )

    sorted_results = sorted(results, key=lambda x: x.get("final_score", 0), reverse=True)

    table_rows = []
    for r in sorted_results:
        score = r.get("final_score", 0)
        explanation = get_explanation(jd_text, r, score)
        r["explanation"] = explanation

        table_rows.append(
            {
                "file_name": r.get("file_name"),
                "final_score": score,
                "semantic_score": r.get("semantic"),
                "skill_score": r.get("skill_score"),
                "experience_score": r.get("experience_score"),
                "skills": ", ".join(r.get("skills", [])),
                "experience_years": r.get("total_experience"),
                "explanation": explanation,
            }
        )

    if table_rows:
        df = pd.DataFrame(table_rows)
    else:
        df = None

    # 5. Classification
    classified = classify_candidates(
        sorted_results,
        threshold_strong=strong_threshold,
        threshold_borderline=borderline_threshold,
    )

    
    role_title = "This Role"
    if jd_text:
        first_line = jd_text.strip().split("\n")[0]
        if 0 < len(first_line) < 80:
            role_title = first_line

    
    st.session_state.sorted_results = sorted_results
    st.session_state.df_results = df
    st.session_state.classified = classified
    st.session_state.role_title = role_title
    st.session_state.has_run = True




if st.session_state.has_run and st.session_state.sorted_results is not None:
    jd_analysis = st.session_state.jd_analysis
    sorted_results = st.session_state.sorted_results
    df = st.session_state.df_results
    classified = st.session_state.classified
    role_title = st.session_state.role_title

    
    st.subheader("🧠 Agent Pre-Check on Job Description")
    if jd_analysis and jd_analysis["issues"]:
        st.warning("The agent noticed some potential issues with your JD:")
        for issue in jd_analysis["issues"]:
            st.write("- ", issue)
    else:
        st.success("The agent did not detect obvious issues in your JD.")

    if jd_analysis and jd_analysis["questions"]:
        st.info("The agent has some clarification questions for you:")
        for q in jd_analysis["questions"]:
            st.write("- ", q)

    st.markdown("---")

    
    st.subheader("🏆 Ranking Results")
    if df is not None:
        
        for r in sorted_results:
            score = r.get("final_score", 0)
            with st.expander(f"{r.get('file_name', 'Candidate')} — Score: {score:.1f}"):
                st.write("**Final Score:**", f"{score:.1f}")
                st.write("**Skills:**", ", ".join(r.get("skills", [])))
                st.write("**Experience (years):**", r.get("total_experience"))
                st.write("**Explanation:**")
                st.write(r.get("explanation", ""))

        st.dataframe(df)
        st.download_button(
            "⬇️ Download All Results as CSV",
            df.to_csv(index=False),
            "screening_results.csv",
            mime="text/csv",
        )
    else:
        st.info("No candidates to display.")

    
    st.subheader("🤖 Agent Decision")
    decision_text = agent_recommendation(classified)
    st.write(decision_text)

    if classified["strong"]:
        st.markdown("**Strongly recommended candidates:**")
        for c in classified["strong"]:
            st.write(
                "-",
                c.get("name") or c.get("file_name"),
                f"(Score: {c.get('final_score', 0):.1f})",
            )

    st.markdown("---")

    
    if classified["strong"]:
        if st.checkbox("Show only shortlisted (strong) candidates table"):
            strong_df = df[df["final_score"] >= strong_threshold]
            st.dataframe(strong_df)
            st.download_button(
                "⬇️ Download Shortlisted Candidates CSV",
                strong_df.to_csv(index=False),
                "shortlisted_candidates.csv",
                mime="text/csv",
            )

    if st.checkbox("Generate HR email draft based on agent recommendation"):
        st.subheader("📨 HR Email Draft (generated by agent)")
        email_text = make_hr_email_draft(role_title, classified["strong"])
        st.text_area(
            "You can copy-paste this email into Gmail/Outlook:",
            email_text,
            height=260,
        )
