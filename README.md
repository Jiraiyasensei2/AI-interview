# ResumeSync

Embedding-based resume ↔ job description matcher with an interpretable skill-gap breakdown.

Given a resume (PDF) and a job description (text), it returns:
- a **0–100 semantic match score**, computed from sentence-transformer embeddings (cosine similarity) — not keyword overlap
- an **interpretable skill-gap breakdown**: skills matched, skills missing from the resume, and extra skills the resume has that the JD doesn't mention

## Architecture

```
hirelens-ai/
├── backend/                 # FastAPI service
│   └── app/
│       ├── main.py          # API routes: /parse-resume, /match
│       ├── config.py        # model name, CORS, skills taxonomy
│       ├── schemas.py       # Pydantic request/response models
│       └── services/
│           ├── parser.py       # PDF/text extraction (pdfplumber)
│           ├── embeddings.py   # sentence-transformers similarity scoring
│           └── skills.py       # keyword-based skill-gap detection
└── frontend/                # React (Vite) single-page app
    └── src/
        ├── App.jsx
        └── components/
            ├── UploadForm.jsx
            ├── ResultsPanel.jsx
            └── ScoreGauge.jsx
```

**Why this shape (talking points for interviews):**
- Backend and frontend are decoupled via a REST API — the backend could serve a CLI, a Slack bot, or a batch job just as easily.
- The embedding model is loaded once at startup (`lifespan` hook) and cached, not reloaded per request — matters a lot for latency.
- Skill-gap detection is deliberately kept separate from the ML scoring: it's a simple, fast, interpretable keyword layer sitting alongside the semantic score, so results aren't just "a number nobody can explain."
- Natural v2 extensions to mention: fuzzy/embedding-based skill matching (catch "k8s" == "kubernetes"), auth + a Postgres store for multi-resume ranking, batch endpoint for screening many resumes against one JD, swap MiniLM for a larger model behind a feature flag.

## Setup

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

First run will download the `all-MiniLM-L6-v2` model (~80MB) from Hugging Face — needs an internet connection once, then it's cached locally.

API docs available at `http://localhost:8000/docs` (FastAPI's auto-generated Swagger UI).

### Frontend

```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

Open `http://localhost:5173`.

## API Reference

### `POST /parse-resume`
Multipart file upload (`file` field, `.pdf` or `.txt`). Returns extracted text.

### `POST /match`
```json
{
  "resume_text": "...",
  "job_description": "..."
}
```
Returns:
```json
{
  "match_score": 78.4,
  "verdict": "Strong match",
  "skill_gap": {
    "matched_skills": ["python", "fastapi", "sql"],
    "missing_skills": ["docker", "aws"],
    "resume_only_skills": ["django"]
  }
}
```

## Roadmap (good "future work" section for your resume/README)
- [ ] Batch mode: rank multiple resumes against one JD
- [ ] Fuzzy skill matching using embeddings instead of exact keywords
- [ ] Persist results to Postgres, add a history view
- [ ] Dockerize both services + docker-compose for one-command local run
- [ ] Deploy backend (Render/Railway) + frontend (Vercel/Netlify)
