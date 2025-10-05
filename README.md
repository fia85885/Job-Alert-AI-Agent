# 📩 Email to WhatsApp – AI Agent
An automated Python-based AI Agent that reads job-related emails from your Gmail inbox, summarizes them using OpenAI, and forwards the summaries to your WhatsApp via Twilio.

This project is designed to act as your personal job alert assistant, keeping you updated with concise job opportunities directly on WhatsApp — without needing to open your email.

## 🧠 Features
✅ Connects securely to Gmail using OAuth 2.0 (credentials.json + token.json)

📥 Fetches unread job-related emails using smart search queries

📝 Extracts email subject and body, handling both plain text and HTML formats

🧠 Summarizes the content using OpenAI GPT (e.g., GPT-4o-mini) for quick scanning

📲 Sends the summarized information to your WhatsApp number using Twilio's API

🔄 Marks emails as read only after successful send to avoid data loss

🔐 Uses .env file for secrets (OpenAI API key, Twilio credentials)

🪶 Lightweight, modular structure – each file has a clear responsibility

## 📁 Project Structure
/Email to WhatsApp/
│
├── agent.py               # Main orchestrator - runs the entire AI agent workflow
├── gmail_client.py        # Handles Gmail authentication & email fetching
├── summarizer.py          # Summarizes email content using OpenAI API
├── whatsapp_client.py     # Sends messages to WhatsApp via Twilio API
├── config.py              # Loads environment variables and app settings
├── requirements.txt       # All Python dependencies for the project
├── .env                   # Secret keys and credentials (NOT to be committed)
├── credentials.json       # OAuth 2.0 client credentials from Google Cloud
├── token.json             # Automatically generated Gmail access token
└── README.md              # 📄 Project documentation (this file)

## ⚙️ File-by-File Breakdown
### 1. agent.py — 🧠 Main AI Agent
This is the entry point of the application. It ties everything together:

Loads the Gmail service.

Fetches unread job-related emails.

Summarizes their content.

Sends the summaries to WhatsApp.

Marks emails as read only after successful delivery.

Key Responsibilities:

Implements the continuous polling loop (with a sleep interval).

Ensures error handling so the agent runs smoothly for hours.

Maintains logs to track processed messages.

### 2. gmail_client.py — 📬 Email Fetching Module
Handles Gmail API authentication and robust email extraction.

Main Components:

get_gmail_service(): Authenticates using credentials.json and token.json to return a Gmail API service instance.

_extract_best_body(payload): Safely extracts text from multipart emails. Prefers text/plain, falls back to text/html.

get_job_emails(service): Uses a search query to find job-related unread emails. Returns structured data with id, subject, and body.

mark_as_read(service, msg_id): Marks emails as read after successful WhatsApp send.

Why it matters: Gmail messages often come in complex multipart formats (text, HTML, attachments). This module ensures reliable extraction without crashing.

### 3. summarizer.py — 📝 AI Summarization Engine
Uses the OpenAI API to generate short, structured summaries of the email content.

Main Steps:

Initializes the OpenAI client with your API key from .env.

Sends a prompt to summarize the job email.

Returns a concise message suitable for WhatsApp.

You can modify the prompt to fit your preferred style (e.g., JSON, bullet points, etc.).

### 4. whatsapp_client.py — 📲 WhatsApp Sender
Handles communication with Twilio's WhatsApp API.

Key Responsibilities:

Initializes Twilio client using TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN from .env.

Sends WhatsApp messages to your number.

Handles errors gracefully (e.g., sandbox verification issues).

Note: If you’re using a Twilio trial account, the recipient must first join the Twilio WhatsApp sandbox and verify their number.

### 5. config.py — ⚡ Configuration Loader
Centralizes environment variables from .env:

OPENAI_API_KEY

TWILIO_ACCOUNT_SID

TWILIO_AUTH_TOKEN

TWILIO_WHATSAPP_NUMBER

YOUR_WHATSAPP_NUMBER

This prevents hardcoding secrets in multiple places and allows easy configuration changes.

### 6. .env — 🔐 Environment Variables
Stores all sensitive credentials in one place. Example:

OPENAI_API_KEY=sk-xxxxxx
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=xxxxxxxxxxxxxx
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
YOUR_WHATSAPP_NUMBER=whatsapp:+91XXXXXXXXXX

⚠️ Never commit this file to GitHub. > Add .env to .gitignore.

### 7. credentials.json & token.json — 🔑 Gmail OAuth
credentials.json → Downloaded from Google Cloud Console (OAuth client ID).

token.json → Automatically generated when you first authenticate. It stores your access + refresh tokens.

Do not share these files publicly. Treat them like passwords.

### 8. requirements.txt — 📦 Dependencies
Contains all Python dependencies. Install with:

pip install -r requirements.txt

🚀 Getting Started
1️⃣ Clone & Enter Project
git clone <your-repo-url>
cd "Email to WhatsApp"

2️⃣ Set Up Virtual Environment
python -m venv venv
venv\Scripts\activate   # Windows
# or
source venv/bin/activate  # Mac/Linux

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Add Your .env File
Create a .env in the root folder and fill in your OpenAI & Twilio credentials.

5️⃣ Add credentials.json
Download your Gmail OAuth client credentials from Google Cloud Console, and place them in the project root.

6️⃣ First Run
python agent.py

On first run:

A browser window opens asking you to sign in to Gmail and grant access.

token.json is created for future runs.

The agent starts checking your inbox every 5 minutes.

🛠 How It Works (Workflow)
Gmail Client connects to your inbox and searches for unread job-related emails using a smart query.

Each email’s subject & body are parsed and cleaned.

The Summarizer sends the email to OpenAI’s model, which returns a short, structured summary.

The WhatsApp Client sends this summary to your number using Twilio’s API.

Once successful, the email is marked as read to avoid duplicates.

📝 Customization Tips
Keywords: Modify the Gmail search query in gmail_client.py to include other job terms (e.g., “internship”, “vacancy”, company names).

Summary Style: Edit the prompt in summarizer.py for different formats (e.g., JSON, bullet points, hashtags).

Polling Frequency: Change the time.sleep(300) in agent.py to a different interval (e.g., 60s for more frequent checks).

Multi-user: Extend .env and Twilio logic to send messages to multiple recipients.

⚠️ Security Notes
✅ Never push .env, credentials.json, or token.json to public repositories.

🔑 Rotate your keys if you ever shared these files accidentally.

🧼 Add .gitignore entries for all sensitive files:

.env
credentials.json
token.json

🧪 Testing
To test Gmail parsing separately:

python -c "from gmail_client import get_gmail_service, get_job_emails; s=get_gmail_service(); print(get_job_emails(s))"

To test Twilio separately:

python -c "from whatsapp_client import send_whatsapp_message; send_whatsapp_message('Test message ✅')"

🧭 Roadmap
[ ] Add cron job / background service support

[ ] Add label-based filtering for more accurate detection

[ ] Support multiple Gmail accounts - [ ] Add database to store processed messages

[ ] Add a web dashboard for message logs

✨ Credits
Gmail API — Google Developers

OpenAI API — OpenAI Platform

Twilio WhatsApp API — Twilio Docs

📜 License
This project is for personal use only.

Before deploying publicly, ensure you comply with Gmail & Twilio's Terms of Service.

MIT License
© 2025 Furqan Ahmed Khan

Happy automating 🚀

Your personal job assistant, straight to WhatsApp.
