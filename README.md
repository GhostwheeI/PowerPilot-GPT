# 🧠 PowerPilot – Secure Local GPT Automation via PowerShell

PowerPilot is a **local-first automation assistant** powered by a Custom GPT that connects to your Windows machine and executes PowerShell commands using natural language. You control the server. You authenticate the access. It does the work.

> ⚡️ Think of it as ChatGPT wired into your OS — with full control, visibility, and safety.

---

## 🚀 Features (v1.1)

- ✅ Secure PowerShell execution via authenticated local API  
- ✅ Bearer token authentication (auto-generated)  
- ✅ HTTPS tunnel via Ngrok (auto-configured)  
- ✅ Automatic OpenAPI schema generation for Custom GPT upload  
- ✅ JSON-per-line logging with gzip rotation and size caps  
- ✅ Timeout handling for slow scripts  
- ✅ `Set-StrictMode -Version Latest` in all scripts  
- ✅ Server-side script validation + absolute path handling  
- ✅ Easily extensible backend architecture  

---

## 📂 Repository Structure

```
PowerPilot-GPT/
├── launch_agent.py         # Launches server + Ngrok + schema
├── server.py               # Flask API for PowerShell commands
├── openapi.json            # Action schema for GPT (auto-generated)
├── secret_token.txt        # Secure token used by GPT
├── CHANGELOG.md            # Version changelog
├── README.md               # You're reading it
├── logs/                   # Rotated .jsonl.gz log files
└── assets/                 # Optional logo or extras
```

---

## 🛠️ Setup Instructions

### 1. Download & Run PowerPilot Agent

Open an **elevated PowerShell terminal** and run:

```powershell
cd C:\Users\User\Documents\GPTAgent
python launch_agent.py
```

This will:

- Install Python packages (`flask`, `requests`)  
- Download and run Ngrok (HTTPS tunnel)  
- Generate a secure `secret_token.txt`  
- Create `openapi.json` with the live Ngrok URL  
- Launch the Flask API server on `http://127.0.0.1:5000`  

---

### 2. Set Up the Custom GPT

1. Visit [https://chat.openai.com/gpts/editor](https://chat.openai.com/gpts/editor)  
2. Name it: **PowerPilot**  
3. Upload the generated `openapi.json`  
4. Set **Authentication**:
   - Type: `Bearer`
   - Location: `Header`
   - Value: `Bearer <your token>` (from `secret_token.txt`)  
5. Paste the contents of `.gpt_instructions.txt` into the GPT Instructions field  
6. Save and test  

---

### 3. Use PowerPilot

Try natural language commands like:

- `List the 10 largest files on C:\`  
- `Stop-Service Spooler`  
- `Create a folder C:\Logs and move *.log files there`  
- `Enable scheduled defrag on system drive`  
- `Check event logs for errors in the last 24 hours`  

---

## 🧾 Logging System

- ✅ Logs every request/response to `logs/powerpilot.log.jsonl`  
- ✅ Uses JSON-per-line format for easy parsing  
- ✅ Automatically rotates after 30MB  
- ✅ Gzips old logs  
- ✅ Maintains total size under 50MB (auto-prunes oldest)  

---

## 🔐 Security Model

- Bearer token is generated once and stored in `secret_token.txt`  
- Token must be passed by GPT in `Authorization: Bearer <token>`  
- Server only accepts requests from localhost (`127.0.0.1`)  
- Public interface is routed only via HTTPS Ngrok  
- Token cannot be overridden or guessed by the GPT  

---

## 💡 Technical Design Highlights

- Uses Flask to host a minimal API at `/run` and `/ping`  
- Executes all PowerShell commands via temporary `.ps1` files  
- Validates and runs with `Set-StrictMode -Version Latest`  
- PowerShell launched with `-ExecutionPolicy Bypass`  
- Scripts timeout at 30 seconds (configurable)  
- Output includes full stdout and stderr  

---

## 🔁 Updating

To update:

1. Pull the latest repo changes  
2. Replace the existing `launch_agent.py` and `server.py`  
3. Run `launch_agent.py` again to refresh your token and schema  
4. Re-upload `openapi.json` to your GPT configuration  

---

## ⚠️ Known Limitations

- The Custom GPT **must be authenticated** and use the updated schema  
- Server must be running continuously during GPT interaction  
- Windows Defender may flag the Python tunnel (add exclusion)  
- This setup is for **local, private use only**  

---

## 🤝 Contributions

Pull requests are welcome! You can improve:

- Logging formats or destinations  
- Extended GPT-action support  
- Shell abstraction (for Bash or cross-platform)  

---

## 📄 License

MIT License

---

Made with 💻 by [@GhostwheeI](https://github.com/GhostwheeI)
