# Spindle  
## Local AI-Powered Network Crawling Assistant

**Spindle** is a lightweight desktop assistant that performs local network discovery and answers natural-language queries about connected devices.  
It’s designed for **offline use**, with all components running locally and no cloud dependencies.  

Built with **Python**, **Flask**, **nmap**, **Tkinter**, **SQLite**, and optional **LLaMA integration (via llama-cpp)** for natural-language responses.

---

## Why Spindle?

- **Local-first:** No external calls — all processing stays on your machine.  
- **Conversational interface:** Ask questions like *“List all devices on my network”* or *“How many hosts are online?”*  
- **Lightweight persistence:** Scan results are saved to a local SQLite database for later review.  
- **Cross-platform:** Runs on Windows, macOS, or Linux.  
- **Offline AI:** Optional LLaMA support for richer, context-aware responses.  

---

## Security & Privacy

- 100% local execution — no data leaves your system by default.  
- Scans are limited to subnets you configure explicitly.  
- Scan history is stored locally in `scan_history.db` (SQLite).  

---

## How It Works

- **Network discovery:** Uses `nmap` for efficient ping-sweep scans over specified subnets.  
- **Data capture:** Records hostname, IP, status, and timestamp for each discovered host.  
- **Assistant API:** Flask backend interprets chat-like queries (counts, lists, host info).  
- **AI integration (optional):** Queries can be forwarded to a local LLaMA model via `llama-cpp` for natural-language answers.  
- **Frontend:** A Tkinter GUI provides a chat-style interface for interacting with the assistant.  

---

## Key Features

- Real-time subnet scanning via lightweight ping sweeps  
- Natural-language interface with AI fallback (LLaMA)  
- Persistent local scan history in SQLite  
- Flask-based REST API for programmatic access  
- Standalone desktop packaging via PyInstaller  

---

## Demo Example

The desktop app’s chat interface accepts plain-language commands such as:  
- **“List all devices.”** — runs a scan across configured subnets and displays device names, IPs, and statuses.  
- **“How many hosts are online?”** — queries the database for live hosts.  
- **“Show me inactive devices.”** — filters results by status.  

---

## Installation & Quick Start (Developer)

### 1. Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate   # macOS/Linux
# OR
.\.venv\Scripts\activate    # Windows
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

```bash
export SPINDLE_SUBNETS="YOUR_SUBNET_CIDR"    # e.g., 192.168.0.0/24
export SPINDLE_DB_PATH="./scan_history.db"
export SPINDLE_API_URL="http://localhost:5000/chat"
# Optional LLaMA server configuration
export SPINDLE_LLAMA_HOST="0.0.0.0"
export SPINDLE_LLAMA_PORT="8000"
export SPINDLE_LLAMA_MODEL="./models/your-model.gguf"
```

### 4. Run the desktop app

```bash
python app/frontend/network_desktop_app.py
```

This launches the Flask backend and optional LLaMA server automatically in background threads.

---

## Running Components Independently

If you prefer to start components separately:

**Assistant API (Flask):**
```bash
python -c "import app.backend.assistant_api as a; a.start_api()"
```

**LLaMA Runner (optional):**
```bash
python -c "import app.llama_runner as l; l.start_llama_server()"
```

---

## Requirements

- **Python 3.8+**
- **nmap** installed and available on system PATH  
  - macOS:  
    ```bash
    brew install nmap
    ```
- **Dependencies:** See `requirements.txt`  

---

## Packaging

Use the included build files to create a standalone desktop app:

```bash
python spindleAI_build.py
```

or run PyInstaller directly using the provided `.spec` file.  

This bundles the Tkinter UI, backend, and optional LLaMA runner into one portable executable.

---

## Project Layout

```
spindle/
  ├─ app/
  │   ├─ backend/
  │   │   └─ assistant_api.py        # Flask API for network scanning & chat
  │   ├─ frontend/
  │   │   └─ network_desktop_app.py  # Tkinter desktop interface
  │   └─ llama_runner.py             # Local llama-cpp server runner (optional)
  ├─ requirements.txt
  ├─ spindle_build.py
  ├─ spindle.spec
  └─ scan_history.db (generated at runtime)
```

---

## Future Plans

- Filtering by subnet, IP range, or hostname  
- Scheduled scans and automation  
- Historical dashboards and trend visualization  
- CSV/JSON data export  
- Enhanced natural-language AI analysis  

---

## Troubleshooting

- **GUI won’t start:** Check console logs or run backend services manually to isolate errors.  
- **nmap not found:** Ensure it’s installed and available on PATH.  
- **LLaMA errors:** Verify the model path and that the llama-cpp library is correctly installed.  
- **Database not updating:** Ensure write permissions in the working directory.  
