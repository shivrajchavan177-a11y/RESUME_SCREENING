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
    "Spring Boot",

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
    "TensorFlow",
    "PyTorch",

    # DevOps / Cloud
    "Linux",
    "Docker",
    "Kubernetes",
    "AWS",
    "Azure",
    "CI/CD",
    "Jenkins",
    "Terraform",

    # Mobile
    "Kotlin",
    "Firebase",
    "Swift",
    "Xcode",
    "Android Studio",

    # UI/UX
    "Figma",
    "UI/UX",
    "Wireframing",
    "Prototyping",

    # Testing
    "Selenium",
    "Automation Testing",
    "Manual Testing",

    # Networking / Security
    "Networking",
    "Cyber Security",
    "Ethical Hacking",
    "Cisco",
    "Routing",
    "Switching",

    # Blockchain / Game
    "Solidity",
    "Ethereum",
    "Blockchain",
    "Web3",
    "Unity",
    "C#",
    "Game Development",
    "Blender",

    # Tools
    "Git",
    "GitHub",
]


ROLE_SKILLS = {

    # FRONTEND
    "frontend developer": [
        "HTML",
        "CSS",
        "JavaScript",
        "React",
        "Angular",
        "Vue",
        "Bootstrap",
        "Tailwind CSS",
        "Git",
        "GitHub",
    ],

    # BACKEND
    "backend developer": [
        "Python",
        "Java",
        "Node.js",
        "Django",
        "Flask",
        "Spring Boot",
        "SQL",
        "MySQL",
        "PostgreSQL",
        "MongoDB",
        "Git",
        "GitHub",
    ],

    # FULL STACK
    "full stack developer": [
        "HTML",
        "CSS",
        "JavaScript",
        "React",
        "Node.js",
        "MongoDB",
        "SQL",
        "Git",
        "GitHub",
    ],

    # DATA ANALYST
    "data analyst": [
        "Python",
        "SQL",
        "Excel",
        "Power BI",
        "Tableau",
        "Data Analysis",
    ],

    # DATA SCIENTIST
    "data scientist": [
        "Python",
        "Machine Learning",
        "Deep Learning",
        "NLP",
        "SQL",
        "Power BI",
        "Tableau",
        "Excel",
        "TensorFlow",
        "PyTorch",
    ],

    # MACHINE LEARNING
    "machine learning engineer": [
        "Python",
        "Machine Learning",
        "Deep Learning",
        "TensorFlow",
        "PyTorch",
        "SQL",
        "Git",
    ],

    # AI ENGINEER
    "ai engineer": [
        "Python",
        "Machine Learning",
        "Deep Learning",
        "NLP",
        "TensorFlow",
        "PyTorch",
        "Git",
    ],

    # DEVOPS
    "devops engineer": [
        "Linux",
        "Docker",
        "Kubernetes",
        "AWS",
        "CI/CD",
        "Git",
        "GitHub",
        "Jenkins",
        "Terraform",
    ],

    # CLOUD ENGINEER
    "cloud engineer": [
        "AWS",
        "Azure",
        "Docker",
        "Kubernetes",
        "Linux",
        "Terraform",
    ],

    # CYBER SECURITY
    "cyber security": [
        "Linux",
        "Python",
        "Networking",
        "Cyber Security",
        "Ethical Hacking",
    ],

    # JAVA
    "java developer": [
        "Java",
        "Spring Boot",
        "SQL",
        "Git",
        "GitHub",
    ],

    # PYTHON
    "python developer": [
        "Python",
        "Django",
        "Flask",
        "SQL",
        "Git",
        "GitHub",
    ],

    # WEB DEVELOPER
    "web developer": [
        "HTML",
        "CSS",
        "JavaScript",
        "React",
        "Node.js",
        "Git",
    ],

    # SOFTWARE ENGINEER
    "software engineer": [
        "Python",
        "Java",
        "SQL",
        "Git",
        "GitHub",
    ],

    # ANDROID
    "android developer": [
        "Java",
        "Kotlin",
        "Android Studio",
        "Firebase",
        "Git",
    ],

    # IOS
    "ios developer": [
        "Swift",
        "Xcode",
        "Firebase",
        "Git",
    ],

    # UI UX
    "ui ux designer": [
        "Figma",
        "UI/UX",
        "Wireframing",
        "Prototyping",
    ],

    # QA TESTER
    "qa engineer": [
        "Manual Testing",
        "Automation Testing",
        "Selenium",
        "Java",
        "SQL",
    ],

    # DATABASE
    "database administrator": [
        "SQL",
        "MySQL",
        "PostgreSQL",
        "MongoDB",
    ],

    # NETWORK ENGINEER
    "network engineer": [
        "Networking",
        "Linux",
        "Cisco",
        "Routing",
        "Switching",
    ],

    # BLOCKCHAIN
    "blockchain developer": [
        "Solidity",
        "Ethereum",
        "Blockchain",
        "Web3",
        "JavaScript",
    ],

    # GAME DEV
    "game developer": [
        "Unity",
        "C#",
        "Game Development",
        "Blender",
    ],
}


SKILL_ALIASES = {

    # Frontend
    "HTML": [r"html"],
    "CSS": [r"css"],
    "JavaScript": [r"javascript", r"js"],
    "React": [r"react", r"reactjs", r"react\.js"],
    "Angular": [r"angular"],
    "Vue": [r"vue"],
    "Bootstrap": [r"bootstrap"],
    "Tailwind CSS": [r"tailwind"],

    # Backend
    "Python": [r"python"],
    "Java": [r"java"],
    "Node.js": [r"node", r"nodejs", r"node\.js"],
    "Django": [r"django"],
    "Flask": [r"flask"],
    "Spring Boot": [r"spring boot"],

    # Database
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

    # AI/Data
    "Power BI": [r"power\s*bi", r"powerbi"],
    "Tableau": [r"tableau"],

    "Machine Learning": [
        r"machine\s+learning",
        r"\bml\b"
    ],

    "Deep Learning": [
        r"deep\s+learning",
        r"neural\s+network"
    ],

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

    "TensorFlow": [r"tensorflow"],
    "PyTorch": [r"pytorch"],

    # DevOps / Cloud
    "Linux": [r"linux"],
    "Docker": [r"docker"],
    "Kubernetes": [r"kubernetes", r"k8s"],
    "AWS": [r"aws", r"amazon web services"],
    "Azure": [r"azure"],
    "CI/CD": [r"ci/cd", r"ci cd"],
    "Jenkins": [r"jenkins"],
    "Terraform": [r"terraform"],

    # Mobile
    "Kotlin": [r"kotlin"],
    "Firebase": [r"firebase"],
    "Swift": [r"swift"],
    "Xcode": [r"xcode"],
    "Android Studio": [r"android studio"],

    # UI/UX
    "Figma": [r"figma"],
    "UI/UX": [r"ui/ux", r"ui ux"],
    "Wireframing": [r"wireframing"],
    "Prototyping": [r"prototyping"],

    # Testing
    "Selenium": [r"selenium"],
    "Automation Testing": [r"automation testing"],
    "Manual Testing": [r"manual testing"],

    # Networking / Security
    "Networking": [r"networking"],
    "Cyber Security": [r"cyber security"],
    "Ethical Hacking": [r"ethical hacking"],
    "Cisco": [r"cisco"],
    "Routing": [r"routing"],
    "Switching": [r"switching"],

    # Blockchain / Game
    "Solidity": [r"solidity"],
    "Ethereum": [r"ethereum"],
    "Blockchain": [r"blockchain"],
    "Web3": [r"web3"],
    "Unity": [r"unity"],
    "C#": [r"c#"],
    "Game Development": [r"game development"],
    "Blender": [r"blender"],

    # Tools
    "Git": [r"\bgit\b"],
    "GitHub": [r"github"],
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


def extract_skills_from_job_description(
    job_description: str
) -> list[str]:

    jd_lower = job_description.lower()

    detected_skills = []

    # Detect role-based skills
    for role, skills in ROLE_SKILLS.items():

        role_words = role.split()

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
