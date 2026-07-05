# extractor.py
# Handles reading resume files and splitting them into logical sections

import pdfplumber
import docx
import re
from skills_data import SECTION_HEADERS


def extract_text(file_path):
    """Extract raw text from PDF or DOCX file."""
    if file_path.endswith(".pdf"):
        text = ""
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text
    elif file_path.endswith(".docx"):
        doc = docx.Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs])
    else:
        raise ValueError("Unsupported file format. Use PDF or DOCX.")


def split_into_sections(text):
    """Split resume text into sections based on common headers."""
    lines = text.split("\n")
    sections = {key: "" for key in SECTION_HEADERS}
    sections["other"] = ""
    current_section = "other"

    for line in lines:
        line_clean = line.strip().lower()
        matched = False
        for section, keywords in SECTION_HEADERS.items():
            for kw in keywords:
                if kw in line_clean and len(line_clean) < 40:
                    current_section = section
                    matched = True
                    break
            if matched:
                break
        if not matched:
            sections[current_section] += line + "\n"

    return sections


def extract_contact_info(text):
    """Detect email, phone, LinkedIn, GitHub from resume text."""
    email = re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
    phone = re.findall(r"(\+?\d{1,3}[-.\s]?)?\d{10}", text)
    linkedin = re.findall(r"linkedin\.com/in/[a-zA-Z0-9-]+", text)
    github = re.findall(r"github\.com/[a-zA-Z0-9-]+", text)
    return {
        "email": email[0] if email else None,
        "phone": phone[0] if phone else None,
        "linkedin": linkedin[0] if linkedin else None,
        "github": github[0] if github else None
    }
