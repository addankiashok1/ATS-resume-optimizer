from typing import List
from pydantic import BaseModel


class ExperienceItem(BaseModel):
    role: str = ""
    company: str = ""
    duration: str = ""
    bullets: List[str] = []


class ResumeData(BaseModel):
    name: str = ""
    email: str = ""
    phone: str = ""
    skills: List[str] = []
    experience: List[ExperienceItem] = []
    projects: List[str] = []
    education: List[str] = []


class ResumeParseResponse(BaseModel):
    status: str = "success"
    parsed_data: ResumeData
