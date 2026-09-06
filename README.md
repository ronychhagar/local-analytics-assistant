# Local LLM Data Tasks

This workspace contains a Python-based project organized by task. The implementation is structured so each task can be explored and run independently.

## Executive summary

The project demonstrates a local-first LLM workflow, a practical tabular ML workflow, a similarity-search pipeline for product replacement, and the timestamp logic required for the final business-time calculations. The main goal was to keep everything local, transparent, and easy to run without depending on a public API.

## uv setup and Python environment

This project is configured as a uv-managed application. The Python version is pinned in [.python-version](.python-version) and the project dependencies are declared in [pyproject.toml](pyproject.toml).

### Install uv

On Windows:

```powershell
python -m pip install uv
```

Then from the project root:

```powershell
cd <project-root>
uv sync
```

This creates the local environment and installs all Python dependencies defined for the project.

### Run with uv

```powershell
cd <project-root>
uv run python task_2/train_classifier.py
uv run python task_3/part_similarity.py
uv run streamlit run task_1/streamlit_app.py --server.port 8501 --server.headless true
```

## Local LLM and model handling

The chatbot uses Ollama as the local inference backend. The model is not shipped in the repository; it is downloaded into the local Ollama store when you pull it.

### Install Ollama and pull the model

Ollama is not installed via Python or uv. It must be installed separately on the machine and then run locally.

1. Install Ollama from the official Ollama website or installer for your OS.
2. Start the local server:

```powershell
ollama serve
```

3. Download the model into your local Ollama store:

```powershell
ollama pull llama3
```

This keeps the model local to your machine and does not require it to live inside the repository.

You can also choose a different local model if preferred, such as `mistral`, by setting the environment variable:

```powershell
$env:OLLAMA_MODEL = "llama3"
```

The app code reads this from the environment automatically.

## Machine setup and LLM rationale

### Model choice
I used Ollama with a lightweight local model (`llama3`) because it keeps the solution local and private while still being easy to run on a standard machine.

### Why this stack
- Runs locally on the developer machine
- Works without external API keys
- Suitable for CPU-only machines and GPU-accelerated hardware
- Widely used, well-documented, and easy to integrate
- Easy to call from Python for human-friendly local interfaces

### Hardware profile
A representative local workstation configuration is:
- OS: Windows 11
- CPU: standard local workstation CPU
- RAM: 16 GB or higher recommended
- GPU: optional NVIDIA CUDA GPU; not required for the implementation to work
- Python: 3.12 recommended

The chatbot code in [task_1/local_chatbot.py](task_1/local_chatbot.py) and the Streamlit app in [task_1/streamlit_app.py](task_1/streamlit_app.py) are designed to target the Ollama HTTP API and can run with either CPU-only inference or GPU acceleration when available.

## Task overview

### Task 1 — Local LLM chatbot
- Implemented as a simple local chatbot interface using Ollama in [task_1/local_chatbot.py](task_1/local_chatbot.py).
- A Streamlit UI is also included in [task_1/streamlit_app.py](task_1/streamlit_app.py) for browser-based use.
- The local model remains under the user’s control with no third-party cloud dependency.

### Task 2 — Binary classification of Type
- Merged the tables by `ID` and built a logistic-regression baseline pipeline in [task_2/train_classifier.py](task_2/train_classifier.py).
- The solution handles both numeric and categorical features using preprocessing and one-hot encoding.
- This is a robust baseline for a binary tabular classification problem.

### Task 3 — Similar parts search
- Implemented a TF-IDF + cosine similarity approach in [task_3/part_similarity.py](task_3/part_similarity.py).
- This is appropriate for the short technical product descriptions because lexical overlap is meaningful and the method is lightweight and interpretable.
- The implementation also includes a data-quality discussion and handling strategy for noisy and partially missing descriptions in [task_3/README.md](task_3/README.md).

### Task 4 and 5 — Timestamp difference logic
- Added the full-hour and business-hour functions in [task_4_5/timestamp_diff.py](task_4_5/timestamp_diff.py).
- The full-hour function returns the rounded full-hours difference.
- The business-hour function counts only weekdays and only the standard 09:00–17:00 window.

## Project structure

- [task_1/](task_1/): local chatbot implementation and UI
- [task_2/](task_2/): binary classification solution
- [task_3/](task_3/): descriptive analysis and similarity search
- [task_4_5/](task_4_5/): timestamp functions for Tasks 4 and 5
- [requirements.txt](requirements.txt): legacy dependency list
- [pyproject.toml](pyproject.toml): uv project configuration
- [.gitignore](.gitignore): local-only generated-files exclusions

## Local repository note

The project is intended to remain local and not be uploaded to public repositories. A local `.git` repository can be initialized on the user’s machine with the usual Git commands if Git is installed.

## Validation

The implementation was checked with a fresh pytest run against the task tests:

```powershell
uv run pytest task_2/test_task_2.py task_4_5/test_timestamp_diff.py
```

Result: 4 passed in 2.34s.

## Final note

This package is designed to be easy to hand off, rerun, and adapt on a local developer workstation. The code remains lightweight, explainable, and aligned with the task brief while keeping the environment local-first and privacy-conscious.
