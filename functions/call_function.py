import os
from runpy import run_path
from google.genai import types
from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.run_python_file import run_python_file
from functions.write_file import write_file
from .config import WORKING_DIRECTORY


def call_function(function_call_part, verbose=False):
    verbose = verbose

    if verbose == True:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")
    
    match function_call_part.name:
        case get_files_info({}):
            print("Running get_files_info...")
            response = get_files_info(**function_call_part.args)
        case get_file_content({}):
            print("Running get_file_content...")
            response = get_file_content(**function_call_part.args)
        case write_file({}):
            print("Running write_file...")
            response = write_file(**fucntion_call_part.args) 
        case run_python_files({}):
            print("Running run_python...")
            response = run_python_file(**function_call_part.args)
        case _:
            return types.Content(
                role="tool",
                parts=[
                    types.Part.from_function_response(
                        name=function_call_part.name,
                        response={"error": f"Unknown function: {function_call_part.name}"},
                    )
                ],
)