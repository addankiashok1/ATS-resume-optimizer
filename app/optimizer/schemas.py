from typing import Dict, List, Optional
from pydantic import BaseModel, Field, Extra


class ExperienceEntry(BaseModel):
    role: str = Field(...)
    company: str = Field(...)
    bullets: List[str] = Field(default_factory=list)
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    details: Optional[str] = None

    model_config = {
        "extra": Extra.ignore,
    }


class ProjectEntry(BaseModel):
    name: Optional[str] = ""
    description: Optional[str] = ""
    bullets: List[str] = Field(default_factory=list)

    model_config = {
        "extra": Extra.ignore,
    }


class EducationEntry(BaseModel):
    degree: Optional[str] = ""
    institution: Optional[str] = ""
    year: Optional[str] = None
    details: Optional[str] = None

    model_config = {
        "extra": Extra.ignore,
    }


class ResumeData(BaseModel):
    summary: str = ""
    skills: List[str] = Field(default_factory=list)
    experience: List[ExperienceEntry] = Field(default_factory=list)
    projects: List[ProjectEntry] = Field(default_factory=list)
    education: List[EducationEntry] = Field(default_factory=list)

    model_config = {
        "extra": Extra.ignore,
    }


class JDData(BaseModel):
    role: Optional[str] = ""
    must_have_skills: List[str] = Field(default_factory=list)
    optional_skills: List[str] = Field(default_factory=list)
    weighted_keywords: Dict[str, float] = Field(default_factory=dict)

    model_config = {
        "extra": Extra.ignore,
    }


class OptimizeRequest(BaseModel):
    resume_data: ResumeData
    jd_data: JDData


class OptimizeResponse(BaseModel):
    status: str
    optimized_resume: ResumeData
