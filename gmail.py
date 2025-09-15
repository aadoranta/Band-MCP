import argparse
import base64
import pathlib
from pyexpat.errors import messages
import re
from typing import Optional

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# ----- CONFIG -----
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
CREDENTIALS = pathlib.Path("auth/credentials.json")
TOKEN = pathlib.Path("auth/token.json")
# ------------------


def get_gmail_service():
    creds = None
    if TOKEN.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN), SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not CREDENTIALS.exists():
                raise FileNotFoundError("credentials.json not found in working directory.")
            flow = InstalledAppFlow.from_client_secrets_file(str(CREDENTIALS), SCOPES)
            creds = flow.run_local_server(port=0)

        with open(TOKEN, "w") as f:
            f.write(creds.to_json())

    service = build("gmail", "v1", credentials=creds)
    return service


def find_thread_by_subject(service, subject, sender=None, days=7):
    # Build Gmail search query
    q = f'subject:"{subject}" newer_than:{days}d'
    if sender:
        q += f" from:{sender}"

    results = service.users().messages().list(userId="me", q=q, maxResults=10).execute()

    if "messages" not in results:
        raise LookupError("No messages found for that subject")

    # Take the first match
    msg_id = results["messages"][0]["id"]
    msg = service.users().messages().get(userId="me", id=msg_id).execute()

    return msg["threadId"]


def _decode_base64url(data: str) -> bytes:
    """Decode base64url text safely (handles missing padding)."""
    if not data:
        return b""
    # add padding if needed
    padding = len(data) % 4
    if padding:
        data += "=" * (4 - padding)
    return base64.urlsafe_b64decode(data.encode("utf-8"))


def extract_text_from_payload(payload) -> str:
    """
    Recursively find and decode the first text/plain or text/html payload found.
    Returns decoded string (may contain HTML).
    """
    # If payload itself has body.data (simple message)
    body = payload.get("body", {}).get("data")
    if body:
        try:
            return _decode_base64url(body).decode("utf-8", errors="replace")
        except Exception:
            return _decode_base64url(body).decode("latin-1", errors="replace")

    # Otherwise, look into parts
    for part in payload.get("parts", []) or []:
        # prefer text/plain but accept HTML if that's all there is
        mime = part.get("mimeType", "")
        # if this part itself has data, decode it
        part_body = part.get("body", {}).get("data")
        if part_body:
            text = _decode_base64url(part_body)
            try:
                return text.decode("utf-8", errors="replace")
            except Exception:
                return text.decode("latin-1", errors="replace")
        # otherwise recurse
        text = extract_text_from_payload(part)
        if text:
            return text
    return ""


def get_header(message, name: str) -> Optional[str]:
    for h in message.get("payload", {}).get("headers", []):
        if h.get("name", "").lower() == name.lower():
            return h.get("value")
    return None


def pull_thread(service, thread_id: str):
    """
    Fetch a thread and pretty-print message headers + body.
    Uses format='full' so the payload is populated.
    """
    thread = service.users().threads().get(userId="me", id=thread_id, format="full").execute()
    messages = thread.get("messages", [])
    results = []
    for i, msg in enumerate(messages, start=1):
        subject = get_header(msg, "Subject") or "(no subject)"
        sender = get_header(msg, "From") or "(no from)"
        date = get_header(msg, "Date") or "(no date)"
        to = get_header(msg, "To") or "(no to)"
        body = extract_text_from_payload(msg.get("payload", {})) or "(no body found)"
        results.append(
            {
                "index": i,
                "id": msg.get("id"),
                "subject": subject,
                "from": sender,
                "to": to,
                "date": date,
                "body": body,
            }
        )
    return results


def get_email_contents_from_subject(subject_line):

    service = get_gmail_service()
    thread_id = find_thread_by_subject(service, subject=subject_line)
    print("Using thread id:", thread_id)

    service = get_gmail_service()
    # optional: verify which account we authorized as
    profile = service.users().getProfile(userId="me").execute()
    print("Authorized as:", profile.get("emailAddress"))

    messages = pull_thread(service, thread_id)
    results = {}
    for i, m in enumerate(messages):
        results[i] = {
            "id": m["id"],
            "from": m["from"],
            "to": m["to"],
            "date": m["date"],
            "subject": m["subject"],
            "body": m["body"],
        }
    return results
