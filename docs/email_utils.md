# About the Email Sending Feature

This feature allows users to send emails through a Gmail SMTP server. It is designed to be simple yet effective for sending notifications or updates. The feature ensures secure email transmission using environment variables to protect sensitive information like email credentials.

## Code Description

### Functions

#### `send_email(recipient_email, subject, body)`
This is the primary function for sending emails using Gmail's SMTP server. It takes three arguments:
- `recipient_email` (string): The email address of the recipient.
- `subject` (string): The subject of the email.
- `body` (string): The main content or body of the email.

**Functionality:**
1. **Input Validation:** Ensures that the `recipient_email`, `subject`, and `body` are not empty. If any of these fields are missing, it raises a `ValueError`.
2. **Message Composition:**
   - Constructs the email using the `MIMEMultipart` class.
   - Sets the sender (`EMAIL_ADDRESS`), recipient, and subject.
   - Attaches the body of the email as plain text.
3. **SMTP Connection:**
   - Connects to Gmail's SMTP server (`smtp.gmail.com`) using port `587`.
   - Secures the connection with `starttls()`.
   - Logs in to the sender's Gmail account using credentials stored in environment variables (`EMAIL_ADDRESS` and `EMAIL_PASSWORD`).
   - Sends the email and closes the connection.
4. **Error Handling:**
   - Catches exceptions during the email-sending process and prints the error message.
   - Rethrows the exception for further handling if needed.

**Usage:**
This function can be used to send emails programmatically by providing the recipient's email, subject, and body content. It ensures secure communication by using an app password for Gmail and a secure SMTP connection.

### Environment Variables

- `EMAIL_ADDRESS`: Your Gmail address, loaded securely from the `.env` file.
- `EMAIL_PASSWORD`: The Gmail app password, loaded securely from the `.env` file.

## Screenshot

Below is an example of the Email Sending Feature in action:

<img src="https://raw.githubusercontent.com/SoftwareEngg2024/SplitIT/feature/email-reminder/assets/screenshot.jpg" alt="Feature Screenshot" width="500"/>

### Example Code Usage

```python
from email_utils import send_email

# Example usage
try:
    send_email(
        recipient_email="recipient@example.com",
        subject="Hello from My Application",
        body="This is a test email sent using the Email Sending Feature."
    )
except Exception as e:
    print(f"Error: {e}")
