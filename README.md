# 🚀 PowerPilot 1.1 — Local GPT-Driven Automation with PowerShell & Python

**PowerPilot** is a secure, local-first automation framework that connects a Custom GPT to your Windows environment using a Python-powered API gateway and Ngrok tunnel. Version 1.1 is a complete overhaul of the original, focusing on robust script execution, enhanced observability, and deep integration support for PowerShell and Python workflows.

---

## 🔧 Features

| Capability | Description |
|------------|-------------|
| ✅ GPT-Triggered Execution | Connects your Custom GPT to your Windows endpoint using Ngrok |
| ✅ PowerShell API | GPT sends commands via the `/run` endpoint with secure authentication |
| ✅ Secure API Token | Uses unique bearer token for every local deployment |
| ✅ Full Logging | JSONL logs with rotation, compression, and retention limits |
| ✅ Timeout Handling | Prevents runaway scripts (default: 30 seconds) |
| ✅ Log Compression | Logs auto-rotate at 30MB and are zipped |
| ✅ Rolling Log Retention | Old logs are pruned once 50MB total is exceeded |
| ✅ GUI-Free Setup | No installer required — just run from PowerShell |
| ✅ GPT-First UX | Designed from scratch for Custom GPT integration and usage

---

## 🔐 Security

- All external access goes through Ngrok (HTTPS)
- Token-based bearer authentication for every request
- Temp PowerShell scripts are validated before execution and deleted after

---

## 📁 Folder Structure

```
PowerPilot-GPT/
├── launch_agent.py         # Main setup + Ngrok launcher + schema generator
├── server.py               # Flask API server for executing PowerShell commands
├── openapi.json            # Automatically generated Custom GPT schema
├── secret_token.txt        # Generated bearer token (keep secret!)
├── logs/                   # JSONL logs with rotation and compression
```

---

## ⚙️ Setup

> 💡 Only requirements: Python 3.10+ and Windows 10/11 (Pro recommended)

### 1. Clone the Repo

```bash
git clone https://github.com/GhostwheeI/PowerPilot-GPT.git
cd PowerPilot-GPT
```

### 2. Run It

```powershell
python launch_agent.py
```

✅ This will:
- Start your Flask server
- Start Ngrok
- Create `openapi.json`
- Print the public HTTPS tunnel URL
- Generate your bearer token in `secret_token.txt`

### 3. Upload to GPT

- Go to [chat.openai.com/gpts](https://chat.openai.com/gpts)
- Edit your Custom GPT
- Under **Actions**, upload `openapi.json`
- Under **Authentication**, choose:
  - Type: `Bearer`
  - Key: (paste the token from `secret_token.txt`)
- Save and test the `/run` action

---

## 📊 Logs

All logs are written to `logs/current.jsonl` in JSON-per-line format for easy parsing. They include:
- Type: `script_received`, `execution_result`, `timeout`, `auth_failure`
- IP address (local)
- Full stdout/stderr
- Exit code
- Duration

Logs rotate when they exceed **30MB**, compress into `.gz`, and prune oldest logs beyond **50MB** total.

---

## 📘 What's New in 1.1

| Area | 1.0 | 1.1 |
|------|-----|-----|
| OpenAPI | Static file | Live-generated with Ngrok URL |
| Auth | Hardcoded token | Unique token stored in file |
| Logging | Minimal | JSONL + rotation + archive retention |
| Execution | Basic PowerShell | Temp script with `Set-StrictMode`, full path |
| Security | None | Bearer + HTTPS enforced |
| Persistence | Manual | Ngrok + Flask kept alive |
| Developer UX | Minimal | Setup, output, Defender warnings added |
| Versioning | Manual | Structured versioning now supported |

---

## 🧠 Ideal Use Cases

- Execute PowerShell from GPT prompts
- Create full automation suites
- Integrate Python-based preprocessing, scripting, or conversion tools
- Build frontend GUIs with a GPT-assisted backend (via CLI or codegen)

---

## 🔮 Future Plans

- Optional `/runPythonScript` endpoint
- Modular action support for running `.ps1`, `.py`, or `.exe` scripts
- Auto-extract info from logs
- GPT-guided script execution history + replay

---

## 🧼 Troubleshooting

- Defender blocking? Add an exclusion:
  ```
  C:\Path\To\PowerPilot-GPT
  ```
- Ngrok not working? Ensure it’s not firewalled or blocked.
- Getting `401 Unauthorized`? Double-check the bearer token in your GPT config.
- Ngrok URL expired? Just re-run `launch_agent.py`.

---

## 🧪 Version

- PowerPilot 1.1
- OpenAPI: 3.1.0
- Python 3.10+
- GPT 4 or 4o compatible

---

## 🛡️ License

MIT — see [LICENSE](LICENSE)