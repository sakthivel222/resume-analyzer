# skills_matcher.py
# Semantic skill extraction and resume-vs-JD comparison using Sentence Transformers

from sentence_transformers import SentenceTransformer, util
from skills_data import TECH_SKILLS

model = SentenceTransformer('all-MiniLM-L6-v2')


def extract_skills_from_text(text):
    """Find which skills from the taxonomy are present in text."""
    text_lower = text.lower()
    found_skills = []

    for skill in TECH_SKILLS:
        if skill in text_lower:
            found_skills.append(skill)

    return list(set(found_skills))


def compare_resume_jd(resume_text, jd_text):
    """Compare resume against job description using semantic similarity."""
    resume_emb = model.encode(resume_text, convert_to_tensor=True)
    jd_emb = model.encode(jd_text, convert_to_tensor=True)
    similarity = util.cos_sim(resume_emb, jd_emb).item()

    resume_skills = set(extract_skills_from_text(resume_text))
    jd_skills = set(extract_skills_from_text(jd_text))

    missing_skills = jd_skills - resume_skills
    matched_skills = jd_skills & resume_skills

    return {
        "similarity_score": round(similarity * 100, 1),
        "matched_skills": list(matched_skills),
        "missing_skills": list(missing_skills),
        "resume_skills": list(resume_skills),
        "jd_skills": list(jd_skills)
    }
