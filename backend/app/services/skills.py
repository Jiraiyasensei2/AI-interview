"""
Interpretable skill-gap detection.

Embeddings give a strong *overall* match score, but interviewers (and real
recruiters) also want a human-readable breakdown: which skills matched,
which are missing. This module does simple, fast keyword matching against
a curated taxonomy (see app/config.py) to produce that breakdown.

This is intentionally simple (not ML) — it's the right tool for this job:
fast, deterministic, and easy to extend. Mention in interviews that a next
step would be fuzzy/embedding-based skill matching to catch synonyms
("k8s" vs "kubernetes") that exact keyword matching misses.
"""
import re

from app.config import SKILLS_TAXONOMY
from app.schemas import SkillGap


def _normalize(text: str) -> str:
    return re.sub(r"[^a-z0-9+.# ]", " ", text.lower())


def extract_skills(text: str) -> set[str]:
    normalized = _normalize(text)
    found = set()
    for skill in SKILLS_TAXONOMY:
        # word-boundary-ish match so "go" doesn't match inside "gorgeous"
        pattern = r"(?<![a-z0-9])" + re.escape(skill.lower()) + r"(?![a-z0-9])"
        if re.search(pattern, normalized):
            found.add(skill)
    return found


def compute_skill_gap(resume_text: str, job_description: str) -> SkillGap:
    resume_skills = extract_skills(resume_text)
    jd_skills = extract_skills(job_description)

    matched = sorted(resume_skills & jd_skills)
    missing = sorted(jd_skills - resume_skills)
    resume_only = sorted(resume_skills - jd_skills)

    return SkillGap(
        matched_skills=matched,
        missing_skills=missing,
        resume_only_skills=resume_only,
    )
