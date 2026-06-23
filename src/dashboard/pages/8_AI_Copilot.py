from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.append(str(ROOT))

import streamlit as st

from src.copilot.chat import (
    ask_portfolio_copilot,
)

st.title("AI Portfolio Copilot")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

question = st.chat_input("Ask about portfolio performance...")

if question:
    st.session_state.messages.append({
        "role": "user",
        "content": question,
    })

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Analyzing portfolio..."):
            answer = ask_portfolio_copilot(question)

        st.markdown(answer)

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer,
    })
