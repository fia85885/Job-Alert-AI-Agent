# summarizer.py
from openai import OpenAI
from config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

def summarize_email(subject, body):
    if not OPENAI_API_KEY:
        return "Error: OpenAI API key not configured."
    try:
        resp = client.chat.completions.create(
            model="gpt-4o-mini",  # cheaper/faster, adjust if you want
            messages=[
                {"role": "system", "content": "You are an expert at summarizing job emails for quick notifications."},
                {"role": "user", "content": f"""Summarize for WhatsApp:
- Company
- Role
- Action (apply/schedule/next steps)

Subject: {subject}

Body:
{body}"""}
            ],
            max_tokens=120,
            temperature=0.2
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        return f"Could not summarize the email ({e})."
