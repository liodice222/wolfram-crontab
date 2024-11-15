import openai
import keyring
import random
import json

# Constants
NUM_QUESTIONS = 10  
TEMPERATURE = 0.7
OUTPUT_FILE = 'questions.py'

# Subjects to generate questions for
subjects = [
    "Chemistry",
    "Biology",
    "Electrical Engineering",
    "Calculus/Algebra",
    "Human Physiology",
    "Physics"
]

# Function to get API key from keychain
def get_api_key():
    return keyring.get_password("openai", "api_key")

# Function to generate a question using OpenAI API
def generate_question(api_key, subject):
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
        question = response['choices'][0]['message']['content'].strip()
        return question
    except Exception as e:
        print(f"Error generating question for {subject}: {e}")
        return None

# Main function to generate questions and store them in a dictionary
def main():
    api_key = get_api_key()
    if not api_key:
        print("API key not found in the keychain. Please add it using keyring.")
        return
    
    openai.api_key = api_key
    questions_dict = {}

    for subject in subjects:
        questions = []
        for _ in range(NUM_QUESTIONS):
            question = generate_question(api_key, subject)
            if question:
                questions.append(question)
            else:
                print(f"Failed to generate a question for {subject}.")
        
        # Store generated questions in the dictionary
        questions_dict[subject] = questions

    # Save questions to a new Python file as a dictionary
    with open(OUTPUT_FILE, 'w') as file:
        file.write("questions = ")
        json.dump(questions_dict, file, indent=4)
    
    print(f"Questions generated and saved in {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
