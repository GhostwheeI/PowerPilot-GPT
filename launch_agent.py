# --------------------------------------------
# Auto-install required packages if missing
# --------------------------------------------
import sys
import subprocess

REQUIRED_PACKAGES = ["requests", "flask"]
for package in REQUIRED_PACKAGES:
    try:
        __import__(package)
    except ImportError:
        print(f"📦 Installing missing package: {package}")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# --------------------------------------------
# Main script logic starts here
# --------------------------------------------
import os
import time
import zipfile
import shutil
import json
import uuid
from pathlib import Path
import requests

# -----------------------------
# Configuration
# -----------------------------
BASE_DIR = Path(__file__).parent.resolve()
NGROK_DIR = BASE_DIR / "ngrok"
NGROK_EXE = NGROK_DIR / "ngrok.exe"
NGROK_ZIP_URL = "https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-stable-windows-amd64.zip"
AUTH_TOKEN_FILE = NGROK_DIR / "auth_token.txt"
TOKEN_FILE = BASE_DIR / "secret_token.txt"
FLASK_PORT = 8080
OPENAPI_FILE = BASE_DIR / "openapi.json"

# -----------------------------
# Defender Exclusion (optional)
# -----------------------------
def offer_windows_defender_exclusion():
    print("\n🛡️ Windows Defender may interfere with the script or ngrok.")
    print(f"   Would you like to add a Defender exclusion for this folder?\n   → {BASE_DIR}")
    choice = input("   Type 'yes' to proceed: ").strip().lower()
    if choice == "yes":
        try:
            subprocess.run([
                "powershell", "-NoProfile", "-Command",
                f"Add-MpPreference -ExclusionPath '{BASE_DIR}'"
            ], check=True)
            print("✅ Exclusion added successfully.")
        except Exception as e:
            print(f"❌ Failed to add exclusion: {e}")
    else:
        print("⏭️ Skipping Defender exclusion.")

# -----------------------------
# Token Handling
# -----------------------------
def generate_token():
    if TOKEN_FILE.exists():
        return TOKEN_FILE.read_text().strip()
    token = str(uuid.uuid4())
    TOKEN_FILE.write_text(token)
    print(f"🔐 New secret token generated and saved to: {TOKEN_FILE}")
    return token

def inject_token_into_server_py(token: str):
    server_path = BASE_DIR / "server.py"
    if not server_path.exists():
        print("❌ server.py not found.")
        return

    contents = server_path.read_text(encoding="utf-8")
    new_contents = []
    replaced = False
    for line in contents.splitlines():
        if line.strip().startswith("SECRET_TOKEN"):
            new_contents.append(f'SECRET_TOKEN = "{token}"  # auto-injected')
            replaced = True
        else:
            new_contents.append(line)

    if replaced:
        server_path.write_text("\n".join(new_contents), encoding="utf-8")
        print("🔐 Secret token injected into server.py.")
    else:
        print("⚠️ SECRET_TOKEN line not found in server.py.")

# -----------------------------
# Ngrok Setup
# -----------------------------
def download_ngrok():
    print("📦 Downloading ngrok...")
    zip_path = NGROK_DIR / "ngrok.zip"
    NGROK_DIR.mkdir(parents=True, exist_ok=True)

    with requests.get(NGROK_ZIP_URL, stream=True) as r:
        with open(zip_path, "wb") as f:
            shutil.copyfileobj(r.raw, f)

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(NGROK_DIR)

    zip_path.unlink()
    print("✅ Ngrok downloaded and extracted.")

def configure_ngrok():
    if not AUTH_TOKEN_FILE.exists():
        print("🔐 Ngrok auth token not found.")
        token = input("🔑 Enter your Ngrok auth token: ").strip()
        subprocess.run([str(NGROK_EXE), "config", "add-authtoken", token], check=True)
        AUTH_TOKEN_FILE.write_text(token)
        print("✅ Ngrok authenticated.")
    else:
        print("🔐 Ngrok auth token already configured.")

def start_ngrok_tunnel():
    print("🌐 Starting ngrok tunnel...")
    proc = subprocess.Popen([str(NGROK_EXE), "http", str(FLASK_PORT)], stdout=subprocess.DEVNULL)
    time.sleep(3)
    try:
        resp = requests.get("http://localhost:4040/api/tunnels")
        public_url = resp.json()["tunnels"][0]["public_url"]
        print(f"✅ Ngrok URL: {public_url}")
        return proc, public_url
    except Exception as e:
        print(f"❌ Failed to fetch ngrok URL: {e}")
        proc.terminate()
        return None, None

# -----------------------------
# Flask Server
# -----------------------------
def start_flask_server():
    print("🚀 Starting Flask server...")
    return subprocess.Popen(["python", "server.py"], cwd=str(BASE_DIR))

# -----------------------------
# OpenAPI Spec Generator
# -----------------------------
def write_openapi_json(public_url: str, token: str):
    print("📝 Generating secure openapi.json...")
    schema = {
        "openapi": "3.1.0",
        "info": {
            "title": "Local PowerShell Runner",
            "version": "1.0.0"
        },
        "servers": [{"url": public_url}],
        "components": {
            "securitySchemes": {
                "BearerAuth": {
                    "type": "http",
                    "scheme": "bearer",
                    "bearerFormat": "Token"
                }
            },
            "schemas": {}
        },
        "security": [{ "BearerAuth": [] }],
        "paths": {
            "/run": {
                "post": {
                    "operationId": "runPowerShellCommand",
                    "summary": "Run a PowerShell command locally",
                    "security": [{ "BearerAuth": [] }],
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "script": {
                                            "type": "string",
                                            "description": "PowerShell script to execute"
                                        }
                                    },
                                    "required": ["script"]
                                }
                            }
                        }
                    },
                    "responses": {
                        "200": {
                            "description": "Command result",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "stdout": {"type": "string"},
                                            "stderr": {"type": "string"},
                                            "exitCode": {"type": "integer"}
                                        }
                                    }
                                }
                            }
                        },
                        "401": {
                            "description": "Unauthorized"
                        }
                    }
                }
            }
        }
    }
    with OPENAPI_FILE.open("w", encoding="utf-8") as f:
        json.dump(schema, f, indent=2)
    print(f"✅ openapi.json created at: {OPENAPI_FILE}")

# -----------------------------
# Main Routine
# -----------------------------
def main():
    offer_windows_defender_exclusion()
    shared_secret = generate_token()
    inject_token_into_server_py(shared_secret)

    if not NGROK_EXE.exists():
        download_ngrok()
    configure_ngrok()

    flask_proc = start_flask_server()
    time.sleep(1)

    ngrok_proc, ngrok_url = start_ngrok_tunnel()
    if ngrok_url:
        write_openapi_json(ngrok_url, shared_secret)

        print("\n🔗 Upload the generated openapi.json when configuring your Custom GPT.")
        print("🔐 Authentication Setup (REQUIRED in GPT Builder):")
        print("   1. Scroll to the **Authentication** section above the Schema field.")
        print("   2. Click **'Add authentication'**.")
        print("   3. Choose:")
        print("      - Type:       Bearer")
        print("      - Location:   Header")
        print("      - Name:       Authorization")
        print("      - Value:      Bearer " + shared_secret)
        print("   4. Click Save ✅")

        print("\n📝 Authorization header (copy-paste ready):")
        print(f"    Authorization: Bearer {shared_secret}")

        print(f"\n📂 Token saved to: {TOKEN_FILE}")
        print("🟢 Endpoint is live. Press Ctrl+C to stop.")
        try:
            flask_proc.wait()
        except KeyboardInterrupt:
            print("\n🛑 Shutting down...")
            flask_proc.terminate()
            ngrok_proc.terminate()
    else:
        flask_proc.terminate()

if __name__ == "__main__":
    main()
