<<<<<<< HEAD
# AI Resume Analyzer

An NLP-based tool that analyzes resumes and provides ATS scoring,
grammar feedback, skill gap analysis, and job description comparison.

## Features
- ATS Score (0-100) with detailed breakdown
- Grammar and weak-phrase detection
- Technical skills extraction
- Resume vs Job Description semantic comparison using Sentence Transformers

## Tech Stack
- Python
- Streamlit (UI)
- Sentence Transformers (semantic similarity / NLP)
- LanguageTool (grammar checking)
- pdfplumber / python-docx (file parsing)

## Project Structure
```
resume-analyzer/
├── app.py                 # Main Streamlit app - UI & entry point
├── extractor.py            # Extracts text from PDF/DOCX + splits into sections
├── ats_scorer.py            # ATS scoring logic (rule-based scoring engine)
├── grammar_checker.py       # Grammar checking using LanguageTool
├── skills_matcher.py        # Sentence Transformers - skill extraction & JD comparison
├── skills_data.py           # Static data: skills list + section header keywords
├── requirements.txt         # Python dependencies
└── sample_resumes/          # Test resumes
```

## How to Run

1. Create and activate a virtual environment:
   ```
   python -m venv venv
   venv\Scripts\activate      (Windows)
   source venv/bin/activate   (Mac/Linux)
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the app:
   ```
   streamlit run app.py
   ```

4. Open the browser at `http://localhost:8501`

## Architecture

```
Resume Upload (PDF/DOCX)
        ↓
Text Extraction (pdfplumber/python-docx)
        ↓
Section Splitting (regex-based header detection)
        ↓
   ┌────┴─────┬──────────┬─────────────┐
ATS Scoring  Grammar   Skills Match   JD Comparison
(rule-based) (LanguageTool) (keyword+NLP)  (Sentence Transformers)
        ↓
Streamlit Dashboard (displays results)
```

## Known Limitations / Future Work
- Section detection depends on resume formatting (creative/graphic resumes may confuse it)
- Skill matching is currently exact-match; could be improved with embedding-based fuzzy matching
- Grammar checking is rule-based; could add an LLM pass for tone/impact suggestions
=======
# resume-analyzer
>>>>>>> 5e21dc71368946ae071e09802b43c68d8c0c20c8
