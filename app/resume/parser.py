import re
from pathlib import Path
from typing import Dict, List
import spacy
from spacy.language import Language


def _load_spacy_model() -> Language:
    try:
        return spacy.load("en_core_web_sm")
    except OSError:
        return spacy.blank("en")


NLP = _load_spacy_model()


class ResumeParser:
    SKILL_KEYWORDS = {
        "python",
        "django",
        "fastapi",
        "sql",
        "postgresql",
        "aws",
        "docker",
        "kubernetes",
        "rest",
        "graphql",
        "javascript",
        "typescript",
        "react",
        "html",
        "css",
        "git",
        "tensorflow",
        "pandas",
        "numpy",
        "machine learning",
        "nlp",
        "data analysis",
        "microservices",
        "ci/cd",
    }

    SECTION_HEADERS = {
        "skills": ["skills", "technical skills", "toolkit", "technologies"],
        "experience": ["experience", "work experience", "professional experience"],
        "education": ["education", "academic background", "education and training"],
        "projects": ["projects", "project experience", "selected projects"],
    }

    @staticmethod
    def parse(text: str) -> Dict[str, object]:
        normalized = text.strip()
        if not normalized:
            raise ValueError("Resume text extraction produced no usable content.")

        sections = ResumeParser._split_sections(normalized)
        name = ResumeParser._extract_name(normalized, sections)
        email = ResumeParser._extract_email(normalized)
        phone = ResumeParser._extract_phone(normalized)
        skills = ResumeParser._extract_skills(sections.get("skills", "") or normalized)
        experience = ResumeParser._extract_experience(sections.get("experience", ""))
        education = ResumeParser._extract_education(sections.get("education", ""))
        projects = ResumeParser._extract_projects(sections.get("projects", ""))

        return {
            "name": name,
            "email": email,
            "phone": phone,
            "skills": skills,
            "experience": experience,
            "projects": projects,
            "education": education,
        }

    @staticmethod
    def _split_sections(text: str) -> Dict[str, str]:
        lines = text.splitlines()
        sections: Dict[str, str] = {key: "" for key in ResumeParser.SECTION_HEADERS}
        current_section = None

        for line in lines:
            stripped = line.strip()
            if not stripped:
                continue

            lower = stripped.lower()
            matched = next(
                (section for section, headers in ResumeParser.SECTION_HEADERS.items() if lower in headers),
                None,
            )
            if matched:
                current_section = matched
                continue

            if current_section:
                sections[current_section] += stripped + "\n"

        return sections

    @staticmethod
    def _extract_email(text: str) -> str:
        match = re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text)
        return match.group(0) if match else ""

    @staticmethod
    def _extract_phone(text: str) -> str:
        pattern = re.compile(
            r"(?:\+?\d{1,3}[\s.-])?(?:\(?\d{2,4}\)?[\s.-])?\d{3,4}[\s.-]?\d{3,4}"
        )
        for match in pattern.finditer(text):
            phone_text = match.group(0).strip()
            digits = re.sub(r"[^0-9]", "", phone_text)
            if len(digits) >= 10:
                return phone_text
        return ""

    @staticmethod
    def _extract_name(text: str, sections: Dict[str, str]) -> str:
        candidate_text = text[:1600]
        doc = NLP(candidate_text)
        person_entities = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]
        if person_entities:
            return person_entities[0]

        first_line = next((line.strip() for line in text.splitlines() if line.strip()), "")
        return first_line

    @staticmethod
    def _extract_skills(text: str) -> List[str]:
        lower_text = text.lower()
        found = sorted({skill for skill in ResumeParser.SKILL_KEYWORDS if skill in lower_text})
        return found

    @staticmethod
    def _extract_experience(text: str) -> List[Dict[str, object]]:
        blocks = [block.strip() for block in re.split(r"\n\s*\n+", text) if block.strip()]
        experience = []

        for block in blocks:
            lines = [line.strip() for line in block.splitlines() if line.strip()]
            if not lines:
                continue

            role, company, duration = ResumeParser._parse_experience_header(lines[0])
            bullets = [line.lstrip("-•* ").strip() for line in lines[1:] if line]
            if not bullets and len(lines) > 1:
                bullets = lines[1:]

            experience.append(
                {
                    "role": role,
                    "company": company,
                    "duration": duration,
                    "bullets": bullets,
                }
            )

        return experience

    @staticmethod
    def _parse_experience_header(line: str) -> tuple[str, str, str]:
        patterns = [
            r"^(?P<role>.+?)\s+at\s+(?P<company>.+?)(?:\s+[\|-–]\s+(?P<duration>.+))?$",
            r"^(?P<role>.+?)\s+[\|-–]\s+(?P<company>.+?)(?:\s+[\|-–]\s+(?P<duration>.+))?$",
            r"^(?P<role>.+?)\s+\|\s+(?P<company>.+?)(?:\s+\|\s+(?P<duration>.+))?$",
        ]
        for pattern in patterns:
            match = re.match(pattern, line)
            if match:
                return (
                    match.group("role").strip(),
                    match.group("company").strip(),
                    (match.group("duration") or "").strip(),
                )

        return line, "", ""

    @staticmethod
    def _extract_education(text: str) -> List[str]:
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        keywords = [
            "university",
            "college",
            "school",
            "bachelor",
            "master",
            "mba",
            "phd",
            "degree",
            "certification",
            "certifications",
        ]
        education = [line for line in lines if any(keyword in line.lower() for keyword in keywords)]
        return education

    @staticmethod
    def _extract_projects(text: str) -> List[str]:
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        if not lines:
            return []

        projects = []
        for line in lines:
            if re.search(r"\b(project|built|developed|designed)\b", line.lower()):
                projects.append(line)
        return projects
