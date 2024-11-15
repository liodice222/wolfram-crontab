import subprocess
import openai
import sys

def get_api_key():
    """Fetch the OpenAI API key from macOS Keychain."""
    try:
        # Using subprocess to execute the security command
        result = subprocess.run(
            ["security", "find-generic-password", "-a", "openai_api_key", "-s", "chatgpt_api_key"],
            capture_output=True,
            text=True
        )

        # If the command was successful
        if result.returncode == 0:
            api_key = result.stdout.strip()
            return api_key
        else:
            print("Failed to retrieve API key from Keychain.")
            sys.exit(1)

    except Exception as e:
        print(f"Error fetching API key: {e}")
        sys.exit(1)

def test_api_key(api_key):
    """Test the OpenAI API key by making a simple API request."""
    openai.api_key = api_key
    try:
        # Making a simple request to check API key validity
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Hello"}],
            max_tokens=5
        )
        # If we receive a response, the API key works
        if response:
            print("Connection Successful: Status Code 200")
    except openai.error.AuthenticationError:
        print("Authentication failed: Invalid API key.")
        sys.exit(1)
    except Exception as e:
        print(f"Error connecting to OpenAI API: {e}")
        sys.exit(1)

if __name__ == "__main__":
    api_key = get_api_key()
    test_api_key(api_key)
 




