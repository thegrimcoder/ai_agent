import os
from google.genai import types
from .config import WORKING_DIRECTORY

def call_function(function_call_part, verbose=False):
    verbose = verbose
    if verbose = True:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")
    
