# Spindle
# Local AI-Powered Network Crawling Assistant

Spindle is a desktop assistant that performs network discovery and answers natural-language queries about devices on specified subnets. It's designed for local demos and offline workflows, everything runs on your machine.
Built with: LLaMA (optional, via llama-cpp), Flask, nmap, Tkinter, and SQLite.

## Why Spindle?
- Local-first: runs without cloud dependencies.
- Conversational interface: ask for counts, lists, and host details in plain language.
- Lightweight persistence: scan results are stored in an on-disk SQLite database for later review.
## Security & privacy
- All components run locally, no data is sent to external services by default.
- Scans are limited to subnets you explicitly configure.
- Scan history is stored locally in a SQLite file.
## How it works
- Uses nmap to perform ping-sweep scans over configured subnet(s).
- Resolves hostnames when available and records timestamp, IP, hostname, and status.
- A Flask-based assistant API exposes a small chat endpoint that interprets a few built-in intents (counts, lists) and can optionally forward to a local LLaMA server for richer responses.
## Key features
- Real-time subnet scanning via lightweight ping sweeps
- Offline AI integration (optional) with llama-cpp
- Natural-language interface with AI fallback
- Local scan history stored in SQLite
- Packable as a standalone desktop application using PyInstaller

## Demo walkthrough (commands)
The demo UI accepts natural-language commands. Example interactions to showcase:

1. "List all devices" — runs a scan across configured subnets and returns device names/IPs/status.
## Installation & quick start (developer)
1) Create and activate a Python virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```
2) Install Python dependencies:

```bash
pip install -r requirements.txt
```
3) Configure required environment variables before running the app (replace placeholders with your settings):

```bash
export SPINDLE_SUBNETS="YOUR_SUBNET_CIDR"
export SPINDLE_DB_PATH="./scan_history.db"
export SPINDLE_API_URL="http://localhost:5000/chat"
export SPINDLE_LLAMA_HOST="0.0.0.0"
export SPINDLE_LLAMA_PORT="8000"
export SPINDLE_LLAMA_MODEL="./models/your-model.gguf"
```
4) Run the desktop app (starts Flask API + LLaMA runner in background threads):

```bash
python app/frontend/network_desktop_app.py
```
## Running components independently
- Assistant API (Flask):

```bash
python -c "import app.backend.assistant_api as a; a.start_api()"
```
- LLaMA runner (if configured):

```bash
python -c "import app.llama_runner as l; l.start_llama_server()"
```
## Requirements & environment
- Ensure the system `nmap` binary is installed and available on PATH (the Python wrapper invokes it). On macOS:

```bash
brew install nmap
```
## Packaging
- Use the included `spindleAI_build.py` and `.spec` files to produce a standalone executable via PyInstaller.

## Project layout
```
spindleAI/
  ├─ app/
  │   ├─ backend/
  │   │   └─ assistant_api.py
  │   ├─ frontend/
  │   │   └─ network_desktop_app.py
  │   └─ llama_runner.py
  ├─ requirements.txt
  ├─ spindleAI_build.py
  └─ *.spec
```
## Future plans
- Filter results by subnet, IP range, or hostname
- Scheduled scans and automation
- Visual dashboard with historical charts
- Faster response times and UI improvements
- AI-driven historical insights and exports (CSV)

## Contributing
- Contributions welcome. If you add dependencies, update `requirements.txt`.

## License
- Add a LICENSE file before publishing to public GitHub.

# SpindleAI

SpindleAI is a lightweight desktop application that combines simple network discovery with a local AI assistant interface. It provides a Tkinter-based GUI front end, a Flask backend that performs network scans with nmap and persists results to SQLite, and an optional local LLaMA server integration for richer conversational responses.

Key features
- Network discovery using nmap (ping scan) across configured subnets
- Simple assistant API to ask questions about the network (counts, lists, hostnames)
- SQLite-based scan history for lightweight persistence
- Local LLaMA server integration (optional) for advanced fallback responses
- Cross-platform desktop GUI (Tkinter) suitable for local demos and packaging

Tech stack
- Python (3.8+)
- Flask (backend)
- tkinter + PIL (frontend UI)
- nmap (python-nmap wrapper) for network scanning
- sqlite3 for storage
- llama-cpp server (optional) for local LLM hosting

Quick start (development)
1. Create and activate a Python virtual environment (recommended):

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Set required environment variables (example, zsh):

```bash
# Configure required environment variables before running the app.
# Replace values below with your own environment-specific settings.
export SPINDLE_SUBNETS="YOUR_SUBNET_CIDR"    # use CIDR notation; multiple subnets may be comma-separated
export SPINDLE_DB_PATH="./scan_history.db"
export SPINDLE_API_URL="http://localhost:5000/chat"
# Optional LLaMA server settings (if you run the included runner):
export SPINDLE_LLAMA_HOST="0.0.0.0"
export SPINDLE_LLAMA_PORT="8000"
export SPINDLE_LLAMA_MODEL="./models/your-model.gguf"
```

4. Run the desktop app (this will start the LLaMA runner and the Flask backend in background threads):

```bash
python app/frontend/network_desktop_app.py
```

Notes
- The GUI will attempt to start both the local LLaMA server (via `app/llama_runner.py`) and the Flask assistant API (via `app/backend/assistant_api.py`) in background threads. If you prefer to run services separately, start them individually:

  - Run the assistant API:

    ```bash
    python -c "import app.backend.assistant_api as a; a.start_api()"
    ```

  - Run the LLaMA runner (if available/configured):

    ```bash
    python -c "import app.llama_runner as l; l.start_llama_server()"
    ```

- Make sure `nmap` is installed on your system (the Python wrapper calls the nmap binary). On macOS you can install it with Homebrew:

```bash
brew install nmap
```

Packaging
- This repo contains `spindleAI_build.py` and PyInstaller spec files which can be used to create a standalone executable for distribution. Use those scripts or run PyInstaller manually with the included .spec files.

Project layout

```
spindleAI/
  ├─ app/
  │   ├─ backend/
  │   │   └─ assistant_api.py   # Flask API that runs nmap scans and stores results
  │   ├─ frontend/
  │   │   └─ network_desktop_app.py  # Tkinter desktop UI (starts services)
  │   └─ llama_runner.py        # small runner for a local llama-cpp server
  ├─ requirements.txt
  ├─ spindleAI_build.py         # build helper / packaging script
  └─ *.spec                     # PyInstaller spec files
```

Contributing
- Contributions are welcome. If you add features that change dependencies, update `requirements.txt`.

Troubleshooting
- If the GUI fails to start, check the log path configured via `SPINDLE_LOG` or run components individually to surface errors.
- Ensure `nmap` binary is installed and available on PATH.
