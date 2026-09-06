import os

import requests
import streamlit as st

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
DEFAULT_MODEL = os.getenv("OLLAMA_MODEL", "llama3")


def generate_response(prompt: str, model: str = DEFAULT_MODEL) -> str:
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
    }
    response = requests.post(f"{OLLAMA_BASE_URL}/api/generate", json=payload, timeout=120)
    response.raise_for_status()
    result = response.json()
    return result.get("response", "").strip()


st.set_page_config(page_title="Local Chatbot", page_icon="🤖", layout="wide")
st.title("Local Chatbot")
st.caption("A minimal local chat UI powered by Ollama.")

if "model_name" not in st.session_state:
    st.session_state.model_name = DEFAULT_MODEL
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! Ask me anything about the local task setup or the LLM configuration."}
    ]

with st.sidebar:
    st.header("Settings")
    model_name = st.text_input("Ollama model", value=st.session_state.model_name)
    if st.button("Apply model"):
        st.session_state.model_name = model_name.strip() or DEFAULT_MODEL

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Type your question here...")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        reply = generate_response(prompt, st.session_state.model_name)
    except Exception as exc:  # pragma: no cover - runtime failure path
        reply = f"Error: {exc}"

    st.session_state.messages.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.markdown(reply)
