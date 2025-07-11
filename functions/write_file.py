import os
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes a file in the working directory, given its relative path",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The relative path to the file, from the working directory",
            ),
              "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file",
            ),
        },
    ),
)

def write_file(working_directory, file_path, content):
    full_path = os.path.join(working_directory, file_path)

    allowed = os.path.commonpath([os.path.abspath(working_directory), os.path.abspath(full_path)]) == os.path.abspath(working_directory)
    if not allowed:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    try:
        if os.path.exists(os.path.dirname(full_path)) == False:
            os.makedirs(os.path.dirname(full_path))

        with open(full_path, "w") as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error: {e}"