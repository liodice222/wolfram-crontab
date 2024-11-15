from dotenv import load_dotenv
import os

# Explicitly load the .env file in the current directory
load_dotenv(dotenv_path=os.path.join(os.getcwd(), '.env'))

# Fetch the OpenAI API key from the environment
api_key = os.getenv("OPENAI_API_KEY")
if api_key:
    print("API Key found:", api_key)
else:
    print("API key not found. Please check your .env file.")
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),  # This is the default and can be omitted
)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "Say this is a test",
        }
    ],
    model="gpt-4o",
)
