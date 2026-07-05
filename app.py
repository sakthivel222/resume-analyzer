# app.py
# Main Streamlit application - entry point

import streamlit as st
import os
import tempfile
from extractor import extract_text, split_into_sections, extract_contact_info
from ats_scorer import calculate_ats_score
from grammar_checker import check_grammar
from skills_matcher import extract_skills_from_text, compare_resume_jd

st.set_page_config(page_title="AI Resume Analyzer", layout="wide")
st.title("📄 AI Resume Analyzer")
st.write("Upload your resume to get an ATS score, grammar check, skill gaps, and improvement tips.")

uploaded_file = st.file_uploader("Upload Resume (PDF or DOCX)", type=["pdf", "docx"])

if uploaded_file:
    # Save temp file
    suffix = ".pdf" if uploaded_file.name.endswith(".pdf") else ".docx"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    with st.spinner("Analyzing resume..."):
        text = extract_text(tmp_path)
        sections = split_into_sections(text)
        contact_info = extract_contact_info(text)
        ats_score, ats_breakdown = calculate_ats_score(text, sections, contact_info)
        grammar_result = check_grammar(text)
        skills_found = extract_skills_from_text(text)

    os.remove(tmp_path)

    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        ["📊 ATS Score", "✍️ Grammar", "🛠️ Skills", "📁 Sections", "🎯 JD Comparison"]
    )

    with tab1:
        st.metric("ATS Score", f"{ats_score}/100")
        st.progress(int(ats_score))
        st.subheader("Score Breakdown")
        for category, points in ats_breakdown.items():
            st.write(f"**{category}**: {points} points")

        st.subheader("Contact Info Detected")
        st.json(contact_info)

    with tab2:
        st.subheader(f"Grammar Issues Found: {grammar_result['total_issues']}")
        if grammar_result["weak_phrases"]:
            st.warning(
                f"Weak phrases detected: {', '.join(grammar_result['weak_phrases'])}. "
                f"Replace with strong action verbs like 'led', 'built', 'designed', 'optimized'."
            )
        for issue in grammar_result["issues"]:
            st.write(f"⚠️ {issue['message']}")
            st.caption(f"Context: ...{issue['context']}...")
            if issue["suggestion"]:
                st.caption(f"Suggestions: {', '.join(issue['suggestion'])}")
            st.divider()

    with tab3:
        st.subheader("Skills Detected in Resume")
        if skills_found:
            st.write(", ".join([f"`{s}`" for s in skills_found]))
        else:
            st.warning("No standard technical skills detected. Consider adding a dedicated Skills section.")

    with tab4:
        st.subheader("Section-wise Content")
        for section, content in sections.items():
            with st.expander(f"{section.title()} ({len(content.split())} words)"):
                st.text(content if content.strip() else "Not found / empty")

    with tab5:
        st.subheader("Compare with Job Description")
        jd_text = st.text_area("Paste Job Description here", height=200)
        if st.button("Compare"):
            if jd_text.strip():
                comparison = compare_resume_jd(text, jd_text)
                st.metric("Resume-JD Match", f"{comparison['similarity_score']}%")

                col1, col2 = st.columns(2)
                with col1:
                    st.success("✅ Matched Skills")
                    st.write(", ".join(comparison["matched_skills"]) or "None")
                with col2:
                    st.error("❌ Missing Skills")
                    st.write(", ".join(comparison["missing_skills"]) or "None")
            else:
                st.warning("Please paste a job description first.")
else:
    st.info("👆 Upload a resume to get started")
