"""
rag.py

Lightweight Retrieval-Augmented Generation (RAG)

Responsibilities
----------------
- Index uploaded document chunks
- Retrieve the most relevant chunks
- Provide context for Gemini
"""

from __future__ import annotations

import re
from collections import Counter


class SimpleRAG:
    """
    Lightweight keyword-based retriever.

    Suitable for portfolio projects without requiring
    FAISS or LangChain.
    """

    def __init__(self):

        self.documents: list[str] = []

    # ======================================================
    # Index Documents
    # ======================================================

    def add_documents(
        self,
        chunks: list[str],
    ) -> None:

        self.documents.extend(chunks)

    def clear(self) -> None:

        self.documents = []

    # ======================================================
    # Retrieval
    # ======================================================

    def retrieve(
        self,
        question: str,
        top_k: int = 3,
    ) -> str:
        """
        Return the most relevant document chunks.
        """

        if not self.documents:
            return ""

        question_words = self._tokenize(question)

        scored = []

        for chunk in self.documents:

            chunk_words = self._tokenize(chunk)

            score = self._similarity(
                question_words,
                chunk_words,
            )

            scored.append(
                (
                    score,
                    chunk,
                )
            )

        scored.sort(
            key=lambda x: x[0],
            reverse=True,
        )

        relevant = [
            chunk
            for score, chunk in scored[:top_k]
            if score > 0
        ]

        return "\n\n".join(relevant)

    # ======================================================
    # Utilities
    # ======================================================

    @staticmethod
    def _tokenize(text: str) -> Counter:

        words = re.findall(
            r"[A-Za-z0-9]+",
            text.lower(),
        )

        return Counter(words)

    @staticmethod
    def _similarity(
        a: Counter,
        b: Counter,
    ) -> int:
        """
        Keyword overlap score.
        """

        return sum(
            (a & b).values()
        )


# ==========================================================
# Global Retriever
# ==========================================================

rag = SimpleRAG()


# ==========================================================
# Public Helper Functions
# ==========================================================

def index_documents(
    chunks: list[str],
) -> None:
    """
    Index uploaded document chunks.
    """

    rag.clear()
    rag.add_documents(chunks)


def retrieve_context(
    question: str,
    top_k: int = 3,
) -> str:
    """
    Retrieve relevant document context.
    """

    return rag.retrieve(
        question,
        top_k=top_k,
    )