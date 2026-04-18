import re
from typing import Dict, List, Tuple
import spacy
from spacy.language import Language


def _load_spacy_model() -> Language:
    try:
        return spacy.load("en_core_web_sm")
    except OSError:
        return spacy.blank("en")


NLP = _load_spacy_model()


class JDParser:
    KEYWORD_CANDIDATES = {
        "python",
        "sql",
        "aws",
        "docker",
        "kubernetes",
        "spark",
        "kafka",
        "hadoop",
        "react",
        "angular",
        "vue",
        "javascript",
        "typescript",
        "java",
        "spring",
        "nodejs",
        "fastapi",
        "django",
        "flask",
        "pandas",
        "numpy",
        "scikit-learn",
        "tensorflow",
        "pytorch",
        "nlp",
        "rest",
        "graphql",
        "git",
        "jenkins",
        "ci/cd",
        "azure",
        "gcp",
        "docker-compose",
        "linux",
        "microservices",
        "data engineering",
        "etl",
        "tableau",
        "power bi",
    }

    ROLE_TERMS = {
        "data engineer",
        "data scientist",
        "machine learning engineer",
        "frontend developer",
        "backend developer",
        "full stack developer",
        "devops engineer",
        "software engineer",
        "product manager",
        "business analyst",
    }

    REQUIRED_INDICATORS = [
        "must have",
        "required",
        "required skills",
        "requirements",
        "strong knowledge",
        "experience with",
    ]

    OPTIONAL_INDICATORS = [
        "nice to have",
        "preferred",
        "optional",
        "would be a plus",
        "nice-to-have",
    ]

    @staticmethod
    def normalize(text: str) -> str:
        return re.sub(r"\s+", " ", (text or "").strip()).lower()

    @staticmethod
    def split_sections(text: str) -> Dict[str, str]:
        normalized = JDParser.normalize(text)
        sections = {
            "requirements": "",
            "nice_to_have": "",
            "other": "",
        }
        current = "other"
        for line in normalized.split("\n"):
            line = line.strip()
            if not line:
                continue

            if any(indicator in line for indicator in JDParser.REQUIRED_INDICATORS):
                current = "requirements"
            elif any(indicator in line for indicator in JDParser.OPTIONAL_INDICATORS):
                current = "nice_to_have"

            sections[current] += line + "\n"

        return sections

    @staticmethod
    def extract_keywords(text: str) -> Dict[str, Dict[str, object]]:
        normalized = JDParser.normalize(text)
        if not normalized:
            return {}

        sections = JDParser.split_sections(normalized)
        keyword_info = {}

        for keyword in JDParser.KEYWORD_CANDIDATES:
            pattern = rf"\b{re.escape(keyword)}\b"
            if re.search(pattern, normalized):
                count = len(re.findall(pattern, normalized))
                first_pos = normalized.find(keyword)
                in_requirements = bool(re.search(pattern, sections["requirements"]))
                in_optional = bool(re.search(pattern, sections["nice_to_have"]))
                keyword_info[keyword] = {
                    "count": count,
                    "first_position": first_pos if first_pos >= 0 else len(normalized),
                    "required_section": in_requirements,
                    "optional_section": in_optional,
                }

        doc = NLP(normalized)
        for ent in doc.ents:
            label = ent.label_.upper()
            if label in {"ORG", "PRODUCT", "WORK_OF_ART", "NORP"}:
                candidate = ent.text.strip().lower()
                if candidate not in keyword_info and len(candidate.split()) <= 3:
                    count = normalized.count(candidate)
                    if count:
                        keyword_info[candidate] = {
                            "count": count,
                            "first_position": normalized.find(candidate),
                            "required_section": bool(re.search(rf"\b{re.escape(candidate)}\b", sections["requirements"])),
                            "optional_section": bool(re.search(rf"\b{re.escape(candidate)}\b", sections["nice_to_have"])),
                        }

        return keyword_info

    @staticmethod
    def extract_role_terms(text: str) -> List[str]:
        normalized = JDParser.normalize(text)
        roles = []
        for role in JDParser.ROLE_TERMS:
            if role in normalized:
                roles.append(role.title())
        return roles
