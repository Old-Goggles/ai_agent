from google.genai import types
from .write_file import write_file
from .get_files_info import get_files_info
from .run_python_file import run_python_file
from .get_file_content import get_file_content

FUNCTION_MAP = {
    "write_file": write_file,
    "get_files_info": get_files_info,
    "run_python_file": run_python_file,
    "get_file_content": get_file_content,
}

def call_function(function_call_part, verbose=False):
    if verbose == True:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")

    args_with_dir = function_call_part.args.copy()
    args_with_dir["working_directory"] = "./calculator"

    function_name = function_call_part.name
    if function_name not in FUNCTION_MAP:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
            )
        ],
    )

    actual_function = FUNCTION_MAP[function_name]
    function_result = actual_function(**args_with_dir)
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )
