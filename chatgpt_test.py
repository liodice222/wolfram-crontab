import os
import openai # type: ignore
from dotenv import load_dotenv # type: ignore
from openai import OpenAI # type: ignore

# Load environment variables from .env file
load_dotenv()


def get_api_key():
    """Fetch the OpenAI API key from the .env file."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("API key not found. Please check your .env file.")
        exit(1)
    return api_key

client = OpenAI()

stream = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Say this is a test"}],
    stream=True,
)
for chunk in stream:
    if chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end="")




# if __name__ == "__main__":
#     api_key = get_api_key()
#     test_api_key(api_key)
