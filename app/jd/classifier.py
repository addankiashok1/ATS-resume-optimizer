from typing import Dict, List
from app.jd.parser import JDParser


class JDClassifier:
    @staticmethod
    def classify_keywords(keywords: Dict[str, Dict[str, object]]) -> Dict[str, List[str]]:
        must_have = []
        optional = []

        for keyword, info in keywords.items():
            if info.get("required_section") or info.get("count", 0) > 1:
                must_have.append(keyword.title())
                continue
            if info.get("optional_section"):
                optional.append(keyword.title())
                continue
            if info.get("count", 0) >= 1:
                optional.append(keyword.title())

        return {
            "must_have_skills": sorted(set(must_have)),
            "optional_skills": sorted(set(optional) - set(must_have)),
        }

    @staticmethod
    def weight_keywords(keywords: Dict[str, Dict[str, object]], text: str) -> Dict[str, float]:
        normalized = JDParser.normalize(text)
        weight_map = {}
        length = max(len(normalized), 1)

        for keyword, info in keywords.items():
            frequency = info.get("count", 0)
            position = 1.0 - (info.get("first_position", 0) / length)
            importance = 1.0 if info.get("required_section") else 0.65 if info.get("optional_section") else 0.5
            score = min(1.0, (frequency * 0.35) + (position * 0.35) + (importance * 0.3))
            weight_map[keyword.title()] = round(score, 2)

        return dict(sorted(weight_map.items(), key=lambda item: item[1], reverse=True))

    @staticmethod
    def infer_role_from_resume(resume_data: Dict[str, object]) -> str:
        skills = [skill.lower() for skill in resume_data.get("skills", [])]
        if any(term in skills for term in ["react", "javascript", "typescript", "angular", "vue"]):
            return "Frontend Developer"
        if any(term in skills for term in ["django", "flask", "fastapi", "java", "spring", "nodejs"]):
            return "Backend Developer"
        if any(term in skills for term in ["python", "sql", "spark", "kafka", "etl", "aws"]):
            return "Data Engineer"
        if any(term in skills for term in ["python", "pandas", "tensorflow", "scikit-learn", "nlp"]):
            return "Data Scientist"
        if any(term in skills for term in ["docker", "kubernetes", "ci/cd", "jenkins", "aws", "azure", "gcp"]):
            return "DevOps Engineer"
        if any(term in skills for term in ["qa", "testing", "selenium", "junit"]):
            return "QA Engineer"
        return "Software Engineer"
