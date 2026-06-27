"""
8_AI_Copilot.py

Healthcare Analytics AI Copilot

Features
--------
- Bring Your Own Gemini API Key
- Enterprise Document Upload
- Grounded Analytics Chat
- Conversation History
- Suggested Questions
"""

from __future__ import annotations

import tempfile
from pathlib import Path

import streamlit as st

from src.utils.dashboard_loader import DashboardLoader

from src.copilot.chat import ask_portfolio_copilot
from src.copilot.gemini_client import validate_api_key
from src.copilot.document_loader import (
    load_document,
    split_into_chunks,
)
from src.copilot.rag import (
    index_documents,
    retrieve_context,
)

# ==========================================================
# Page Configuration
# ==========================================================

st.set_page_config(
    page_title="AI Copilot",
    page_icon="🤖",
    layout="wide",
)

loader = DashboardLoader()

# ==========================================================
# Portfolio Validation
# ==========================================================

if not loader.portfolio_exists():

    st.warning(
        """
No processed portfolio found.

Please execute the Healthcare Analytics
Pipeline before using the AI Copilot.
"""
    )

    st.stop()

# ==========================================================
# Session State
# ==========================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "api_key" not in st.session_state:
    st.session_state.api_key = ""

if "documents_indexed" not in st.session_state:
    st.session_state.documents_indexed = False

# ==========================================================
# Header
# ==========================================================

st.title("🤖 AI Copilot")

st.caption(
    "Grounded Healthcare Insurance Analytics Assistant"
)

st.divider()

# ==========================================================
# Sidebar
# ==========================================================

with st.sidebar:

    st.subheader("Gemini API")

    api_key = st.text_input(
        "Gemini API Key",
        type="password",
        value=st.session_state.api_key,
    )

    if st.button(
        "Validate API Key",
        use_container_width=True,
    ):

        ok, message = validate_api_key(api_key)

        if ok:

            st.session_state.api_key = api_key

            st.success("Connected")

        else:

            st.error(message)

    st.divider()

    st.subheader("Enterprise Documents")

    uploaded_files = st.file_uploader(

        "Upload Company Documents",

        type=[
            "pdf",
            "docx",
            "txt",
            "csv",
            "xlsx",
        ],

        accept_multiple_files=True,
    )

    if uploaded_files:

        chunks = []

        for file in uploaded_files:

            suffix = Path(file.name).suffix

            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=suffix,
            ) as tmp:

                tmp.write(file.getvalue())

                tmp_path = tmp.name

            text = load_document(tmp_path)

            chunks.extend(
                split_into_chunks(text)
            )

        index_documents(chunks)

        st.session_state.documents_indexed = True

        st.success(
            f"{len(uploaded_files)} document(s) indexed."
        )

    st.divider()

    st.subheader("Suggested Questions")

    suggestions = [

        "Give me an executive summary.",

        "How healthy is this portfolio?",

        "Which customers are most likely to lapse?",

        "Which risk segment has the highest claims?",

        "Explain the pricing recommendations.",

        "Summarize underwriting performance.",

        "What is the portfolio loss ratio?",

        "What should management focus on?",
    ]

    for question in suggestions:

        if st.button(
            question,
            use_container_width=True,
        ):

            st.session_state.selected_question = question

    st.divider()

    st.subheader("Chat")

    if st.button(
        "🗑️ Clear Chat",
        use_container_width=True,
    ):

        st.session_state.messages = []

        if "selected_question" in st.session_state:
            del st.session_state.selected_question

        st.rerun()

# ==========================================================
# Display Conversation
# ==========================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

# ==========================================================
# User Prompt
# ==========================================================

prompt = st.chat_input(
    "Ask about your healthcare portfolio..."
)

if "selected_question" in st.session_state:

    prompt = st.session_state.selected_question

    del st.session_state.selected_question

# ==========================================================
# Chat
# ==========================================================

if prompt:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt,
        }
    )

    with st.chat_message("user"):

        st.markdown(prompt)

    with st.chat_message("assistant"):

        with st.spinner("Analyzing portfolio..."):

            try:

                # ------------------------------------------
                # API Key Check
                # ------------------------------------------

                if not st.session_state.api_key:

                    answer = (
                        "Please enter and validate your "
                        "Gemini API Key from the sidebar."
                    )

                else:

                    # --------------------------------------
                    # Retrieve document context (RAG)
                    # --------------------------------------

                    document_context = ""

                    if st.session_state.documents_indexed:

                        document_context = retrieve_context(
                            prompt
                        )

                    # --------------------------------------
                    # Ask Copilot
                    # --------------------------------------

                    answer = ask_portfolio_copilot(
                        question=prompt,
                        api_key=st.session_state.api_key,
                        document_context=document_context,
                    )

            except Exception as e:

                answer = (
                    "Unable to generate a response.\n\n"
                    f"{e}"
                )

            st.markdown(answer)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
        }
    )

# ==========================================================
# Footer
# ==========================================================

st.divider()

col1, col2 = st.columns(2)

with col1:

    if st.session_state.documents_indexed:

        st.success(
            "Enterprise knowledge base loaded."
        )

    else:

        st.info(
            "No enterprise documents uploaded."
        )

with col2:

    if st.session_state.api_key:

        st.success(
            "Gemini Connected"
        )

    else:

        st.warning(
            "Gemini API Key Required"
        )

st.info(
    """
The AI Copilot answers using:

• Generated portfolio analytics
• Executive reports
• Pricing outputs
• Underwriting outputs
• Lapse analytics
• Uploaded enterprise documents (if available)

If the required information is unavailable,
the Copilot will state that it cannot answer
rather than inventing unsupported information.
"""
)