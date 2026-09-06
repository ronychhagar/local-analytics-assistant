# Task 1 — Local LLM chatbot

## Model selection

I selected Ollama with a small open-weight model such as llama3.2 because it is a widely used local inference stack that works well on both CPU and GPU hardware. It is easy to run without sending data to a third-party API, which fits the requirement to keep the solution local and privacy-preserving.

### Why this choice

- Runs locally on the developer machine
- Works with or without GPU acceleration
- Uses a recognized and trusted ecosystem (Ollama + open models)
- Easy to integrate into a lightweight CLI or web UI
- Suitable for experimentation and iterative prompting

## Implementation

The project includes a CLI chatbot in [task_1/local_chatbot.py](task_1/local_chatbot.py) that calls the local Ollama API using HTTP and returns generated responses. It is intentionally simple and human-friendly.

## Usage

1. Install Ollama and pull a model such as `llama3.2`.
2. Run `ollama serve`.
3. Install the Python dependency list in this folder.
4. Launch the chatbot script.

Example:

```bash
python task_1/local_chatbot.py
```

The script accepts a user prompt and prints the local-model response.

## Hardware note

The implementation is designed to run on a typical local workstation. If a GPU is present, the model will accelerate generation; otherwise CPU inference remains fully functional.
