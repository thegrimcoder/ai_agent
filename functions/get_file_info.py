import os

def get_files_info(working_directory, directory="."):
    full_path = os.path.join(working_directory, directory)
    abs_full_path = os.path.abspath(full_path)
    abs_working_directory = os.path.abspath(working_directory)
    if abs_full_path.startswith(abs_working_directory):
        if os.path.isdir(full_path):
            list = os.listdir(full_path)
            ### Need to implement this
        else:
            return f'Error: "{directroy}" is not a directory'
    else:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'