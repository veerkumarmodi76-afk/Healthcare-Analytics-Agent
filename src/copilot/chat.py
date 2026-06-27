"""
chat.py

Main AI Copilot interface.

Responsibilities
----------------
- Build grounded context
- Construct final prompt
- Send request to Gemini
- Return response
"""

from __future__ import annotations

from typing import Optional

from .context_builder import build_context
from .gemini_client import ask_gemini
from .prompts import SYSTEM_PROMPT


# ==========================================================
# Portfolio Copilot
# ==========================================================

def ask_portfolio_copilot(
    question: str,
    api_key: Optional[str] = None,
    document_context: Optional[str] = None,
) -> str:
    """
    Ask the Healthcare Analytics Copilot.

    Parameters
    ----------
    question
        User question.

    api_key
        Gemini API key.

    document_context
        Optional enterprise document context
        (Phase 11 RAG).

    Returns
    -------
    str
        AI response.
    """

    context = build_context(
        document_context=document_context,
    )

    prompt = f"""
{SYSTEM_PROMPT}

==================================================
HEALTHCARE ANALYTICS CONTEXT
==================================================

{context}

==================================================
USER QUESTION
==================================================

{question}

==================================================
INSTRUCTIONS
==================================================

1. Answer ONLY from the supplied context.

2. Never invent:
   - numbers
   - percentages
   - premiums
   - claims
   - policies
   - recommendations not supported by the data.

3. If information is unavailable, clearly state that
   the requested information does not exist in the
   supplied analytics or uploaded documents.

4. If uploaded documents are available, combine them
   with the analytics before answering.

5. Structure every response as:

### Summary

### Supporting Evidence

### Recommendations
"""

    return ask_gemini(
        prompt=prompt,
        api_key=api_key,
    )