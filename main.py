import os
import sys
from google import genai
from dotenv import load_dotenv
from google.genai import types
from functions.call_function import call_function
from functions.write_file import schema_write_file
from functions.get_files_info import schema_get_files_info
from functions.run_python_file import schema_run_python_file
from functions.get_file_content import schema_get_file_content

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

available_functions = types.Tool(
    function_declarations=[
        schema_write_file,
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
    ]
)

def main():
    model_name = "gemini-2.0-flash-001"
    if len(sys.argv) == 1:
        print("Please provide a prompt!")
        sys.exit(1)
    else:
        prompt = sys.argv[1]

    messages = [{
        "role": "user",
        "parts": [
            {"text": prompt}
        ]
    }]

    response = client.models.generate_content(
        model=model_name,
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ),
    )

    if "--verbose" in sys.argv:
        print(f"User prompt: {prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    
    if hasattr(response, "function_calls") and response.function_calls:
        for function_call_part in response.function_calls:
            function_call_result = call_function(function_call_part, verbose="--verbose" in sys.argv)
    
            if not hasattr(function_call_result, 'parts') or not function_call_result.parts:
                raise Exception("Invalid function call result")
    
            if "--verbose" in sys.argv:
                print(f"-> {function_call_result.parts[0].function_response.response}")
    else:
        print(response.text)

if __name__ == "__main__":
    main()
