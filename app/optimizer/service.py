import json
import re
from typing import Any, Dict, List, Set, Tuple
from app.optimizer.schemas import OptimizeRequest, ResumeData
from app.optimizer.prompt_builder import build_optimization_prompt
from app.utils.ai_client import AIClient


class OptimizerService:
    ai_client = AIClient()

    @staticmethod
    def optimize(payload: OptimizeRequest) -> Dict[str, Any]:
        resume_data = payload.resume_data.model_dump()
        jd_data = payload.jd_data.model_dump()
        prompt = build_optimization_prompt(resume_data, jd_data)

        response_text = OptimizerService.ai_client.complete(prompt)
        parsed = OptimizerService._extract_json(response_text)

        optimized = OptimizerService._validate_optimized_resume(parsed, resume_data)
        return {"status": "success", "optimized_resume": optimized.model_dump()}

    @staticmethod
    def _extract_json(raw_text: str) -> Dict[str, Any]:
        try:
            return json.loads(raw_text)
        except json.JSONDecodeError:
            start = raw_text.find("{")
            end = raw_text.rfind("}")
            if start == -1 or end == -1:
                raise ValueError("AI output was not valid JSON.")
            try:
                return json.loads(raw_text[start:end + 1])
            except json.JSONDecodeError as exc:
                raise ValueError(f"Unable to parse AI output as JSON: {exc}") from exc

    @staticmethod
    def _validate_optimized_resume(parsed: Dict[str, Any], original_resume: Dict[str, Any]) -> ResumeData:
        OptimizerService._validate_structure(parsed)
        optimized = ResumeData.model_validate(parsed)

        OptimizerService._ensure_skills_subset(optimized.skills, original_resume)
        OptimizerService._ensure_experience_matches(optimized.experience, original_resume.get("experience", []))
        OptimizerService._ensure_projects_match(optimized.projects, original_resume.get("projects", []))
        OptimizerService._ensure_education_match(optimized.education, original_resume.get("education", []))

        OptimizerService._ensure_no_hallucinated_metrics(parsed, original_resume)
        return optimized

    @staticmethod
    def _validate_structure(parsed: Dict[str, Any]) -> None:
        allowed_fields = {"summary", "skills", "experience", "projects", "education"}
        if set(parsed.keys()) != allowed_fields:
            raise ValueError(
                "AI output must contain only the keys: summary, skills, experience, projects, education."
            )

    @staticmethod
    def _ensure_skills_subset(optimized_skills: List[str], original_resume: Dict[str, Any]) -> None:
        original_skills = {skill.strip().lower() for skill in original_resume.get("skills", []) if isinstance(skill, str)}
        new_skills = [skill for skill in optimized_skills if skill.strip().lower() not in original_skills]
        if new_skills:
            raise ValueError(
                f"Optimized resume contains skills not present in original resume: {new_skills}"
            )

    @staticmethod
    def _ensure_experience_matches(optimized_experience: List[Any], original_experience: List[Dict[str, Any]]) -> None:
        if len(optimized_experience) != len(original_experience):
            raise ValueError("Optimized experience must preserve the same number of experience entries.")

        lower_original: Set[Tuple[str, str]] = {
            (
                str(entry.get("role", "")).strip().lower(),
                str(entry.get("company", "")).strip().lower(),
            )
            for entry in original_experience
            if entry.get("role") is not None and entry.get("company") is not None
        }

        optimized_pairs = {
            (
                entry.role.strip().lower(),
                entry.company.strip().lower(),
            )
            for entry in optimized_experience
        }

        if not optimized_pairs.issubset(lower_original):
            raise ValueError("Optimized experience contains entries not present in the original resume.")

    @staticmethod
    def _ensure_projects_match(optimized_projects: List[Any], original_projects: List[Dict[str, Any]]) -> None:
        if len(original_projects) == 0:
            return
        if len(optimized_projects) != len(original_projects):
            raise ValueError("Optimized projects must preserve the same number of project entries.")

    @staticmethod
    def _ensure_education_match(optimized_education: List[Any], original_education: List[Dict[str, Any]]) -> None:
        if len(original_education) == 0:
            return
        if len(optimized_education) != len(original_education):
            raise ValueError("Optimized education must preserve the same number of education entries.")

    @staticmethod
    def _ensure_no_hallucinated_metrics(parsed: Dict[str, Any], original_resume: Dict[str, Any]) -> None:
        original_text = " ".join(
            [str(item) for item in original_resume.get("skills", [])]
            + [str(original_resume.get("summary", ""))]
            + [str(entry.get("role", "")) + " " + str(entry.get("company", "")) + " " + " ".join(entry.get("bullets", [])) for entry in original_resume.get("experience", [])]
        ).lower()

        hallucinatory_tokens = ["won ", "generated ", "spearheaded ", "achieved ", "%", "million", "billion"]
        new_metrics = [token for token in hallucinatory_tokens if token in str(parsed).lower() and token not in original_text]
        if new_metrics:
            raise ValueError("Optimized resume may include fabricated metrics or achievements.")
