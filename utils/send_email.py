from email.mime.text import MIMEText
import smtplib
from config import smtp_email, smtp_password, smtp_host, smtp_port


async def send_email(receiver_email, subject, body):
    context = {"subject": subject, "body": body}

    html_message = MIMEText(context["body"], "html")
    html_message["Subject"] = context["subject"]
    html_message["From"] = smtp_email
    html_message["To"] = receiver_email

    with smtplib.SMTP_SSL(smtp_host, smtp_port) as server:
        server.login(smtp_email, smtp_password)
        server.sendmail(smtp_email, receiver_email, html_message.as_string())
