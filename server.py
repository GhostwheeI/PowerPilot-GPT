import os
import subprocess
import uuid
import json
import time
import gzip
import shutil
from flask import Flask, request, jsonify
from datetime import datetime
from pathlib import Path

LOG_DIR = Path("logs")
MAX_LOG_FILE_SIZE_MB = 30
MAX_TOTAL_LOG_ARCHIVE_SIZE_MB = 50
TOKEN_FILE = "secret_token.txt"
app = Flask(__name__)

# Ensure log directory exists
LOG_DIR.mkdir(exist_ok=True)

# Load bearer token
if not os.path.exists(TOKEN_FILE):
    raise FileNotFoundError(f"Missing {TOKEN_FILE}")
with open(TOKEN_FILE, "r") as f:
    BEARER_TOKEN = f.read().strip()

# Log a single event
def log_event(data):
    log_path = LOG_DIR / "current.jsonl"
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(data, ensure_ascii=False) + "\n")
    rotate_logs_if_needed()

# Rotate logs when current log file exceeds MAX_LOG_FILE_SIZE_MB
def rotate_logs_if_needed():
    current_log = LOG_DIR / "current.jsonl"
    if current_log.stat().st_size > MAX_LOG_FILE_SIZE_MB * 1024 * 1024:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        archived_log = LOG_DIR / f"log_{timestamp}.jsonl"
        gzip_path = str(archived_log) + ".gz"
        with open(current_log, 'rb') as f_in, gzip.open(gzip_path, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
        current_log.unlink()
        prune_old_logs()

# Prune old logs if total archived logs exceed MAX_TOTAL_LOG_ARCHIVE_SIZE_MB
def prune_old_logs():
    archives = sorted(LOG_DIR.glob("log_*.jsonl.gz"), key=os.path.getmtime)
    total_size = sum(f.stat().st_size for f in archives)
    while total_size > MAX_TOTAL_LOG_ARCHIVE_SIZE_MB * 1024 * 1024:
        oldest = archives.pop(0)
        total_size -= oldest.stat().st_size
        oldest.unlink()

@app.route("/ping", methods=["GET"])
def ping():
    return "OK", 200

@app.route("/run", methods=["POST"])
def run_script():
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer ") or auth_header.split(" ", 1)[1] != BEARER_TOKEN:
        log_event({"type": "auth_failure", "ip": request.remote_addr})
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json(force=True)
    script = data.get("script", "")

    log_event({"type": "script_received", "script": script[:1000], "ip": request.remote_addr})

    temp_file = f"temp_{uuid.uuid4().hex}.ps1"
    temp_file_path = os.path.abspath(temp_file)

    with open(temp_file_path, "w", encoding="utf-8") as f:
        f.write("Set-StrictMode -Version Latest\n")
        f.write(script)

    command = ["powershell.exe", "-ExecutionPolicy", "Bypass", "-File", temp_file_path]

    try:
        start_time = time.time()
        process = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=30
        )
        duration = round(time.time() - start_time, 2)

        log_data = {
            "type": "execution_result",
            "script": script[:1000],
            "stdout": process.stdout,
            "stderr": process.stderr,
            "exitCode": process.returncode,
            "duration_sec": duration,
            "ip": request.remote_addr
        }
        log_event(log_data)

        return jsonify({
            "stdout": process.stdout,
            "stderr": process.stderr,
            "exitCode": process.returncode
        })

    except subprocess.TimeoutExpired:
        log_event({
            "type": "timeout",
            "script": script[:1000],
            "ip": request.remote_addr
        })
        return jsonify({"error": "Command timed out"}), 408

    except Exception as e:
        log_event({
            "type": "server_error",
            "error": str(e),
            "ip": request.remote_addr
        })
        return jsonify({"error": "Internal server error"}), 500

    finally:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

if __name__ == "__main__":
    app.run(port=5000)
