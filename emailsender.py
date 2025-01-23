import os
import time
import logging
from smtplib import SMTP_SSL
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("email_sender.log"), logging.StreamHandler()]
)

# Constants
SENDER_EMAIL = os.getenv('EMAIL')
SMTP_SERVER = "mail.privateemail.com"
SMTP_PORT = int(os.getenv('PORT', 465))  # Default to 465 if not provided
EMAIL_PASSWORD = os.getenv('PASSWORD')
CV_FILE_PATH = "./cv.pdf"
RECIPIENTS_FILE = 'hr.txt'
HTML_TEMPLATE_FILE = 'template1.html'


def load_file_content(filepath, mode='r', encoding='utf-8'):
    """Load content from a file."""
    try:
        with open(filepath, mode, encoding=encoding) as file:
            return file.read()
    except FileNotFoundError:
        logging.error(f"File not found: {filepath}")
        return None


def load_recipients(filepath):
    """Load recipient emails from a file."""
    recipients = load_file_content(filepath)
    if recipients:
        return [line.strip() for line in recipients.splitlines() if line.strip()]
    return []


def create_email_message(subject, sender, recipient, html_content, attachment_path=None):
    """Create an email message with optional attachment."""
    message = MIMEMultipart('alternative')
    message['Subject'] = subject
    message['From'] = sender
    message['To'] = recipient

    # Attach plain text and HTML versions
    message.attach(MIMEText(html_content, 'plain'))
    message.attach(MIMEText(html_content, 'html'))

    # Attach a file if provided (REMOVE THIS IF YOU DON'T WANT CV)
    if attachment_path:
        try:
            with open(attachment_path, 'rb') as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header(
                    'Content-Disposition',
                    f'attachment; filename={os.path.basename(attachment_path)}'
                )
                message.attach(part)
        except Exception as e:
            logging.error(f"Error attaching file {attachment_path}: {e}")
    return message


def send_email(smtp_server, smtp_port, sender, password, recipient, message):
    """Send an email using SMTP."""
    try:
        with SMTP_SSL(smtp_server, smtp_port) as smtp:
            smtp.login(sender, password)
            smtp.sendmail(sender, recipient, message.as_string())
        logging.info(f"Email sent to {recipient}")
    except Exception as e:
        logging.error(f"Error sending email to {recipient}: {e}")


def main():
    """Main function to send emails."""
    if not all([SENDER_EMAIL, SMTP_SERVER, SMTP_PORT, EMAIL_PASSWORD]):
        logging.error("Missing required environment variables.")
        return

    # Load recipients and email template
    recipients = load_recipients(RECIPIENTS_FILE)
    html_content = load_file_content(HTML_TEMPLATE_FILE)

    if not recipients:
        logging.error("No recipients found. Exiting.")
        return
    if not html_content:
        logging.error("HTML template could not be loaded. Exiting.")
        return

    # Send emails
    for recipient in recipients:
        message = create_email_message(
            subject="Staj Başvurusu - Yazılım Geliştirici",
            sender=SENDER_EMAIL,
            recipient=recipient,
            html_content=html_content,
            attachment_path=CV_FILE_PATH
        )
        send_email(SMTP_SERVER, SMTP_PORT, SENDER_EMAIL, EMAIL_PASSWORD, recipient, message)

        # Delay to avoid rate limiting
        time.sleep(5)


if __name__ == "__main__":
    main()
