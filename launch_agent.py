import os
import subprocess
import sys
import uuid
import json
import shutil
import zipfile
import urllib.request
import time
from pathlib import Path

# Constants
PORT = 5000
NGROK_FILENAME = "ngrok.exe"
NGROK_ZIP = "ngrok.zip"
NGROK_URL = "https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-stable-windows-amd64.zip"
NGROK_AUTHTOKEN = os.environ.get("NGROK_AUTHTOKEN")
NGROK_PATH = Path(NGROK_FILENAME)
OPENAPI_PATH = Path("openapi.json")
SECRET_TOKEN_PATH = Path("secret_token.txt")
SERVER_SCRIPT = "server.py"

# Ensure ngrok is installed
def download_ngrok():
    print("[*] Downloading ngrok...")
    urllib.request.urlretrieve(NGROK_URL, NGROK_ZIP)
    with zipfile.ZipFile(NGROK_ZIP, 'r') as zip_ref:
        zip_ref.extractall(".")
    os.remove(NGROK_ZIP)
    print("[+] ngrok downloaded successfully.")

# Check if package is installed, else install
def ensure_python_package(package):
    try:
        __import__(package)
    except ImportError:
        print(f"[*] Installing {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Ensure required packages
ensure_python_package("requests")

import requests

# Generate a secure token
def generate_token():
    token = uuid.uuid4().hex
    SECRET_TOKEN_PATH.write_text(token, encoding="utf-8")
    return token

# Read or create token
def get_token():
    if SECRET_TOKEN_PATH.exists():
        return SECRET_TOKEN_PATH.read_text().strip()
    return generate_token()

# Launch the local API server
def launch_server():
    print("[*] Launching PowerPilot local server...")
    subprocess.Popen([sys.executable, SERVER_SCRIPT])
    time.sleep(3)

# Start ngrok tunnel
def start_ngrok():
    if not NGROK_PATH.exists():
        download_ngrok()

    print("[*] Starting ngrok tunnel...")
    ngrok_cmd = [str(NGROK_PATH), "http", str(PORT)]
    subprocess.Popen(ngrok_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # Wait for ngrok to come online
    public_url = None
    for _ in range(20):
        try:
            resp = requests.get("http://localhost:4040/api/tunnels")
            tunnels = resp.json().get("tunnels", [])
            for tunnel in tunnels:
                url = tunnel.get("public_url", "")
                if url.startswith("http"):
                    public_url = url
                    break
            if public_url:
                break
        except Exception:
            time.sleep(1)

    if not public_url:
        print("[!] Failed to retrieve ngrok public URL. Is ngrok running?")
        sys.exit(1)

    # ✅ Force HTTPS for GPT compatibility
    if public_url.startswith("http://"):
        public_url = public_url.replace("http://", "https://")

    print(f"[+] Ngrok tunnel: {public_url}")
    return public_url

# Generate and write full OpenAPI schema
def write_openapi(public_url, token):
    openapi = {
        "openapi": "3.1.0",
        "info": {
            "title": "PowerPilot API",
            "version": "1.0.0",
            "description": "Local PowerShell automation assistant using secure API access"
        },
        "servers": [
            { "url": public_url }
        ],
        "paths": {
            "/run": {
                "post": {
                    "operationId": "runPowerShellCommand",
                    "summary": "Run a PowerShell script on the local system",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "script": {
                                            "type": "string",
                                            "description": "The full PowerShell script or command to execute"
                                        }
                                    },
                                    "required": ["script"]
                                }
                            }
                        }
                    },
                    "responses": {
                        "200": {
                            "description": "Successful execution",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "stdout": { "type": "string" },
                                            "stderr": { "type": "string" },
                                            "exitCode": { "type": "integer" }
                                        }
                                    }
                                }
                            }
                        },
                        "400": { "description": "Bad request or script error" },
                        "401": { "description": "Unauthorized" },
                        "408": { "description": "Command timed out" }
                    }
                }
            }
        },
        "components": {
            "securitySchemes": {
                "BearerAuth": {
                    "type": "http",
                    "scheme": "bearer"
                }
            },
            "schemas": {}
        },
        "security": [
            {
                "BearerAuth": []
            }
        ]
    }

    with open(OPENAPI_PATH, "w", encoding="utf-8") as f:
        json.dump(openapi, f, indent=2)

    print("[✓] openapi.json created with live Ngrok endpoint.")

# Optional: notify user about Defender
def suggest_defender_exclusion():
    print("\n⚠️  [INFO] If Windows Defender flags this tool, you may need to exclude this folder manually.")
    print("   Recommended exclusion path:", os.getcwd())

# Main logic
def main():
    token = get_token()
    launch_server()
    public_url = start_ngrok()
    write_openapi(public_url, token)
    suggest_defender_exclusion()
    print("\n[✅] PowerPilot is ready. Upload openapi.json to your Custom GPT Actions.")
    print("[ℹ️] Ngrok and the server are running in the background.")
    print("[🔒] Leave this window open while using PowerPilot.")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[!] PowerPilot shutting down.")

if __name__ == "__main__":
    main()
