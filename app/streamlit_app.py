import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import tempfile
import streamlit as st
import pandas as pd

from src.pipeline import ResumePipeline

# -------------------------
# Page Config
# -------------------------
st.set_page_config(
    page_title="AI Resume Screener",
    page_icon="📄",
    layout="wide"
)

# -------------------------
# Styling
# -------------------------
st.markdown("""
<style>
    /* Base */
    [data-testid="stAppViewContainer"] {
        background-color: #080810;
    }
    [data-testid="stHeader"] {
        background: transparent;
    }
    .block-container {
        padding: 2rem 3rem;
        max-width: 1200px;
    }

    /* Hero */
    .hero {
        padding: 48px 0 32px 0;
        border-bottom: 1px solid #1e1e2e;
        margin-bottom: 40px;
    }
    .hero-label {
        font-size: 11px;
        letter-spacing: 3px;
        text-transform: uppercase;
        color: #6ee7b7;
        font-family: monospace;
        margin-bottom: 12px;
    }
    .hero-title {
        font-size: 42px;
        font-weight: 800;
        color: #ffffff;
        letter-spacing: -1px;
        margin-bottom: 10px;
        line-height: 1.1;
    }
    .hero-sub {
        font-size: 15px;
        color: #64748b;
        font-family: monospace;
    }

    /* Section headers */
    .section-title {
        font-size: 11px;
        letter-spacing: 3px;
        text-transform: uppercase;
        color: #64748b;
        font-family: monospace;
        margin-bottom: 16px;
        margin-top: 8px;
    }

    /* Upload panel */
    .upload-panel {
        background: #0f0f1a;
        border: 1px solid #1e1e2e;
        border-radius: 16px;
        padding: 28px;
        height: 100%;
    }
    .upload-panel-title {
        font-size: 14px;
        font-weight: 700;
        color: #e2e8f0;
        margin-bottom: 16px;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    /* File list */
    .file-item {
        display: flex;
        align-items: center;
        gap: 10px;
        background: #1a1a2e;
        border: 1px solid #2d2d44;
        border-radius: 8px;
        padding: 10px 14px;
        margin-bottom: 8px;
        font-size: 13px;
        color: #94a3b8;
        font-family: monospace;
    }
    .file-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: #6ee7b7;
        flex-shrink: 0;
    }

    /* Analyze button override */
    [data-testid="stButton"] > button {
        background: linear-gradient(135deg, #6ee7b7 0%, #3b82f6 100%);
        color: #000000;
        font-weight: 800;
        font-size: 15px;
        border: none;
        border-radius: 12px;
        padding: 16px;
        width: 100%;
        letter-spacing: 0.5px;
        transition: opacity 0.2s;
    }
    [data-testid="stButton"] > button:hover {
        opacity: 0.9;
    }

    /* Rankings table */
    .rank-table {
        width: 100%;
        border-collapse: collapse;
        font-family: monospace;
        font-size: 13px;
    }
    .rank-table th {
        text-align: left;
        color: #64748b;
        padding: 10px 16px;
        border-bottom: 1px solid #1e1e2e;
        font-size: 11px;
        letter-spacing: 2px;
        text-transform: uppercase;
    }
    .rank-table td {
        padding: 14px 16px;
        border-bottom: 1px solid #0f0f1a;
        color: #cbd5e1;
    }
    .rank-table tr:hover td {
        background: #0f0f1a;
    }
    .rank-num {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 28px;
        height: 28px;
        border-radius: 50%;
        background: linear-gradient(135deg, #6ee7b7, #3b82f6);
        color: #000;
        font-weight: 800;
        font-size: 12px;
    }
    .score-pill {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 13px;
    }
    .score-high { background: rgba(110,231,183,0.15); color: #6ee7b7; }
    .score-mid  { background: rgba(251,191,36,0.15);  color: #fbbf24; }
    .score-low  { background: rgba(251,113,133,0.15); color: #fb7185; }

    /* Candidate card */
    .candidate-header {
        background: #0f0f1a;
        border: 1px solid #1e1e2e;
        border-radius: 12px;
        padding: 20px 24px;
        margin-bottom: 12px;
    }
    .candidate-name {
        font-size: 18px;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 4px;
    }
    .candidate-rank {
        font-size: 12px;
        color: #6ee7b7;
        font-family: monospace;
        letter-spacing: 1px;
    }

    /* Score cards */
    .score-card {
        background: #0f0f1a;
        border: 1px solid #1e1e2e;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
    }
    .score-card-label {
        font-size: 10px;
        letter-spacing: 2px;
        text-transform: uppercase;
        color: #64748b;
        font-family: monospace;
        margin-bottom: 8px;
    }
    .score-card-value {
        font-size: 32px;
        font-weight: 800;
        color: #ffffff;
    }

    /* Summary box */
    .summary-box {
        background: #0f0f1a;
        border-left: 3px solid #6ee7b7;
        border-radius: 0 12px 12px 0;
        padding: 18px 20px;
        font-size: 14px;
        color: #94a3b8;
        line-height: 1.7;
        margin: 16px 0;
        font-style: italic;
    }

    /* Skill tags */
    .skill-tag-green {
        display: inline-block;
        background: rgba(110,231,183,0.1);
        color: #6ee7b7;
        border: 1px solid rgba(110,231,183,0.25);
        border-radius: 6px;
        padding: 4px 12px;
        margin: 4px;
        font-size: 12px;
        font-family: monospace;
    }
    .skill-tag-red {
        display: inline-block;
        background: rgba(251,113,133,0.1);
        color: #fb7185;
        border: 1px solid rgba(251,113,133,0.25);
        border-radius: 6px;
        padding: 4px 12px;
        margin: 4px;
        font-size: 12px;
        font-family: monospace;
    }
    .skills-section-title {
        font-size: 11px;
        letter-spacing: 2px;
        text-transform: uppercase;
        color: #64748b;
        font-family: monospace;
        margin-bottom: 10px;
        margin-top: 16px;
    }

    /* Divider */
    .divider {
        border: none;
        border-top: 1px solid #1e1e2e;
        margin: 32px 0;
    }

    /* Hide default streamlit elements */
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# -------------------------
# Load Pipeline
# -------------------------
@st.cache_resource
def load_pipeline():
    return ResumePipeline("data/skills/skills_en.csv")

pipeline = load_pipeline()

# -------------------------
# Hero
# -------------------------
st.markdown("""
<div class="hero">
    <div class="hero-label">Powered by ESCO + Sentence Transformers + Gemini</div>
    <div class="hero-title">AI Resume Screening</div>
    <div class="hero-sub">Upload a job description and resumes → get ranked candidates instantly</div>
</div>
""", unsafe_allow_html=True)

# -------------------------
# Upload Section
# -------------------------
st.markdown('<div class="section-title">Input</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown('<div class="upload-panel-title">📋 Job Description</div>', unsafe_allow_html=True)
    job_description = st.text_area(
        label="jd",
        label_visibility="collapsed",
        height=280,
        placeholder="Paste the job description here...\n\nExample:\nWe are looking for a Machine Learning Engineer with experience in Python, TensorFlow, and SQL..."
    )

with col2:
    st.markdown('<div class="upload-panel-title">📁 Resumes</div>', unsafe_allow_html=True)
    uploaded_files = st.file_uploader(
        label="resumes",
        label_visibility="collapsed",
        type=["pdf"],
        accept_multiple_files=True
    )
    if uploaded_files:
        for f in uploaded_files:
            name = os.path.splitext(f.name)[0]
            st.markdown(f'<div class="file-item"><div class="file-dot"></div>{name}</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
analyze = st.button("Analyze Resumes →", use_container_width=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# -------------------------
# Analyze
# -------------------------
if analyze:
    if not job_description.strip():
        st.error("Please enter a job description.")
    elif not uploaded_files:
        st.error("Please upload at least one resume.")
    else:
        pdf_paths = []
        tmp_files = []

        for uploaded_file in uploaded_files:
            tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
            tmp.write(uploaded_file.getvalue())
            tmp.close()
            pdf_paths.append((tmp.name, uploaded_file.name))
            tmp_files.append(tmp.name)

        try:
            with st.spinner("Analyzing candidates..."):
                results = []
                for pdf_path, original_name in pdf_paths:
                    result = pipeline.rank_pdf_resume(pdf_path, job_description)
                    result["filename"] = os.path.splitext(original_name)[0]
                    results.append(result)
                results.sort(key=lambda x: x["final_score"], reverse=True)

            # -------------------------
            # Rankings Table
            # -------------------------
            st.markdown('<div class="section-title">Rankings</div>', unsafe_allow_html=True)

            def score_pill(score_str):
                val = int(score_str.replace("%", ""))
                cls = "score-high" if val >= 60 else "score-mid" if val >= 35 else "score-low"
                return f'<span class="score-pill {cls}">{score_str}</span>'

            rows = ""
            for rank, r in enumerate(results, 1):
                final = f"{r['final_score']:.0%}"
                semantic = f"{r['semantic_score']:.0%}"
                skill = f"{r['skill_score']:.0%}"
                rows += f"""
                <tr>
                    <td><span class="rank-num">{rank}</span></td>
                    <td style="font-weight:600; color:#e2e8f0;">{r['filename']}</td>
                    <td>{score_pill(final)}</td>
                    <td style="color:#94a3b8;">{semantic}</td>
                    <td style="color:#94a3b8;">{skill}</td>
                    <td style="color:#6ee7b7;">{len(r['matched_skills'])}</td>
                    <td style="color:#fb7185;">{len(r['missing_skills'])}</td>
                </tr>
                """

            h1, h2, h3, h4, h5, h6, h7 = st.columns([0.5, 2, 1.5, 1.5, 1.5, 1, 1])
            h1.markdown("**#**")
            h2.markdown("**Candidate**")
            h3.markdown("**Final Score**")
            h4.markdown("**Semantic**")
            h5.markdown("**Skill Match**")
            h6.markdown("**Matched**")
            h7.markdown("**Missing**")
            st.divider()
            
            for rank, r in enumerate(results, 1):
                final = r['final_score']
                col1, col2, col3, col4, col5, col6, col7 = st.columns([0.5, 2, 1.5, 1.5, 1.5, 1, 1])
                col1.markdown(f"**#{rank}**")
                col2.markdown(f"**{r['filename']}**")
                col3.markdown(f"`{final:.0%}`")
                col4.markdown(f"`{r['semantic_score']:.0%}`")
                col5.markdown(f"`{r['skill_score']:.0%}`")
                col6.markdown(f"✅ {len(r['matched_skills'])}")
                col7.markdown(f"❌ {len(r['missing_skills'])}")

            st.markdown('<hr class="divider">', unsafe_allow_html=True)

            # -------------------------
            # Candidate Details
            # -------------------------
            st.markdown('<div class="section-title">Candidate Details</div>', unsafe_allow_html=True)

            for rank, result in enumerate(results, 1):
                with st.expander(f"#{rank}  {result['filename']}  —  {result['final_score']:.0%}"):

                    # Score cards
                    c1, c2, c3 = st.columns(3)
                    with c1:
                        st.markdown(f"""
                        <div class="score-card">
                            <div class="score-card-label">Final Score</div>
                            <div class="score-card-value">{result['final_score']:.0%}</div>
                        </div>""", unsafe_allow_html=True)
                    with c2:
                        st.markdown(f"""
                        <div class="score-card">
                            <div class="score-card-label">Semantic Similarity</div>
                            <div class="score-card-value">{result['semantic_score']:.0%}</div>
                        </div>""", unsafe_allow_html=True)
                    with c3:
                        st.markdown(f"""
                        <div class="score-card">
                            <div class="score-card-label">Skill Match</div>
                            <div class="score-card-value">{result['skill_score']:.0%}</div>
                        </div>""", unsafe_allow_html=True)

                    # Summary
                    summary = result.get("summary", "")
                    if summary and not summary.startswith("Summary unavailable"):
                        st.markdown(f'<div class="summary-box">{summary}</div>', unsafe_allow_html=True)
                    else:
                        st.markdown('<div class="summary-box" style="border-color:#64748b; color:#475569;">AI summary unavailable — Gemini quota exceeded. Try again in a moment.</div>', unsafe_allow_html=True)

                    # Skills
                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.markdown('<div class="skills-section-title">✅ Matched Skills</div>', unsafe_allow_html=True)
                        if result["matched_skills"]:
                            tags = "".join([f'<span class="skill-tag-green">{s}</span>' for s in result["matched_skills"]])
                            st.markdown(tags, unsafe_allow_html=True)
                        else:
                            st.markdown('<span style="color:#475569; font-size:13px;">No matched skills found.</span>', unsafe_allow_html=True)

                    with col_b:
                        st.markdown('<div class="skills-section-title">❌ Missing Skills</div>', unsafe_allow_html=True)
                        if result["missing_skills"]:
                            tags = "".join([f'<span class="skill-tag-red">{s}</span>' for s in result["missing_skills"]])
                            st.markdown(tags, unsafe_allow_html=True)
                        else:
                            st.markdown('<span style="color:#475569; font-size:13px;">No missing skills.</span>', unsafe_allow_html=True)

        finally:
            for path in tmp_files:
                if os.path.exists(path):
                    os.remove(path)