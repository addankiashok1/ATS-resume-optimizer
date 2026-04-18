from typing import Dict

PROMPT_TEMPLATE = """You are an ATS-friendly resume optimizer.

Given a parsed resume JSON and job description keyword data, generate an optimized resume structure in JSON only.

Rules:
- Do NOT add any new skills, job titles, companies, dates, metrics, or experience that are not already present in the resume_data.
- Do NOT invent achievements, metrics, or accomplishments.
- Do NOT hallucinate or fabricate details.
- Only rephrase, clarify, and strengthen existing content.
- Keep language simple, ATS-friendly, and readable.
- Prioritize must-have skills from jd_data when they are already present or clearly implied in the resume.
- If a keyword is implied in the resume but not explicitly listed, include it only when it matches the existing content.
- Do not add unrelated technologies, tools, or skills.
- Reorder experience entries so the most relevant roles appear first, based on the job description.
- If jd_data.role is provided, emphasize relevance to that role without inventing new responsibilities.
- Maintain the output structure exactly as a JSON object with these fields and no extra keys: summary, skills, experience, projects, education.

Output format example:
{
  "summary": "...",
  "skills": ["..."],
  "experience": [
    {
      "role": "...",
      "company": "...",
      "bullets": ["..."]
    }
  ],
  "projects": [
    {
      "name": "...",
      "description": "...",
      "bullets": ["..."]
    }
  ],
  "education": [
    {
      "degree": "...",
      "institution": "...",
      "year": "...",
      "details": "..."
    }
  ]
}

resume_data: {resume_data}
jd_data: {jd_data}

Respond with only the optimized resume JSON object and nothing else."""


def build_optimization_prompt(resume_data: Dict[str, object], jd_data: Dict[str, object]) -> str:
    structured_resume = {
        "summary": resume_data.get("summary", ""),
        "skills": resume_data.get("skills", []),
        "experience": resume_data.get("experience", []),
        "projects": resume_data.get("projects", []),
        "education": resume_data.get("education", []),
    }
    structured_jd = {
        "role": jd_data.get("role", ""),
        "must_have_skills": jd_data.get("must_have_skills", []),
        "optional_skills": jd_data.get("optional_skills", []),
        "weighted_keywords": jd_data.get("weighted_keywords", {}),
    }
    return PROMPT_TEMPLATE.format(resume_data=structured_resume, jd_data=structured_jd)
