"""
document_loader.py

Loads enterprise documents for the AI Copilot.

Supported Formats
-----------------
- PDF
- DOCX
- TXT
- CSV
- XLSX
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from docx import Document
from pypdf import PdfReader


SUPPORTED_EXTENSIONS = {
    ".pdf",
    ".docx",
    ".txt",
    ".csv",
    ".xlsx",
}


def load_document(file_path: str | Path) -> str:
    """
    Load a supported document and return its text.
    """

    path = Path(file_path)

    if not path.exists():
        return ""

    suffix = path.suffix.lower()

    if suffix not in SUPPORTED_EXTENSIONS:
        raise ValueError(
            f"Unsupported file type: {suffix}"
        )

    if suffix == ".pdf":
        return _load_pdf(path)

    if suffix == ".docx":
        return _load_docx(path)

    if suffix == ".txt":
        return path.read_text(
            encoding="utf-8",
            errors="ignore",
        )

    if suffix == ".csv":
        return pd.read_csv(path).to_string(index=False)

    if suffix == ".xlsx":
        return pd.read_excel(path).to_string(index=False)

    return ""


def _load_pdf(path: Path) -> str:

    reader = PdfReader(path)

    text = []

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:
            text.append(page_text)

    return "\n".join(text)


def _load_docx(path: Path) -> str:

    document = Document(path)

    return "\n".join(
        paragraph.text
        for paragraph in document.paragraphs
    )


def split_into_chunks(
    text: str,
    chunk_size: int = 1000,
    overlap: int = 200,
) -> list[str]:
    """
    Split text into overlapping chunks.
    """

    if not text.strip():
        return []

    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunks.append(text[start:end])

        start += chunk_size - overlap

    return chunks