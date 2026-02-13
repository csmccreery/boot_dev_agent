import os
import argparse
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from google.genai import types
from system_prompt import agent_system_instruction
from functions.call_function import available_functions
from functions.run_python import run_python_file
from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.write_file import write_file

try:
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
except Exception as e:
    print(f"Error: Unable to load .env variables: {e}")

try:
    client = genai.Client(api_key=api_key)
except Exception as e:
    print(f"Error: Unable to assign client {e}")


def call_function(function_call, verbose=False):
    function_args = dict(function_call.args) if function_call.args else {}
    function_name = function_call.name or ""

    if verbose:
        print(f"Calling function: {function_name}({function_args})")
    else:
        print(f" - Calling function: {function_name}")

    function_map = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "write_file": write_file,
        "run_python_file": run_python_file,
    }

    if not function_name in function_map:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response = {"error": f"Unkown function: {function_name}"},
                )
            ]
        )

    function_args["working_directory"] = "./calculator"
    function_result = function_map[function_name](**function_args)

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )
    
def main():

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    function_responses = []

    if args.verbose:
        print("Starting agent call")
        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=messages,
            config=types.GenerateContentConfig(system_instruction=agent_system_instruction),
        )
        print("agent call complete: printing results")
    else:
        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=messages,
            config=types.GenerateContentConfig(
                system_instruction=agent_system_instruction,
                tools=[available_functions]
            ),
        )

    if response.usage_metadata is not None:
        prompt_tokens = response.usage_metadata.prompt_token_count
        response_tokens = response.usage_metadata.candidates_token_count
    else:
        raise RuntimeError("API Call failed, no usage metadata present")

    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Response tokens: {response_tokens}")

    if response.function_calls:
        for function_call in response.function_calls:
            result = call_function(function_call, args.verbose)

            if not result.parts:
                raise Exception("Error: Function response has no 'parts' field")
            else:
                result_parts = result.parts
            
            if not result_parts[0].function_response:
                raise Exception("Error: Function doesn't contain response")
            else:
                result_parts_response = result_parts[0].function_response

            if not result_parts_response.response:
                raise Exception("Error: Function response contains no content")

            function_responses.append(result_parts[0])

            if verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")
    else:
        print(response.text)

    print(function_responses)


if __name__ == "__main__":
    main()
