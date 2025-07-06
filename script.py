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
from db import db_manager

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
print(OPENAI_API_KEY)

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

# Initialize database with questions
def initialize_database():
    """Populate the database with questions from questions.py if empty"""
    db_manager.populate_from_questions(questions)

# Function to get a practice problem from database
def get_practice_problem():
    # Get a random unsent question from the database
    question_data = db_manager.get_random_unsent_question()
    
    if question_data is None:
        # If no unsent questions, reset all questions to unsent
        print("No unsent questions available. Resetting database...")
        db_manager.populate_from_questions(questions)
        question_data = db_manager.get_random_unsent_question()
    
    if question_data:
        # Format the question and answer choices
        problem = f"Subject: {question_data['subject'].title()}\n"
        problem += f"Question: {question_data['question']}\n"
        for option in question_data['options']:
            problem += f"{option}\n"
        
        # Include the explanation
        problem += f"Explanation: {question_data['explanation']}\n"
        problem += f"Resource: {question_data['resource']}\n"
        
        # Return both the formatted problem and the question ID for tracking
        return problem, question_data['id']
    
    return "No questions available.", None

# Function to send an HTML email with the problem
def send_html_email(problem, question_id=None):
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
            <p>{problem.replace(chr(10), '<br>')}</p>
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
        
        # Mark the question as sent and move it to sent database
        if question_id:
            db_manager.mark_question_as_sent(question_id)
        
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False

# Function to get database statistics
def print_database_stats():
    stats = db_manager.get_stats()
    print(f"Database Statistics:")
    print(f"  Unsent questions: {stats['unsent']}")
    print(f"  Sent questions: {stats['sent']}")
    print(f"  Total questions: {stats['total']}")

if __name__ == "__main__":
    # Initialize the database
    initialize_database()
    
    # Print current stats
    print_database_stats()
    
    # Get a practice problem and send it
    problem, question_id = get_practice_problem()
    
    if question_id:
        success = send_html_email(problem, question_id)
        if success:
            print("Question sent and marked as sent in database")
        else:
            print("Failed to send question - it will remain in unsent database")
    else:
        print("No question available to send")
    
    # Print updated stats
    print_database_stats()
