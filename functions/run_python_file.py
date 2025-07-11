import os
import subprocess
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file in the working directory, given its relative path",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The relative path to the file, from the working directory",
            ),
        },
    ),
)

def run_python_file(working_directory, file_path):
    full_path = os.path.join(working_directory, file_path)

    allowed = os.path.commonpath([os.path.abspath(working_directory), os.path.abspath(full_path)]) == os.path.abspath(working_directory)
    if not allowed:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if os.path.isfile(full_path) == False:
        return f'Error: File "{file_path}" not found.'
    
    if os.path.abspath(full_path).endswith(".py") == False:
        return f'Error: "{file_path}" is not a Python file.'
    
    try:
        result = subprocess.run(
            ["python", file_path],
            cwd=working_directory,
            capture_output=True,
            timeout=30,
            text=True
    )
        
        output_lines = []

        if result.stdout:
            output_lines.append("STDOUT:" + result.stdout)
        if result.stderr:
            output_lines.append("STDERR:" + result.stderr)
        if result.returncode != 0:
            output_lines.append(f"Process exited with code {result.returncode}")

        if not output_lines:
            return "No output produced."
        else:
            return "\n".join(output_lines)

    except Exception as e:
         return f"Error: executing Python file: {e}"
        