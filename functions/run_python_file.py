import os
import subprocess
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Run Python File",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="file to run",
            ),
        },
    ),
)

def run_python_file(working_directory, file_path, args=[]):
    try:
        full_path = os.path.join(working_directory, file_path)
        abs_full_path = os.path.abspath(full_path)
        abs_working_directory = os.path.abspath(working_directory)
        if not abs_full_path.startswith(abs_working_directory):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.exists(abs_full_path):
            return f'Error: File "{file_path}" not found.'
        if not abs_full_path.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file.'
        
        if args:
            execute_command = f"uv run {abs_full_path} {args[0]}"
        else:
            execute_command = f"uv run {abs_full_path}"
        try:
            completed_process = subprocess.run(execute_command, timeout=30, capture_output=True, text=True, shell=True)
            output =""
            if completed_process.stdout or completed_process.stderr:
                output = f"STDOUT: \n{completed_process.stdout}\nSTDERR: \n{completed_process.stderr}"
            else:
                output = "No output produced"
            if completed_process.returncode != 0:
                output += f"\nProcess exited with code {completed_process.returncode}"

            return output
        except Exception as e:
            return f"Error: executing Python file: {e}"
        
    except Exception as e:
        return f'Error: An unexpected error occured while executing Python file: {e}'