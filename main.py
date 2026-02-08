import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from system_prompt import agent_system_instruction

try:
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    print("Success: Loaded API key to environment variable")
except Exception as e:
    print(f"Error: Unable to load .env variables: {e}")

try:
    print(api_key)
    client = genai.Client(api_key=api_key)
except Exception as e:
    print(f"Error: Unable to assign client {e}")
    
def main():

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    print("Starting agent call")
    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=messages
    )
    print("agent call complete: printing results")

    if response.usage_metadata is not None:
        prompt_tokens = response.usage_metadata.prompt_token_count
        response_tokens = response.usage_metadata.candidates_token_count
    else:
        raise RuntimeError("API Call failed, no usage metadata present")

    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Response tokens: {response_tokens}")

    print(response.text)


if __name__ == "__main__":
    main()
