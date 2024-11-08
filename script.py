import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Wolfram Alpha API Setup
API_KEY = 'your_wolfram_alpha_api_key'
QUERY_URL = 'http://api.wolframalpha.com/v2/query'

def get_practice_problem():
    params = {
        'input': 'algebra practice problem',  # specify your type of question here
        'appid': API_KEY,
        'output': 'json'
    }
    response = requests.get(QUERY_URL, params=params)
    data = response.json()
    # Parse the response data to extract the question text
    question = "Example practice question"  # Replace with parsed data
    return question

# Email Setup
def send_email(problem):
    sender_email = "your_email@example.com"
    receiver_email = "your_email@example.com"
    password = "your_email_password"  # Use app-specific passwords for Gmail or store securely

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = "Daily Practice Problem"

    message.attach(MIMEText(problem, "plain"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())

# Main function
def main():
    problem = get_practice_problem()
    send_email(problem)

if __name__ == "__main__":
    main()
