from contextlib import asynccontextmanager

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from app.config import ALLOWED_ORIGINS
from app.schemas import MatchRequest, MatchResponse, ParseResponse
from app.services.embeddings import get_model, semantic_match_score
from app.services.parser import extract_text
from app.services.skills import compute_skill_gap


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Warm up the embedding model once at startup so the first real request
    # isn't slow (model download/load can take a few seconds).
    get_model()
    yield


app = FastAPI(
    title="HireLens-AI",
    description="Embedding-based resume ↔ job description matching and skill-gap analysis.",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/parse-resume", response_model=ParseResponse)
async def parse_resume(file: UploadFile = File(...)):
    """Extract raw text from an uploaded resume (.pdf or .txt)."""
    file_bytes = await file.read()
    try:
        text = extract_text(file.filename, file_bytes)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    if not text:
        raise HTTPException(
            status_code=422,
            detail="Could not extract any text — the PDF may be a scanned image.",
        )

    return ParseResponse(filename=file.filename, extracted_text=text, char_count=len(text))


@app.post("/match", response_model=MatchResponse)
def match(payload: MatchRequest):
    """
    Compare a resume against a job description:
    - semantic similarity score (sentence-transformers embeddings)
    - interpretable skill-gap breakdown (matched / missing / extra skills)
    """
    if not payload.resume_text.strip() or not payload.job_description.strip():
        raise HTTPException(status_code=400, detail="resume_text and job_description are required.")

    score = semantic_match_score(payload.resume_text, payload.job_description)
    gap = compute_skill_gap(payload.resume_text, payload.job_description)

    if score >= 75:
        verdict = "Strong match"
    elif score >= 50:
        verdict = "Partial match — some skill gaps to address"
    else:
        verdict = "Weak match"

    return MatchResponse(match_score=score, skill_gap=gap, verdict=verdict)
