from enum import Enum
from typing import Dict, List, Optional
from pydantic import BaseModel, Field, Extra


class ResumeData(BaseModel):
    name: Optional[str] = ""
    email: Optional[str] = ""
    phone: Optional[str] = ""
    skills: List[str] = []
    experience: List[Dict[str, object]] = []
    projects: List[str] = []
    education: List[str] = []

    model_config = {
        "extra": Extra.ignore,
    }


class JDAnalyzeRequest(BaseModel):
    job_description: Optional[str] = Field(None, description="Job description text")
    resume_data: ResumeData


class JDAnalyzeResponse(BaseModel):
    role: str
    must_have_skills: List[str]
    optional_skills: List[str]
    weighted_keywords: Dict[str, float]


class SkillImportance(str, Enum):
    must_have = "must_have"
    optional = "optional"
