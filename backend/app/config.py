"""
Central configuration for HireLens-AI backend.
"""

# Sentence-transformers model used for semantic embeddings.
# all-MiniLM-L6-v2 is small (~80MB), fast on CPU, and strong enough for
# resume/JD similarity. Swap to a larger model (e.g. all-mpnet-base-v2)
# for higher accuracy at the cost of latency.
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"

# CORS origins allowed to call the API (add your deployed frontend URL here too).
ALLOWED_ORIGINS = [
    "http://localhost:5173",  # Vite dev server default
    "http://127.0.0.1:5173",
    "https://ai-interview-two-ivory.vercel.app",
]

# Curated skills taxonomy used for keyword-based skill extraction.
# This runs alongside the embedding similarity score so the app can show
# *interpretable* matched/missing skills, not just a single opaque number.
# Extend this list freely as you use the tool on real job descriptions.
SKILLS_TAXONOMY = [
    # Languages
    "python", "java", "javascript", "typescript", "c++", "c", "go", "rust", "sql",
    # Web / backend frameworks
    "fastapi", "flask", "django", "spring boot", "node.js", "express",
    "react", "next.js", "vue", "angular",
    # Data / ML
    "pandas", "numpy", "scikit-learn", "pytorch", "tensorflow", "keras",
    "nlp", "machine learning", "deep learning", "data analysis",
    "sentence-transformers", "huggingface", "llm", "computer vision",
    # Databases
    "postgresql", "mysql", "mongodb", "redis", "sqlite",
    # DevOps / cloud
    "docker", "kubernetes", "aws", "azure", "gcp", "ci/cd", "git", "linux",
    # CS fundamentals (relevant for SP/DSE roles specifically)
    "data structures", "algorithms", "system design", "oop", "rest api",
    "microservices", "unit testing",
]