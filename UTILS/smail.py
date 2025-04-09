import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

TEMPLATE_FILE = "email_template.html"  # Make sure to provide the correct path to your HTML template file


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


def send_email_smtp(to_email, name, title, total_questions, score):
    from_email = "balajic@drngpit.ac.in"
    password = "#Balaji@472003"

    # Create the email message
    msg = MIMEMultipart()
    msg["From"] = from_email
    msg["To"] = to_email
    msg["Subject"] = f"📊 Your Quiz Score Report - {title}"

    # Generate the HTML content using the template
    html_content = render_email_template(name, title, total_questions, score)
    msg.attach(MIMEText(html_content, "html"))

    try:
        # Set up the server and send the email
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(from_email, password)
        text = msg.as_string()
        server.sendmail(from_email, to_email, text)
        server.quit()
        print("✅ Email sent successfully!")
        return "✅ Email sent successfully!"
    except Exception as e:
        print(f"❌ Error sending email: {e}")
        return f"❌ Error sending email: {e}"


# Example call to send the email
send_email_smtp("rasdsaa@sds.com", "John Doe", "Python Basics", 10, 8)
