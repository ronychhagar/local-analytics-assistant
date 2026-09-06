import argparse
import os
from typing import Optional

import requests

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
DEFAULT_MODEL = os.getenv("OLLAMA_MODEL", "llama3")


def generate_response(prompt: str, model: str = DEFAULT_MODEL, system_prompt: Optional[str] = None) -> str:
    if system_prompt is None:
        system_prompt = (
            "You are a helpful local assistant. "
            "Answer clearly, concisely, and with practical engineering guidance."
        )

    payload = {
        "model": model,
        "prompt": f"{system_prompt}\n\nUser: {prompt}\nAssistant:",
        "stream": False,
    }

    response = requests.post(f"{OLLAMA_BASE_URL}/api/generate", json=payload, timeout=120)
    if response.status_code == 404:
        raise RuntimeError(
            "Ollama generate endpoint not found. Ensure the Ollama server is running and the model is installed."
        )
    response.raise_for_status()
    payload_response = response.json()
    return payload_response.get("response", "").strip()


def interactive_chat(model: str = DEFAULT_MODEL) -> None:
    print("Local chatbot is ready. Type 'exit' to quit.")
    while True:
        user_input = input("You: ").strip()
        if not user_input:
            continue
        if user_input.lower() in {"exit", "quit"}:
            print("Goodbye.")
            break

        answer = generate_response(user_input, model=model)
        print(f"Assistant: {answer}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run a local LLM chatbot through Ollama.")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="Local model name to use in Ollama.")
    parser.add_argument("--prompt", default=None, help="Optional single prompt to answer without interactive mode.")
    args = parser.parse_args()

    if args.prompt:
        print(generate_response(args.prompt, model=args.model))
    else:
        interactive_chat(model=args.model)
