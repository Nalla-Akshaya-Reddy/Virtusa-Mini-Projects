
import re
import json
import sqlite3
from pathlib import Path
from datetime import datetime

import pdfplumber
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

nltk.download("punkt", quiet=True)
nltk.download("stopwords", quiet=True)
nltk.download("punkt_tab", quiet=True)

DB_PATH = Path(__file__).parent / "data" / "history.db"

#Creating a tech skill word bank for skill assessment
SKILL_BANK = {
    "programming": [
        "python", "java", "javascript", "typescript", "c++", "c#", "golang",
        "ruby", "php", "swift", "kotlin", "rust", "scala", "r", "matlab",
    ],
    "web": [
        "html", "css", "react", "angular", "vue", "django", "flask", "fastapi",
        "node.js", "express", "spring", "rest", "graphql", "bootstrap", "tailwind",
    ],
    "data": [
        "sql", "mysql", "postgresql", "mongodb", "redis", "elasticsearch",
        "pandas", "numpy", "scikit-learn", "tensorflow", "pytorch", "keras",
        "tableau", "power bi", "spark", "hadoop", "kafka",
    ],
    "devops": [
        "docker", "kubernetes", "aws", "azure", "gcp", "ci/cd", "jenkins",
        "github actions", "terraform", "ansible", "linux", "bash",
    ],
    "soft_skills": [
        "communication", "teamwork", "leadership", "problem solving",
        "agile", "scrum", "project management", "analytical",
    ],
}

ALL_SKILLS = [skill for group in SKILL_BANK.values() for skill in group]

#Creating a database
def init_db():
    DB_PATH.parent.mkdir(exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS analyses (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            filename  TEXT,
            job_role  TEXT,
            score     REAL,
            skills    TEXT,
            missing   TEXT,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()


def save_analysis(filename, job_role, score, skills, missing):
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT INTO analyses (filename, job_role, score, skills, missing, timestamp) VALUES (?,?,?,?,?,?)",
        (filename, job_role, round(score, 1),
         json.dumps(skills), json.dumps(missing),
         datetime.now().strftime("%Y-%m-%d %H:%M")),
    )
    conn.commit()
    conn.close()


def get_history():
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute(
        "SELECT filename, job_role, score, timestamp FROM analyses ORDER BY id DESC LIMIT 10"
    ).fetchall()
    conn.close()
    return [{"filename": r[0], "job_role": r[1], "score": r[2], "timestamp": r[3]} for r in rows]


# PDF Extraction
def extract_text_from_pdf(pdf_path: str) -> str:
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text.strip()


#Keyword Extraction
def extract_skills(text: str) -> dict:
    text_lower = text.lower()
    found = {cat: [] for cat in SKILL_BANK}
    for category, skills in SKILL_BANK.items():
        for skill in skills:
            # whole-word match
            pattern = r'\b' + re.escape(skill) + r'\b'
            if re.search(pattern, text_lower):
                found[category].append(skill)
    return found


def extract_contact_info(text: str) -> dict:
    email = re.findall(r'[\w.+-]+@[\w-]+\.[a-zA-Z]{2,}', text)
    phone = re.findall(r'[\+]?[\d][\d\s\-().]{8,14}[\d]', text)
    linkedin = re.findall(r'linkedin\.com/in/[\w-]+', text, re.I)
    github = re.findall(r'github\.com/[\w-]+', text, re.I)
    return {
        "email": email[0] if email else None,
        "phone": phone[0].strip() if phone else None,
        "linkedin": linkedin[0] if linkedin else None,
        "github": github[0] if github else None,
    }


def extract_sections(text: str) -> dict:
    section_headers = {
        "education": r'(education|academic|qualification)',
        "experience": r'(experience|employment|work history)',
        "projects": r'(project|portfolio)',
        "certifications": r'(certif|license|award)',
    }
    found = {}
    for key, pattern in section_headers.items():
        found[key] = bool(re.search(pattern, text, re.I))
    return found


#Assigning Scores
def compute_match_score(resume_text: str, job_description: str) -> float:
    """TF-IDF cosine similarity, scaled to 0-100."""
    vectorizer = TfidfVectorizer(stop_words="english")
    try:
        tfidf = vectorizer.fit_transform([resume_text, job_description])
        similarity = cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]
        return round(similarity * 100, 1)
    except Exception:
        return 0.0


def find_missing_skills(resume_text: str, job_description: str) -> list:
    """Return skills mentioned in JD but absent from resume."""
    jd_lower = job_description.lower()
    resume_lower = resume_text.lower()
    missing = []
    for skill in ALL_SKILLS:
        pattern = r'\b' + re.escape(skill) + r'\b'
        in_jd = bool(re.search(pattern, jd_lower))
        in_resume = bool(re.search(pattern, resume_lower))
        if in_jd and not in_resume:
            missing.append(skill)
    return missing


# Suggetions for improvement
def generate_suggestions(score: float, missing: list, sections: dict, contact: dict) -> list:
    tips = []

    if score < 40:
        tips.append("Your resume has low keyword overlap with the job description. Tailor it more closely to the role.")
    elif score < 65:
        tips.append("Good start — add more role-specific keywords to push past the 65% threshold.")
    else:
        tips.append("Strong match! Keep your resume focused and quantify achievements where possible.")

    if missing:
        top = missing[:5]
        tips.append(f"Consider adding these skills if you know them: {', '.join(top)}.")

    if not sections.get("projects"):
        tips.append("Add a Projects section — it's one of the most important sections for freshers.")
    if not sections.get("certifications"):
        tips.append("Include certifications (Coursera, Udemy, etc.) to strengthen your profile.")
    if not contact.get("github"):
        tips.append("Add your GitHub profile link — it shows practical work to recruiters.")
    if not contact.get("linkedin"):
        tips.append("Add your LinkedIn URL for professional credibility.")

    return tips

#Main
def analyze(pdf_path: str, job_description: str, job_role: str = "General") -> dict:
    init_db()

    resume_text = extract_text_from_pdf(pdf_path)
    if not resume_text:
        raise ValueError("Could not extract text from the PDF. Ensure it's not a scanned image.")

    skills_found = extract_skills(resume_text)
    contact = extract_contact_info(resume_text)
    sections = extract_sections(resume_text)
    score = compute_match_score(resume_text, job_description)
    missing = find_missing_skills(resume_text, job_description)
    suggestions = generate_suggestions(score, missing, sections, contact)

    all_found_skills = [s for group in skills_found.values() for s in group]

    result = {
        "score": score,
        "contact": contact,
        "sections": sections,
        "skills": skills_found,
        "all_skills": all_found_skills,
        "missing_skills": missing[:10],
        "suggestions": suggestions,
        "word_count": len(resume_text.split()),
    }

    save_analysis(
        filename=Path(pdf_path).name,
        job_role=job_role,
        score=score,
        skills=all_found_skills,
        missing=missing[:10],
    )

    return result
