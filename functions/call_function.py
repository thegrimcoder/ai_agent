import os
from runpy import run_path
from google.genai import types
from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.run_python_file import run_python_file
from functions.write_file import write_file
from .config import WORKING_DIRECTORY

functions = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "write_file": write_file,
    "run_python_file": run_python_file
}

def call_function(function_call_part, verbose=False):
    verbose = verbose

    #Example of calling a function from the functions dictionary
    #functions[function_call_part.name](**function_call_part.args)

    if function_call_part.name in functions:
        if verbose == True:
            print(f"Calling function: {function_call_part.name}({function_call_part.args})")
            result = functions[function_call_part.name](WORKING_DIRECTORY, **function_call_part.args)
            return types.Content(
                role="tool",
                parts=[
                    types.Part.from_function_response(
                        name=function_call_part.name,
                        response={"result": result},
                    )
                ],
            )
        else:
            print(f" - Calling function: {function_call_part.name}")
            result = functions[function_call_part.name](WORKING_DIRECTORY, **function_call_part.args)
            return types.Content(
                role="tool",
                parts=[
                    types.Part.from_function_response(
                        name=function_call_part.name,
                        response={"result": result},
                    )
                ],
            )
    else:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"error": f"Unknown function: {function_call_part.name}"},
                )
            ],
        )