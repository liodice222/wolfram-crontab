import openai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_api_key():
    """Fetch the OpenAI API key from the .env file."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("API key not found. Please check your .env file.")
        exit(1)
    return api_key

def test_api_key(api_key):
    """Test the OpenAI API key by making a simple API request."""
    openai.api_key = api_key
    try:
        # Make a simple request to verify the API key
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Hello, can you confirm my API key is working?"}],
            max_tokens=10
        )
        # Print the success message
        print("Connection Successful: Status Code 200")
        print("Response:", response['choices'][0]['message']['content'].strip())
    except openai.error.AuthenticationError:
        print("Authentication failed: Invalid API key.")
        exit(1)
    except openai.error.OpenAIError as e:
        print(f"OpenAI API Error: {e}")
        exit(1)
    except Exception as e:
        print(f"Unexpected Error: {e}")
        exit(1)

if __name__ == "__main__":
    api_key = get_api_key()
    test_api_key(api_key)
