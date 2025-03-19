import os
import base64
import google.auth
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SCOPES = ["https://www.googleapis.com/auth/gmail.send"]
TOKEN_FILE = "token.json"
CREDENTIALS_FILE = "cred.json"
TEMPLATE_FILE = "email_template.html"


def authenticate_gmail():
    """Authenticate with Gmail API and return a service instance."""
    creds = None

    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=3000)

        with open(TOKEN_FILE, "w") as token:
            token.write(creds.to_json())

    return build("gmail", "v1", credentials=creds)


def render_email_template(name, title, total_questions, score):
    """Reads and fills the HTML email template."""
    with open(TEMPLATE_FILE, "r", encoding="utf-8") as file:
        template = file.read()

    return (
        template.replace("{{name}}", name)
        .replace("{{title}}", title)
        .replace("{{total_questions}}", str(total_questions))
        .replace("{{score}}", str(score))
    )


from datetime import datetime


def send_email(to_email, name, title, total_questions, score):
    """Send an email with a dynamically rendered HTML template."""
    service = authenticate_gmail()
    current_datetime = datetime.now().strftime("%d/%m/%Y %H:%M")

    # Create the email
    email_msg = MIMEMultipart()
    email_msg["From"] = "me"
    email_msg["To"] = to_email
    email_msg["Subject"] = f"KRISHTEC - 📊 Your Quiz Score Report - {current_datetime}"

    # Generate the HTML message
    html_content = render_email_template(name, title, total_questions, score)
    email_msg.attach(MIMEText(html_content, "html"))

    # Encode message to base64
    encoded_msg = base64.urlsafe_b64encode(email_msg.as_bytes()).decode("utf-8")

    message_data = {"raw": encoded_msg}

    try:
        service.users().messages().send(userId="me", body=message_data).execute()
        return "✅ Email sent successfully!"
    except Exception as e:
        return f"❌ Error sending email: {str(e)}"


# Example Usage
# send_email("recipient@example.com", "John Doe", "Python Basics", 10, 8)
