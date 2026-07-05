# ats_scorer.py
# Rule-based ATS scoring engine

import re


def calculate_ats_score(text, sections, contact_info):
    score = 0
    breakdown = {}

    # 1. Contact info completeness (20 points)
    contact_score = 0
    if contact_info["email"]:
        contact_score += 7
    if contact_info["phone"]:
        contact_score += 7
    if contact_info["linkedin"] or contact_info["github"]:
        contact_score += 6
    breakdown["Contact Info"] = contact_score
    score += contact_score

    # 2. Section presence (30 points)
    section_score = 0
    key_sections = ["experience", "education", "skills", "projects"]
    for sec in key_sections:
        if sections.get(sec, "").strip():
            section_score += 7.5
    breakdown["Section Completeness"] = round(section_score, 1)
    score += section_score

    # 3. Quantifiable achievements (20 points)
    numbers_found = len(re.findall(r"\d+%|\d+\+|\$\d+|\d+x", text))
    metric_score = min(numbers_found * 4, 20)
    breakdown["Quantifiable Impact"] = metric_score
    score += metric_score

    # 4. Length check (15 points)
    word_count = len(text.split())
    if 300 <= word_count <= 800:
        length_score = 15
    elif word_count < 300:
        length_score = 8
    else:
        length_score = 10
    breakdown["Length Appropriateness"] = length_score
    score += length_score

    # 5. Formatting red flags (15 points)
    formatting_score = 15
    if len(re.findall(r"\t", text)) > 10:
        formatting_score -= 5  # possible table/column layout
    if word_count < 100:
        formatting_score -= 10  # likely parsing failure due to bad layout
    breakdown["Formatting/Parseability"] = max(formatting_score, 0)
    score += max(formatting_score, 0)

    return round(score, 1), breakdown
