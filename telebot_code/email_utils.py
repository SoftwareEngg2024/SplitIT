import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")  # Your Gmail address
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")  # App password

def send_email(recipient_email, subject, body):
    """Send an email using Gmail SMTP."""
    if not recipient_email or not subject or not body:
        raise ValueError("Recipient, Subject, and Body are required fields.")
    
    try:
        # Create the email content
        message = MIMEMultipart()
        message["From"] = EMAIL_ADDRESS
        message["To"] = recipient_email
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain"))

        # Connect to Gmail's SMTP server
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()  # Secure connection
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, recipient_email, message.as_string())

        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")
        raise e

