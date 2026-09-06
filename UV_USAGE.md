# UV Usage Guide

This project uses uv for a reproducible local Python environment.

## 1. Install uv

```powershell
python -m pip install uv
```

## 2. Sync the environment

From the project root:

```powershell
cd <project-root>
uv sync
```

This installs all dependencies listed in [pyproject.toml](pyproject.toml).

## 3. Start the local model backend

The LLM is not stored inside the repository. It is downloaded into the local Ollama store using Ollama itself.

```powershell
ollama serve
ollama pull llama3
```

You can replace `llama3` with another local model if needed.

## 4. Run the project with uv

### Streamlit UI

```powershell
cd <project-root>
uv run streamlit run task_1/streamlit_app.py --server.port 8501 --server.headless true
```

Then open:

```text
http://localhost:8501
```

### CLI chatbot

```powershell
cd <project-root>
uv run python task_1/local_chatbot.py --prompt "Say hello in one sentence."
```

### Task scripts

```powershell
cd <project-root>
uv run python task_2/train_classifier.py
uv run python task_3/part_similarity.py
uv run python task_4_5/timestamp_diff.py
```

### Tests

```powershell
cd <project-root>
uv run pytest task_2/test_task_2.py task_4_5/test_timestamp_diff.py
```

## 5. Useful environment variables

```powershell
$env:OLLAMA_BASE_URL = "http://localhost:11434"
$env:OLLAMA_MODEL = "llama3"
```

These can be set in the same PowerShell session before launching the app.

## 6. Notes

- The LLM model lives in the local Ollama cache rather than in the repository.
- The Python project itself is managed by uv via [pyproject.toml](pyproject.toml).
- The repo remains local and intended for local use only.
