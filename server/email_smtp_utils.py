import threading
import queue
import json
import uuid
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
from django.http import JsonResponse
import time

TEMPLATE_FILE = "email_template.html"

# Create a queue for email processing
email_queue = queue.Queue()


# **Email Worker Thread** (Processes emails from the queue with delays to prevent throttling)
def email_worker():
    while True:
        to_email, name, title, total_questions, score = email_queue.get()
        if to_email is None:  # Exit signal
            break

        try:
            send_email_smtp(to_email, name, title, total_questions, score)
        except Exception as e:
            print(f"❌ Error sending email to {to_email}: {e}")
        email_queue.task_done()
        time.sleep(1)  # Adding delay between emails to avoid rate limiting


# Start the worker thread
email_thread = threading.Thread(target=email_worker, daemon=True)
email_thread.start()


# Function to add email to the queue
def queue_email(to_email, name, title, total_questions, score):
    email_queue.put((to_email, name, title, total_questions, score))


# **HTML Template Renderer**
def render_email_template(name, title, total_questions, score):
    with open(TEMPLATE_FILE, "r", encoding="utf-8") as file:
        template = file.read()

    return (
        template.replace("{{name}}", name)
        .replace("{{title}}", title)
        .replace("{{total_questions}}", str(total_questions))
        .replace("{{score}}", str(score))
    )


# **SMTP Email Sender Function with Exponential Backoff**
def send_email_smtp(to_email, name, title, total_questions, score):
    from_email = "aptitude@krishtec.co.in"
    password = "KRISHtec@5747"
    attempt = 0
    delay = 5  # Initial retry delay

    while attempt < 5:  # Retry up to 5 times
        try:
            current_datetime = datetime.now().strftime("%d/%m/%Y %H:%M")
            msg = MIMEMultipart()
            msg["From"] = from_email
            msg["To"] = to_email
            msg["Subject"] = (
                f"KRISHTEC - 📊 Your Quiz Score Report - {current_datetime}"
            )
            html_content = render_email_template(name, title, total_questions, score)
            msg.attach(MIMEText(html_content, "html"))

            server = smtplib.SMTP("mail.krishtec.co.in", 587)
            server.starttls()
            server.login(from_email, password)
            server.sendmail(from_email, to_email, msg.as_string())
            server.quit()
            print(f"✅ Email sent to {to_email}")
            return "✅ Email sent successfully!"
        except smtplib.SMTPException as e:
            print(f"⚠️ SMTP Error: {e}")
            attempt += 1
            time.sleep(delay)
            delay *= 2  # Increase delay exponentially on failure
    print(f"❌ Failed to send email to {to_email} after retries.")
    return f"❌ Failed to send email to {to_email}"
