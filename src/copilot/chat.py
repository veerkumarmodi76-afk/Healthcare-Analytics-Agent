from .context_builder import build_context
from .gemini_client import ask_gemini
from .prompts import SYSTEM_PROMPT


def ask_portfolio_copilot(
    question: str,
) -> str:

    context = build_context()

    prompt = f"""
{SYSTEM_PROMPT}

PORTFOLIO DATA

{context}

QUESTION

{question}
"""

    return ask_gemini(prompt)
