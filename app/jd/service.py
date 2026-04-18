from typing import Dict
from app.jd.parser import JDParser
from app.jd.classifier import JDClassifier
from app.jd.schemas import JDAnalyzeRequest


class JDService:
    @staticmethod
    def analyze(payload: JDAnalyzeRequest) -> Dict[str, object]:
        job_description = (payload.job_description or "").strip()
        resume_data = payload.resume_data.model_dump() if hasattr(payload.resume_data, "model_dump") else payload.resume_data

        if not resume_data or not isinstance(resume_data, dict):
            raise ValueError("Invalid resume_data provided.")

        if job_description:
            keywords = JDParser.extract_keywords(job_description)
            if not keywords:
                raise ValueError("Unable to extract keywords from the provided job description.")

            classification = JDClassifier.classify_keywords(keywords)
            weights = JDClassifier.weight_keywords(keywords, job_description)
            role_candidates = JDParser.extract_role_terms(job_description)
            role = role_candidates[0] if role_candidates else JDClassifier.infer_role_from_resume(resume_data)

            return {
                "role": role,
                "must_have_skills": classification["must_have_skills"],
                "optional_skills": classification["optional_skills"],
                "weighted_keywords": weights,
            }

        role = JDClassifier.infer_role_from_resume(resume_data)
        skills = resume_data.get("skills", []) if isinstance(resume_data.get("skills", []), list) else []
        return {
            "role": role,
            "must_have_skills": [skill.title() for skill in skills],
            "optional_skills": [],
            "weighted_keywords": {skill.title(): 0.5 for skill in skills},
        }
