import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import datetime
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def send_email_notification(user_email, admin_email, subject, body):
    """
    Sends an email notification to the admin with the specified subject and body.
    
    :param user_email: The sender's email (user email).
    :param admin_email: The recipient's email (admin email).
    :param subject: Subject of the email.
    :param body: Body of the email.
    """
    sender_email = os.getenv("SENDER_EMAIL")
    sender_password = os.getenv("EMAIL_PASSWORD")

    if not sender_email or not sender_password:
        logging.error("Email credentials are missing")
        return

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = admin_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP_SSL("smtp.mail.ru", 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, admin_email, message.as_string())
        logging.info("Email sent successfully")
    except Exception as e:
        logging.error(f"Error sending email: {e}")
