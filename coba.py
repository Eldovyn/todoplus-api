import smtplib
from email.mime.text import MIMEText

sender_email = "ditttt.tiktok@gmail.com"
sender_password = "aubt abtg tftq ptpk"
receiver_email = "jasere1761@merotx.com"

context = {"subject": "subject", "body": "body"}

html_message = MIMEText(context["body"], "html")
html_message["Subject"] = context["subject"]
html_message["From"] = sender_email
html_message["To"] = receiver_email

with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
    server.login(sender_email, sender_password)
    server.sendmail(sender_email, receiver_email, html_message.as_string())
