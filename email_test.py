import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
import os
import subprocess

#EMAIL CONFIG 
def get_password_from_keychain(account):
    try:
        return subprocess.run(
            ["security", "find-generic-password", "-a", account, "-w"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
    except subprocess.CalledProcessError:
        return None

SENDER_EMAIL = "iodice.pt@gmail.com"
SENDER_PASSWORD = get_password_from_keychain(SENDER_EMAIL)

#verify password is stored correctly 
#print(SENDER_PASSWORD)

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
RECIPIENT_EMAIL = "lea.iodice3@gmail.com"

def send_html_email():
    # Create the email
    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"Daily Update - {datetime.now().strftime('%Y-%m-%d')}"
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECIPIENT_EMAIL

    # HTML message content
    html_content = f"""
    <html>
        <body>
            <h2>Daily Problem!! Wee!</h2>
            <p>Hello! This is your daily problem for {datetime.now().strftime('%Y-%m-%d')}.</p>
            <p> <insert problem with api here> /p>
        </body>
    </html>
    """
    # Attach the HTML content
    msg.attach(MIMEText(html_content, "html"))

    # Send the email
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

if __name__ == "__main__":
    send_html_email()
