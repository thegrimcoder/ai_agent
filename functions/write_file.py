import os

def write_file(working_directory, file_path, content):
    try:
        full_path = os.path.join(working_directory, file_path)
        abs_full_path = os.path.abspath(full_path)
        abs_working_directory = os.path.abspath(working_directory)
        if not abs_full_path.startswith(abs_working_directory):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.exists(abs_full_path):
            dir = abs_full_path.rsplit('/', 1)[0]
            if not os.path.isdir(dir):
                os.makedirs(dir)
            with open(abs_full_path, "w") as f:
                f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        else:
            with open(abs_full_path, "w") as f:
                f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        
    except Exception as e:
        return f'Error: An unexpected error occured: {e}'