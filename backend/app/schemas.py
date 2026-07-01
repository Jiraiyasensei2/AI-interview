from pydantic import BaseModel, Field


class MatchRequest(BaseModel):
    resume_text: str = Field(..., description="Raw extracted resume text")
    job_description: str = Field(..., description="Raw job description text")


class SkillGap(BaseModel):
    matched_skills: list[str]
    missing_skills: list[str]
    resume_only_skills: list[str]


class MatchResponse(BaseModel):
    match_score: float = Field(..., description="0-100 semantic similarity score")
    skill_gap: SkillGap
    verdict: str


class ParseResponse(BaseModel):
    filename: str
    extracted_text: str
    char_count: int
