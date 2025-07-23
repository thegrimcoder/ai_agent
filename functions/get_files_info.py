import os
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

def get_files_info(working_directory, directory="."):
    try:
        full_path = os.path.join(working_directory, directory)
        abs_full_path = os.path.abspath(full_path)
        abs_working_directory = os.path.abspath(working_directory)
        if abs_full_path.startswith(abs_working_directory):
            if os.path.isdir(full_path):
                list = os.listdir(full_path)
                results = "Result for current directory:\n"
                for item in list:
                    temp_path = os.path.join(full_path, item)
                    results += f" - {item}: file_size={os.path.getsize(temp_path)} bytes, is_dir={os.path.isdir(temp_path)}\n"
                return results
            else:
                return f'Error: "{directory}" is not a directory'
        else:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    except Exception as e:
        return f'Error: An unexpected error occured: {e}'
    


