"""
Resume text extraction.

Supports PDF (via pdfplumber) and plain .txt uploads. Keeping this isolated
from the API layer means you can swap in OCR (e.g. for scanned resumes)
later without touching main.py.
"""
import io

import pdfplumber


def extract_text_from_pdf(file_bytes: bytes) -> str:
    text_chunks = []
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text_chunks.append(page_text)
    return "\n".join(text_chunks).strip()


def extract_text(filename: str, file_bytes: bytes) -> str:
    lower = filename.lower()
    if lower.endswith(".pdf"):
        return extract_text_from_pdf(file_bytes)
    if lower.endswith(".txt"):
        return file_bytes.decode("utf-8", errors="ignore").strip()
    raise ValueError(f"Unsupported file type for '{filename}'. Use .pdf or .txt")
