"""Service to send emails"""
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from core.config import Config


smtp_host = Config.SMTP_HOST
smtp_mail = Config.SMTP_MAIL
smtp_password = Config.SMTP_PASSWORD


def load_template(path: str):
    """Function to load email template"""
    with open(path, 'r') as file:
        template = file.read()
    return template


def send_verification(to_email: str, verification_code: str):
    """Function to send verification email"""
    """Verification sent process started"""
    template_path = 'static/templates/email_verification.html'
    template = load_template(template_path)

    content = template.replace('{{ verification_code }}', str(verification_code))

    msg = MIMEMultipart('alternative')
    msg['From'] = smtp_mail
    msg['To'] = to_email
    msg['Subject'] = 'Your Verification Code'

    msg.attach(MIMEText(content, 'html'))

    server = smtplib.SMTP(smtp_host, 587)
    try:
        server.starttls()
        server.login(smtp_mail, smtp_password)
        server.send_message(msg)
    except Exception as e:
        print(f"Failed to send email: {e}")
    finally:
        server.quit()
