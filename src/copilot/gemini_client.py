"""
gemini_client.py

Gemini API client for the AI Copilot.

Features
--------
- Bring Your Own API Key (BYOK)
- API validation
- Graceful error handling
- Uses Gemini 2.5 Flash
"""

from __future__ import annotations

import os
from typing import Optional

from google import genai


MODEL_NAME = "gemini-2.5-flash"


# ==========================================================
# Client Factory
# ==========================================================

def _create_client(api_key: Optional[str] = None) -> genai.Client:
    """
    Create a Gemini client.

    Priority:
    1. User supplied key
    2. Environment variable
    """

    key = api_key or os.getenv("GEMINI_API_KEY")

    if not key:
        raise ValueError(
            "Gemini API key not found."
        )

    return genai.Client(api_key=key)


# ==========================================================
# Validate API Key
# ==========================================================

def validate_api_key(api_key: str) -> tuple[bool, str]:
    """
    Validate a Gemini API key.

    Returns
    -------
    (success, message)
    """

    try:

        client = _create_client(api_key)

        client.models.generate_content(
            model=MODEL_NAME,
            contents="Reply with OK",
        )

        return True, "Connected"

    except Exception as e:

        return False, str(e)


# ==========================================================
# Ask Gemini
# ==========================================================

def ask_gemini(
    prompt: str,
    api_key: Optional[str] = None,
) -> str:
    """
    Send a grounded prompt to Gemini.
    """

    client = _create_client(api_key)

    try:

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
        )

        if hasattr(response, "text") and response.text:
            return response.text

        return "Gemini returned an empty response."

    except Exception as e:

        return (
            "Unable to contact Gemini.\n\n"
            f"{e}"
        )