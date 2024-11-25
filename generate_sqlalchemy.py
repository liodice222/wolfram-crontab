import openai
import keyring
import random
import subprocess
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import SQLAlchemyError

# Constants
NUM_QUESTIONS = 10  # Number of questions per subject
TEMPERATURE = 0.7
DATABASE_URL = "sqlite:///questions.db"

# Subjects to generate questions for
subjects = [
    "Chemistry",
    "Biology",
    "Electrical Engineering",
    "Calculus/Algebra",
    "Human Physiology",
    "Physics",
    "Immunology"
]

# ORM Base
Base = declarative_base()

# Question Model
class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    subject = Column(String, nullable=False)
    question_text = Column(String, nullable=False)
    source = Column(String, nullable=False)
    sent = Column(Boolean, default=False)

# ChatGPT API Setup
def get_api_key(account):
    try:
        return subprocess.run(
            ["security", "find-generic-password", "-a", account, "-w"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
    except subprocess.CalledProcessError:
        return None

OPENAI_API_KEY = get_api_key("openai_api_key")


# Function to initialize the database
def init_db():
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()

# Function to generate a question using OpenAI API
def generate_question(openai_api_key, subject):
    prompt = (
        f"Create a challenging post-baccalaureate level question in {subject} "
        f"in 50 words, and include one reputable source for the question."
    )
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an assistant that creates study questions."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            temperature=TEMPERATURE
        )
        question_content = response['choices'][0]['message']['content'].strip()
        # Extract question text and source if provided
        if "Source:" in question_content:
            question_text, source = question_content.split("Source:", 1)
            return question_text.strip(), source.strip()
        return question_content, "Unknown"
    except Exception as e:
        print(f"Error generating question for {subject}: {e}")
        return None, None

# Function to save a question to the database
def save_question(session, subject, question_text, source):
    try:
        new_question = Question(
            subject=subject,
            question_text=question_text,
            source=source,
            sent=False
        )
        session.add(new_question)
        session.commit()
        print(f"Saved question for {subject}")
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Failed to save question: {e}")

# Main function to generate and store questions
def main():
    api_key = get_api_key("openai_api_key")
    if not api_key:
        print("API key not found in the keychain. Please add it using keyring.")
        return
    
    openai.api_key = api_key
    session = init_db()

    for subject in subjects:
        for _ in range(NUM_QUESTIONS):
            question_text, source = generate_question(api_key, subject)
            if question_text and source:
                save_question(session, subject, question_text, source)
            else:
                print(f"Failed to generate a question for {subject}.")

if __name__ == "__main__":
    main()
