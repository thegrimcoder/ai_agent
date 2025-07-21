import os
from .config import CHARACTER_LIMIT

def get_file_content(working_directory, file_path):
    try:
        full_path = os.path.join(working_directory, file_path)
        abs_full_path = os.path.abspath(full_path)
        abs_working_directory = os.path.abspath(working_directory)
        if not abs_full_path.startswith(abs_working_directory):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(abs_full_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        with open(abs_full_path, "r") as f:
            file_content_string = f.read()
            if len(file_content_string) > 10000:
                #print(file_content_string)
                return file_content_string[:CHARACTER_LIMIT] + f'[...File "{file_path}" truncated at 10000 characters]'
            else:
                return file_content_string
        
    except Exception as e:
        return f'Error: An unexpected error occured: {e}'