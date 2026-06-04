
"""Skill extraction utilities."""

from __future__ import annotations

import re
from typing import Iterable

import spacy


DEFAULT_SKILLS = [

    # Frontend
    "HTML",
    "CSS",
    "JavaScript",
    "React",
    "Angular",
    "Vue",
    "Bootstrap",
    "Tailwind CSS",

    # Backend
    "Python",
    "Java",
    "Node.js",
    "Django",
    "Flask",

    # Database
    "SQL",
    "MySQL",
    "MongoDB",
    "PostgreSQL",

    # AI / Data
    "Machine Learning",
    "Deep Learning",
    "NLP",
    "Data Analysis",
    "Power BI",
    "Tableau",
    "Excel",

    # Tools
    "Git",
    "GitHub",
]


ROLE_SKILLS = {

    "frontend developer": [
        "HTML",
        "CSS",
        "JavaScript",
        "React",
        "Bootstrap",
        "Git",
        "GitHub",
    ],

    "backend developer": [
        "Python",
        "Java",
        "Node.js",
        "SQL",
        "Django",
        "Flask",
    ],

    "data scientist": [
        "Python",
        "Machine Learning",
        "Deep Learning",
        "NLP",
        "SQL",
        "Power BI",
        "Tableau",
        "Excel",
    ],
}


SKILL_ALIASES = {

    "HTML": [r"html"],
    "CSS": [r"css"],
    "JavaScript": [r"javascript", r"js"],
    "React": [r"react", r"reactjs", r"react\.js"],
    "Angular": [r"angular"],
    "Vue": [r"vue"],
    "Bootstrap": [r"bootstrap"],
    "Tailwind CSS": [r"tailwind"],

    "Python": [r"python"],
    "Java": [r"java"],

    "Node.js": [r"node", r"nodejs", r"node\.js"],

    "SQL": [
        r"sql",
        r"mysql",
        r"postgresql",
        r"postgres",
        r"sqlite",
        r"sql server"
    ],

    "MySQL": [r"mysql"],
    "MongoDB": [r"mongodb"],
    "PostgreSQL": [r"postgresql"],

    "Power BI": [r"power\s*bi", r"powerbi"],
    "Tableau": [r"tableau"],

    "Machine Learning": [r"machine\s+learning", r"\bml\b"],

    "NLP": [
        r"\bnlp\b",
        r"natural\s+language\s+processing"
    ],

    "Excel": [
        r"excel",
        r"microsoft\s+excel"
    ],

    "Data Analysis": [
        r"data\s+analysis",
        r"analytics"
    ],

    "Deep Learning": [
        r"deep\s+learning",
        r"neural\s+network"
    ],

    "Git": [r"\bgit\b"],
    "GitHub": [r"github"],

    "Django": [r"django"],
    "Flask": [r"flask"],
}


try:
    NLP = spacy.load("en_core_web_sm")

except OSError:
    NLP = spacy.blank("en")
    NLP.add_pipe("sentencizer")


def normalize_text(text: str) -> str:

    text = text or ""
    return re.sub(r"\s+", " ", text).strip()


def extract_skills(
    text: str,
    required_skills: Iterable[str] | None = None
) -> list[str]:

    normalized = normalize_text(text).lower()

    skills_to_check = list(required_skills or DEFAULT_SKILLS)

    found_skills = []

    for skill in skills_to_check:

        patterns = SKILL_ALIASES.get(
            skill,
            [re.escape(skill.lower())]
        )

        if any(
            re.search(
                rf"(?<!\w){pattern}(?!\w)",
                normalized
            )
            for pattern in patterns
        ):
            found_skills.append(skill)

    return sorted(set(found_skills), key=str.lower)


def extract_skills_from_job_description(job_description: str) -> list[str]:

    jd_lower = job_description.lower()

    detected_skills = []

    # Detect role-based skills
    for role, skills in ROLE_SKILLS.items():

        role_words = role.split()

        # Match all words from role
        if all(word in jd_lower for word in role_words):
            detected_skills.extend(skills)

    # Detect directly mentioned skills
    direct_skills = extract_skills(
        job_description,
        DEFAULT_SKILLS
    )

    detected_skills.extend(direct_skills)

    # Remove duplicates
    detected_skills = list(set(detected_skills))

    return detected_skills

def get_missing_skills(
    found_skills: Iterable[str],
    required_skills: Iterable[str]
) -> list[str]:

    found_set = {
        skill.lower()
        for skill in found_skills
    }

    return [
        skill
        for skill in required_skills
        if skill.lower() not in found_set
    ]


def create_resume_summary(
    text: str,
    max_sentences: int = 3
) -> str:

    cleaned = normalize_text(text)

    if not cleaned:
        return "No readable text found."

    doc = NLP(cleaned)

    sentences = [
        sent.text.strip()
        for sent in doc.sents
        if len(sent.text.strip()) > 30
    ]

    summary = " ".join(sentences[:max_sentences])

    return summary or cleaned[:450]
