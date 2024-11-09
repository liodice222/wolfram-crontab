#add shebang line
#!/usr/bin/env python3
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
import os
import subprocess
import requests # type: ignore
from questions import questions 
import random

#verify requests is working 
response = requests.get('https://api.github.com')
print(response.status_code)

# ChatGPT API Setup
def get_api_key_from_keychain(account):
    try:
        return subprocess.run(
            ["security", "find-generic-password", "-a", account, "-w"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
    except subprocess.CalledProcessError:
        return None

OPENAI_API_KEY = get_api_key_from_keychain("openai_api_key")
CHATGPT_API_URL = "https://api.openai.com/v1/chat/completions"

# Email Configuration
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
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
RECIPIENT_EMAIL = "lea.iodice3@gmail.com"

#Function to cycle through dictionary of problems in directory
def get_practice_problem():
    # Randomly select a subject (chemistry, biochemistry, or physics)
    subject = random.choice(list(questions.keys()))
    
    # Randomly select a question from the selected subject
    question_data = random.choice(questions[subject])
    
    # Format the question and answer choices
    problem = f"Question: {question_data['question']}\n"
    for option in question_data['options']:
        problem += f"{option}\n"
    
    # Include the answer and explanation
    #problem += f"\nAnswer: {question_data['answer']}\n"
    problem += f"Explanation: {question_data['explanation']}\n"
    
    # Return the formatted problem
    #print (problem)
    return problem
    
# Function to get a practice problem using ChatGPT, used later on 

# def get_practice_problem():
#     headers = {
#         "Authorization": f"Bearer {OPENAI_API_KEY}",
#         "Content-Type": "application/json"
#     }

#     prompt = (
#         "Generate a challenging but solvable algebra practice problem, "
#         "including instructions and the expected answer format."
#     )

#     data = {
#         "model": "gpt-4",
#         "messages": [{"role": "user", "content": prompt}],
#         "max_tokens": 150,
#         "temperature": 0.7
#     }

#     response = requests.post(CHATGPT_API_URL, headers=headers, json=data)
#     print(response)

#     if response.status_code == 200:
#         problem = response.json()['choices'][0]['message']['content']
#         return problem.strip()
#     else:
#         print(f"Error {response.status_code}: {response.text}")
#         return "Unable to generate a practice problem at this time."

# Function to send an HTML email with the problem
def send_html_email(problem):
    # Create the email
    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"Daily Problem - {datetime.now().strftime('%Y-%m-%d')}"
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECIPIENT_EMAIL

    # HTML message content
    html_content = f"""
    <html>
        <body>
            <h2>Daily Problem!! Wee!</h2>
            <p>Hello! This is your daily problem for {datetime.now().strftime('%Y-%m-%d')}.</p>
            <p><strong>Problem:</strong></p>
            <p>{problem}</p>
            <p>Good luck solving it!</p>
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
    problem = get_practice_problem()
    send_html_email(problem)
