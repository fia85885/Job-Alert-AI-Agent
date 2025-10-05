# gmail_client.py
import os
import os.path
import base64
from typing import List, Dict, Optional

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# For robust HTML -> text fallback (install via: pip install beautifulsoup4)
from bs4 import BeautifulSoup

# Scopes define the level of access you are requesting
SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]  # read + modify labels (mark as read)


# --------------------------
# Authentication
# --------------------------
def get_gmail_service():
    """
    Authenticates with the Gmail API and returns an authorized service object.
    Expects a local 'credentials.json' next to this file.
    Will create/refresh 'token.json' on first run / expiry.
    """
    creds = None
    token_path = "token.json"
    creds_path = "credentials.json"

    # Load existing token if present
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)

    # Refresh or run OAuth flow if needed
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(creds_path):
                raise FileNotFoundError(
                    "credentials.json not found. "
                    "Download your OAuth client credentials and place them next to this script."
                )
            flow = InstalledAppFlow.from_client_secrets_file(creds_path, SCOPES)
            # Opens a browser window for Google auth on first run
            creds = flow.run_local_server(port=0)

        # Save the token for next runs
        with open(token_path, "w", encoding="utf-8") as token:
            token.write(creds.to_json())

    return build("gmail", "v1", credentials=creds)


# --------------------------
# Helpers: headers & bodies
# --------------------------
def _b64url_decode_to_text(b64data: str) -> str:
    """
    Gmail uses URL-safe base64 without padding.
    This safely decodes to UTF-8 text, ignoring broken bytes.
    """
    return base64.urlsafe_b64decode(b64data + "==").decode("utf-8", errors="ignore")


def _get_header(headers: List[Dict[str, str]], name: str) -> Optional[str]:
    """Return the value for a header name (case-insensitive)."""
    name_lower = name.lower()
    for h in headers or []:
        if h.get("name", "").lower() == name_lower:
            return h.get("value")
    return None


def _extract_best_body(payload: Dict) -> str:
    """
    Walk the payload parts and return a best-effort text body.
    Preference:
      1) text/plain
      2) text/html (stripped to text)
    Ignores parts that only have attachmentId (no 'data').
    """
    text_plain, text_html = None, None
    stack = [payload] if payload else []

    while stack:
        part = stack.pop()

        # Recurse into nested multiparts
        for child in part.get("parts", []) or []:
            stack.append(child)

        mime = part.get("mimeType", "") or ""
        body = part.get("body", {}) or {}

        # Some parts (attachments) have 'attachmentId' but no 'data'
        data = body.get("data")
        if not data:
            continue

        try:
            content = _b64url_decode_to_text(data)
        except Exception:
            continue

        if mime.startswith("text/plain") and not text_plain:
            text_plain = content
        elif mime.startswith("text/html") and not text_html:
            # Strip HTML tags; keep reasonable spacing
            text_html = BeautifulSoup(content, "html.parser").get_text(separator="\n")

    return (text_plain or text_html or "").strip()


# --------------------------
# Main operations
# --------------------------
def get_job_emails(service, max_results: int = 20) -> List[Dict[str, str]]:
    """
    Fetch unread, job-related emails (subject/body keywords), extract Subject + text Body.
    Returns: list of dicts with keys: 'id', 'subject', 'body'
    """
    try:
        # Make subject intent explicit; also search body terms
        # Adjust/extend keywords as needed (LinkedIn, Naukri, Indeed, etc.)
        query = (
            'is:unread '
            '(subject:(job OR opportunity OR interview OR career) '
            'OR (job OR opportunity OR interview OR career))'
        )

        result = service.users().messages().list(
            userId="me", q=query, maxResults=max_results
        ).execute()

        messages = result.get("messages", []) or []
        if not messages:
            print("No new job-related emails found.")
            return []

        emails: List[Dict[str, str]] = []

        for m in messages:
            msg_id = m.get("id")
            if not msg_id:
                continue

            full = service.users().messages().get(
                userId="me", id=msg_id, format="full"
            ).execute()

            payload = full.get("payload", {}) or {}
            headers = payload.get("headers", []) or []
            subject = _get_header(headers, "Subject") or "(no subject)"

            body_text = _extract_best_body(payload)

            # Defensive cap AFTER HTML->text conversion
            if len(body_text) > 20000:
                body_text = body_text[:20000]

            emails.append(
                {
                    "id": msg_id,
                    "subject": subject.strip(),
                    "body": body_text.strip(),
                }
            )

        return emails

    except Exception as e:
        print(f"An error occurred while fetching emails: {e}")
        return []


def mark_as_read(service, msg_id: str) -> None:
    """
    Marks an email as read by removing the 'UNREAD' label.
    NOTE: Call this only after you successfully process/send the message.
    """
    try:
        service.users().messages().modify(
            userId="me",
            id=msg_id,
            body={"removeLabelIds": ["UNREAD"]},
        ).execute()
        print(f"Marked email {msg_id} as read.")
    except Exception as e:
        print(f"An error occurred while marking email as read: {e}")
