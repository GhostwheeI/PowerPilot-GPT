from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

# 🔐 Auto-injected by launch_agent.py
SECRET_TOKEN = "auto-injected-placeholder"  # auto-injected

# Default script execution timeout (in seconds)
DEFAULT_TIMEOUT_SECONDS = 30

@app.route("/run", methods=["POST"])
def run_command():
    auth_header = request.headers.get("Authorization")
    if auth_header != f"Bearer {SECRET_TOKEN}":
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    script = data.get("script")
    if not script:
        return jsonify({"error": "No script provided"}), 400

    try:
        result = subprocess.run(
            ["powershell", "-NoProfile", "-Command", script],
            capture_output=True,
            text=True,
            timeout=DEFAULT_TIMEOUT_SECONDS
        )
        return jsonify({
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip(),
            "exitCode": result.returncode
        })
    except subprocess.TimeoutExpired:
        return jsonify({"error": f"Command timed out after {DEFAULT_TIMEOUT_SECONDS} seconds."}), 504
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(port=8080)
