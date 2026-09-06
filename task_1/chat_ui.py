import argparse
import json
import os
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import requests

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
DEFAULT_MODEL = os.getenv("OLLAMA_MODEL", "llama3")

HTML_PAGE = """
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Local Chatbot</title>
    <style>
      :root {
        --bg: #101827;
        --panel: #1f2937;
        --panel-alt: #111827;
        --text: #f9fafb;
        --muted: #cbd5e1;
        --border: #374151;
        --accent: #60a5fa;
        --accent-strong: #2563eb;
      }
      * { box-sizing: border-box; }
      body {
        margin: 0;
        font-family: Arial, sans-serif;
        background: linear-gradient(180deg, var(--bg), #0f172a);
        color: var(--text);
        min-height: 100vh;
        display: flex;
        align-items: center;
        justify-content: center;
      }
      .app {
        width: min(900px, 92vw);
        height: min(86vh, 720px);
        background: rgba(17, 24, 39, 0.92);
        border: 1px solid var(--border);
        border-radius: 16px;
        overflow: hidden;
        box-shadow: 0 18px 45px rgba(0,0,0,0.35);
      }
      .header {
        padding: 18px 20px;
        background: var(--panel-alt);
        border-bottom: 1px solid var(--border);
        font-size: 1.1rem;
        font-weight: 700;
      }
      .messages {
        height: calc(100% - 150px);
        overflow-y: auto;
        padding: 18px;
        background: rgba(15, 23, 42, 0.7);
      }
      .message {
        margin-bottom: 14px;
        padding: 12px 14px;
        border-radius: 12px;
        max-width: 75%;
        line-height: 1.45;
      }
      .user {
        background: var(--accent-strong);
        margin-left: auto;
      }
      .assistant {
        background: var(--panel);
        border: 1px solid var(--border);
      }
      .composer {
        display: flex;
        gap: 10px;
        padding: 14px 16px;
        border-top: 1px solid var(--border);
        background: var(--panel-alt);
      }
      input {
        flex: 1;
        border: 1px solid var(--border);
        background: var(--panel);
        color: var(--text);
        border-radius: 10px;
        padding: 12px 14px;
        font-size: 1rem;
      }
      button {
        border: none;
        border-radius: 10px;
        background: linear-gradient(135deg, var(--accent), var(--accent-strong));
        color: white;
        padding: 12px 18px;
        font-size: 1rem;
        font-weight: 700;
        cursor: pointer;
      }
      button:hover { filter: brightness(1.05); }
      .status {
        color: var(--muted);
        font-size: 0.85rem;
        padding: 0 18px 10px;
      }
    </style>
  </head>
  <body>
    <div class="app">
      <div class="header">Local Chatbot</div>
      <div id="messages" class="messages"></div>
      <div class="status" id="status">Ready</div>
      <div class="composer">
        <input id="prompt" type="text" placeholder="Type your question here..." />
        <button id="send">Send</button>
      </div>
    </div>

    <script>
      const messages = document.getElementById('messages');
      const promptInput = document.getElementById('prompt');
      const sendButton = document.getElementById('send');
      const status = document.getElementById('status');

      function addMessage(text, sender) {
        const div = document.createElement('div');
        div.className = `message ${sender}`;
        div.textContent = text;
        messages.appendChild(div);
        messages.scrollTop = messages.scrollHeight;
      }

      async function sendPrompt() {
        const prompt = promptInput.value.trim();
        if (!prompt) return;

        addMessage(prompt, 'user');
        promptInput.value = '';
        status.textContent = 'Thinking...';

        try {
          const response = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ prompt })
          });

          const data = await response.json();
          if (!response.ok) {
            throw new Error(data.error || 'Request failed');
          }

          addMessage(data.reply || 'No response returned.', 'assistant');
          status.textContent = 'Ready';
        } catch (error) {
          addMessage(`Error: ${error.message}`, 'assistant');
          status.textContent = 'Error';
        }
      }

      sendButton.addEventListener('click', sendPrompt);
      promptInput.addEventListener('keydown', (event) => {
        if (event.key === 'Enter') {
          sendPrompt();
        }
      });

      addMessage('Hello! Ask me anything about the local task setup or model usage.', 'assistant');
    </script>
  </body>
</html>
"""


def generate_response(prompt: str, model: str = DEFAULT_MODEL, system_prompt: str | None = None) -> str:
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


class ChatHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(HTML_PAGE.encode('utf-8'))
            return

        self.send_error(404)

    def do_POST(self):
        if self.path != '/api/chat':
            self.send_error(404)
            return

        try:
            length = int(self.headers.get('Content-Length', '0'))
            body = self.rfile.read(length)
            data = json.loads(body.decode('utf-8'))
        except Exception:
            self.send_response(400)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': 'Invalid JSON body'}).encode('utf-8'))
            return

        prompt = str(data.get('prompt', '')).strip()
        if not prompt:
            self.send_response(400)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': 'Prompt cannot be empty'}).encode('utf-8'))
            return

        try:
            reply = generate_response(prompt, model=DEFAULT_MODEL)
            response_body = json.dumps({'reply': reply}).encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', str(len(response_body)))
            self.end_headers()
            self.wfile.write(response_body)
        except Exception as exc:  # pragma: no cover - runtime failure path
            response_body = json.dumps({'error': str(exc)}).encode('utf-8')
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', str(len(response_body)))
            self.end_headers()
            self.wfile.write(response_body)

    def log_message(self, format, *args):
        return


def run_ui(host: str = '127.0.0.1', port: int = 8000, open_browser: bool = True) -> None:
    server = ThreadingHTTPServer((host, port), ChatHandler)
    url = f'http://{host}:{port}/'
    print(f'Local chatbot UI running at {url}')
    if open_browser:
        webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('Stopping chat UI...')
        server.server_close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run a minimal local HTML UI for the chatbot.')
    parser.add_argument('--host', default='127.0.0.1', help='Host address to bind the UI to.')
    parser.add_argument('--port', type=int, default=8000, help='Port to serve the UI on.')
    parser.add_argument('--model', default=DEFAULT_MODEL, help='Ollama model to use.')
    parser.add_argument('--no-open-browser', action='store_true', help='Do not open the browser automatically.')
    args = parser.parse_args()

    # keep the actual model used by the app in sync with CLI args
    os.environ['OLLAMA_MODEL'] = args.model

    run_ui(host=args.host, port=args.port, open_browser=not args.no_open_browser)
