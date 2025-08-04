# 📁 PowerPilot-GPT Repository Structure

```
PowerPilot-GPT/
│
├── README.md
├── launch_agent.py
├── server.py
├── openapi_template.json
├── .gpt_instructions.txt
├── requirements.txt
└── assets/
    └── powerpilot-logo.png (optional placeholder)
```

---

## 📄 1. `README.md`

```markdown
# 🧠 PowerPilot – Local PowerShell Control via GPT

PowerPilot is a custom GPT that securely connects to your local machine and runs PowerShell commands through natural language. You control it. It runs locally. It’s private, powerful, and customizable.

---

## 🚀 Features

- ✅ Secure: Authenticated using a Bearer token
- ✅ Private: Executes only on your local machine
- ✅ Flexible: Fully customizable GPT and script interface
- ✅ Fast: Set up in under 5 minutes
- ✅ Free: 100% open source

---

## 🛠️ Setup Instructions (5 Minutes)

### 1. Download & Run PowerPilot Agent

- Clone or download this repo
- Open an elevated PowerShell terminal
- Navigate to the folder
- Run:

```bash
python launch_agent.py
```

This will:

- Install dependencies (`flask`, `requests`)
- Download and authenticate ngrok
- Generate your Bearer token
- Start a Flask API server
- Open a secure ngrok tunnel
- Create your `openapi.json`

---

### 2. Create Your Custom GPT

1. Go to [https://chat.openai.com/gpts/editor](https://chat.openai.com/gpts/editor)
2. Name your GPT: **PowerPilot**
3. Upload the generated `openapi.json`
4. Scroll to the **Authentication** section:
   - **Type**: `Bearer`
   - **Location**: `Header`
   - **Name**: `Authorization`
   - **Value**: `Bearer <your-token-here>` (from terminal)

5. In the **Instructions** field, paste the contents of `.gpt_instructions.txt`

6. Click Save & Test!

---

### 3. Try It!

Ask PowerPilot things like:

- `Get top 5 processes`
- `List .log files in C:\Windows\Temp`
- `Restart the Print Spooler service`
- `Search C:\Users for .ps1 scripts`

---

## 🛡️ Safety

- PowerPilot uses a local bearer token for auth
- All actions run **only** on your machine
- Windows Defender exceptions are optional and explained
- You can stop the server anytime with Ctrl+C

---

## 🧠 Want to Contribute?

PRs and suggestions are welcome!
```

---

## 🧾 2. `.gpt_instructions.txt`

```txt
You are PowerPilot — a secure local PowerShell assistant.

Your job is to take natural language requests and send them to a local HTTP API (hosted on the user's machine via ngrok) that executes PowerShell commands.

Instructions:

- Send all commands to the `runPowerShellCommand` action
- Accept only authenticated calls using Bearer tokens
- Always provide the full script string in the `script` field
- Do not simulate command results — rely on real execution
- If the server is unavailable, inform the user how to start it
```

---

## 🧪 3. `requirements.txt`

```txt
flask
requests
```

---

## ⚙️ 4. `openapi_template.json`

This is optional since `launch_agent.py` auto-generates `openapi.json`, but if you want a static template:

```json
{
  "openapi": "3.1.0",
  "info": {
    "title": "PowerPilot API",
    "version": "1.0.0"
  },
  "servers": [{ "url": "https://your-url.ngrok.io" }],
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
        "summary": "Run a PowerShell command",
        "requestBody": {
          "required": true,
          "content": {
            "application/json": {
              "schema": {
                "type": "object",
                "properties": {
                  "script": { "type": "string" }
                },
                "required": ["script"]
              }
            }
          }
        },
        "responses": {
          "200": {
            "description": "Execution output",
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
          "401": { "description": "Unauthorized" }
        }
      }
    }
  }
}
```

---

## 🖼️ 5. `assets/powerpilot-logo.png` (optional)

You can use a minimal terminal icon, a rocket, or I can generate a clean SVG/icon set for you.

---

## ✅ Final Step

Just upload this to GitHub and share the link publicly.  
Here’s a good repo description:

> 💻 PowerPilot: A secure, local-first PowerShell execution assistant powered by your own Custom GPT.
