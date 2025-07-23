import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.config import SYSTEM_PROMPT
import sys

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
    ]
)

def main():
    model = "gemini-2.0-flash-001"
    if len(sys.argv) > 1:
        contents = sys.argv[1]
        messages = [types.Content(role="user", parts=[types.Part(text=contents)]),]
        response = client.models.generate_content(model=model, contents=messages, config=types.GenerateContentConfig(tools=[available_functions],system_instruction=SYSTEM_PROMPT))
        if response.function_calls:
            for functions_called in response.function_calls:
                print(f"Calling function: {functions_called.name}({functions_called.args})")
        else:
            print(response.text)
        if len(sys.argv) > 2:
            print(f"User prompt: {contents}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    else:
        print("No prompt was provided")
        exit(1)

if __name__ == "__main__":
    main()
