---

### 📘 `README.md` for PowerPilot v1.1

```markdown
# 🧠 PowerPilot – Secure Local GPT Automation via PowerShell

PowerPilot is a **local-first automation assistant** powered by a Custom GPT that connects to your Windows machine and executes PowerShell commands using natural language. You control the server. You authenticate the access. It does the work.

> ⚡️ Think of it as ChatGPT wired into your OS — with full control, visibility, and safety.

---

## 🚀 Features (v1.1)

- ✅ **Secure Execution**: Bearer-token protected API
- ✅ **Automatic OpenAPI Generation**: Live schema with ngrok URL
- ✅ **Painless Setup**: One command to start everything
- ✅ **Structured Logging**: JSON-per-line logs, gzipped & rotated
- ✅ **Timeout Handling**: Prevents stuck or runaway scripts
- ✅ **Portable**: Works from any local folder
- ✅ **Private**: Nothing runs outside your machine

---

## 📂 Repository Structure

```
PowerPilot-GPT/
│
├── launch_agent.py           # Launch server + tunnel + schema
├── server.py                 # Flask server handling PowerShell
├── openapi.json              # Generated OpenAPI schema
├── secret_token.txt          # Bearer token stored here
├── CHANGELOG.md              # Latest version changes
├── README.md                 # This file
├── logs/                     # Rotated, compressed JSON logs
└── assets/                   # Optional logo
```

---

## 🛠️ Setup Instructions

### 1. Download & Run PowerPilot Agent

Open an elevated PowerShell terminal and run:

```powershell
cd C:\Users\User\Documents\GPTAgent
python launch_agent.py
```

This will:

- Install dependencies (`flask`, `requests`)
- Download & initialize Ngrok
- Generate a secure Bearer token
- Create `openapi.json` with your live tunnel URL
- Start the Flask API server at `http://127.0.0.1:5000`

---

### 2. Create the Custom GPT

1. Go to [https://chat.openai.com/gpts/editor](https://chat.openai.com/gpts/editor)
2. Name it: **PowerPilot**
3. Upload the `openapi.json` that was just generated
4. Under **Authentication**:
   - Type: `Bearer`
   - Location: `Header`
   - Name: `Authorization`
   - Value: `Bearer <your-token>` (from `secret_token.txt`)
5. Paste in the contents of `.gpt_instructions.txt` into the **Instructions** field
6. Save and Test

---

### 3. Use PowerPilot!

Try prompts like:

- `Show top 10 largest files on C:\`
- `Scan for .ps1 files in Documents`
- `Start-Service WinDefend`
- `List scheduled tasks`
- `Remove all files from Temp folder older than 14 days`

---

## 🧾 Logging System (v1.1+)

- ✅ Logs stored in `logs/` folder
- ✅ JSON-per-line format
- ✅ Rotated after 30MB/file
- ✅ Archived to `.gz`
- ✅ Max folder size: 50MB (older logs deleted automatically)

---

## 🛡️ Security

- ✅ Authenticated via Bearer token (stored in `secret_token.txt`)
- ✅ Token is never hardcoded in source
- ✅ HTTPS endpoint served through Ngrok
- ✅ Flask server only accessible locally (127.0.0.1)

---

## 🔁 Development Notes

- PowerShell scripts are run with full error trapping and `Set-StrictMode`
- The Ngrok tunnel is HTTPS-only and regenerates with every launch
- The GPT relies solely on live server output — no simulated responses
- All commands are executed from a temporary `.ps1` file

---

## ❗ Known Limitations

- GPT must have access to live `openapi.json` + token
- You must leave `launch_agent.py` running for full GPT interaction
- Server should not be deployed to external machines without further hardening

---

## 🤝 Contributions

PRs are welcome! You can improve logging, command parsing, or even help expand PowerPilot to support other shells like Bash or CMD.

---

> 💬 Need help or want to show off what PowerPilot built? Open a GitHub Issue or start a Discussion!

```

---

## 🧾 2. Line-by-Line PowerShell Instructions to Create a GitHub Release

This time, we’ll **tag the release in Git**, then create the release on GitHub from PowerShell:

---

### 🪄 Step-by-Step (PowerShell)

> Assumes you’re on branch `v1.1` already.

1. **Create tag for v1.1:**

```powershell
git tag v1.1
```

2. **Push tag to GitHub:**

```powershell
git push origin v1.1
```

3. **Visit the GitHub Releases UI:**

```powershell
Start-Process "https://github.com/GhostwheeI/PowerPilot-GPT/releases/new"
```

4. In the webpage:
   - **Tag version**: `v1.1`
   - **Target**: `v1.1`
   - **Release title**: `PowerPilot v1.1 — Logging, Security, API Improvements`
   - **Paste the release body** from earlier

Then hit **"Publish release"** 🎉

---
