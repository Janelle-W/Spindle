from flask import Flask, request, jsonify
from datetime import datetime
import requests
import nmap
import sqlite3
import sys
import os

app = Flask(__name__)

# --- Intent matching ---
intents = {
    "how many devices are online": "count_up",
    "how many are up": "count_up",
    "what devices are active": "count_up",
    "how many are down": "count_down",
    "what devices are offline": "count_down",
    "list all devices": "list_all",
    "show me device names": "device_names"
}

# --- Configuration (placeholders only, no sensitive info) ---
# Subnets must be provided by the user via environment
_subnets_env = os.getenv("SPINDLE_SUBNETS")  # e.g., "YOUR_SUBNET_HERE,YOUR_OTHER_SUBNET"
if _subnets_env:
    SUBNETS = [s.strip() for s in _subnets_env.split(",") if s.strip()]
else:
    SUBNETS = ["YOUR_SUBNET_HERE"]  # <-- placeholder only, not functional until replaced

# Path to SQLite DB (override with env var)
DB_PATH = os.getenv("SPINDLE_DB_PATH", "YOUR_DB_PATH_HERE")  # e.g., "./scan_history.db"

# LLaMA endpoint (must be set by user if fallback is needed)
LLAMA_URL = os.getenv("SPINDLE_LLAMA_URL", "YOUR_LLM_ENDPOINT_HERE")


def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.abspath(relative_path)


# --- Initialize SQLite ---
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS scans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            ip TEXT,
            hostname TEXT,
            status TEXT,
            subnet TEXT
        )
    """)
    conn.commit()
    conn.close()


# --- Run Network Scan ---
def run_scan():
    scanner = nmap.PortScanner()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    results = []

    for subnet in SUBNETS:
        scanner.scan(hosts=subnet, arguments='-sn')
        for host in scanner.all_hosts():
            hostname = scanner[host].hostname()
            status = scanner[host].state()
            results.append({
                "IP": host,
                "Hostname": hostname or "Unknown",
                "Status": status,
                "Subnet": subnet
            })

    return results, timestamp


# --- Save scan results ---
def save_to_db(devices, timestamp):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    for d in devices:
        cursor.execute("""
            INSERT INTO scans (timestamp, ip, hostname, status, subnet)
            VALUES (?, ?, ?, ?, ?)
        """, (timestamp, d["IP"], d["Hostname"], d["Status"], d["Subnet"]))
    conn.commit()
    conn.close()


# --- Intent match ---
def match_intent(user_input):
    lowered = user_input.lower()
    for phrase, intent in intents.items():
        if phrase in lowered:
            return intent
    return "unknown"


# --- Main Chat API ---
@app.route("/chat", methods=["POST"])
def chat():
    user_prompt = request.json.get("message", "")
    intent = match_intent(user_prompt)

    if intent != "unknown":
        devices, timestamp = run_scan()
        save_to_db(devices, timestamp)

        if intent == "count_up":
            up = [d for d in devices if d["Status"].lower() == "up"]
            return jsonify({"response": f"{len(up)} devices are online as of {timestamp}."})

        elif intent == "count_down":
            down = [d for d in devices if d["Status"].lower() == "down"]
            return jsonify({"response": f"{len(down)} devices are offline as of {timestamp}."})

        elif intent == "list_all":
            lines = [f"{d['Hostname']} ({d['IP']}) in {d['Subnet']} is {d['Status']}" for d in devices]
            return jsonify({"response": f"Devices as of {timestamp}:\n" + "\n".join(lines)})
        
        elif intent == "device_names":
            names = [d["Hostname"] for d in devices if d["Hostname"] != "Unknown"]
            reply = f"Device names as of {timestamp}:\n" + "\n".join(names) if names else "No hostnames found."
            return jsonify({"response": reply})

    # Fallback to LLaMA (only works if SPINDLE_LLAMA_URL is set)
    try:
        response = requests.post(LLAMA_URL, json={
            "messages": [
                {"role": "system", "content": "You are a helpful assistant that answers questions about networks."},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 200,
            "stream": False
        })
        data = response.json()
        reply = data.get("choices", [{}])[0].get("message", {}).get("content", "[No response]")
    except Exception as e:
        reply = f"[Error: {str(e)}]"

    return jsonify({"response": reply})


# --- Flask Startup ---
def start_api():
    init_db()
    # Host/port must come from environment — no defaults
    host = os.getenv("SPINDLE_FLASK_HOST", "YOUR_HOST_HERE")
    port = int(os.getenv("SPINDLE_FLASK_PORT", "YOUR_PORT_HERE"))
    app.run(host=host, port=port)
