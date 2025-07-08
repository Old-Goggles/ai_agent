import os

def get_file_content(working_directory, file_path):
    full_path = os.path.join(working_directory, file_path)

    allowed = os.path.commonpath([os.path.abspath(working_directory), os.path.abspath(full_path)]) == os.path.abspath(working_directory)
    if not allowed:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if os.path.isfile(full_path) == False:
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    try:
        max_characters = 10000
        with open(full_path, "r") as f:
            file_content_string = f.read(max_characters)
        if len(file_content_string) >= max_characters:
            return f"{file_content_string}[...File '{file_path}' truncated at 10000 characters]"
        else:
            return file_content_string
        
    except Exception as e:
        return f"Error: {e}"
    