import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.write_file import schema_write_file
from functions.run_python_file import schema_run_python_file
from functions.config import SYSTEM_PROMPT
from functions.call_function import call_function
import sys

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_run_python_file
    ]
)

def main():
    model = "gemini-2.0-flash-001"
    if len(sys.argv) > 1:
        contents = sys.argv[1]
        messages = [types.Content(role="user", parts=[types.Part(text=contents)]),]
        i = 0
        while i <= 19:
            try:
                response = client.models.generate_content(model=model, contents=messages, config=types.GenerateContentConfig(tools=[available_functions],system_instruction=SYSTEM_PROMPT))
                
                if not response.function_calls and response.text:
                    print(response.text)
                    break

                if response.candidates:
                    for candidate in response.candidates:
                        messages.append(candidate.content)
                
                if response.function_calls and len(sys.argv) > 2:
                    for functions_called in response.function_calls:
                        function_response = call_function(functions_called, True)
                        try:
                            if function_response.parts[0].function_response.response:
                                msg = str(function_response.parts[0].function_response.response[next(iter(function_response.parts[0].function_response.response))])
                                #print(f"-> {msg}")
                                messages.append(msg)
                            else:
                                raise Exception("No response received")
                        except Exception as e:
                            print(f"An unexpected error occurred: {e}")
                else:
                    for functions_called in response.function_calls:
                        function_response = call_function(functions_called, False)
                        try:
                            if function_response.parts[0].function_response.response:
                                msg = str(function_response.parts[0].function_response.response[next(iter(function_response.parts[0].function_response.response))])
                                #print(f"-> {msg}")
                                messages.append(msg)
                            else:
                                raise Exception("No response received")
                        except Exception as e:
                            print(f"An unexpected error occurred: {e}")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")

            i += 1
    else:
        print("No prompt was provided")
        exit(1)

if __name__ == "__main__":
    main()
