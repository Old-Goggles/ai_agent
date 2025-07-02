import os
import sys
from google import genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

def main():
    model_name = "gemini-2.0-flash-001"
    if len(sys.argv) == 1:
        print("Please provide a prompt!")
        sys.exit(1)
    else:
        prompt = sys.argv[1]

    response = client.models.generate_content(model=model_name, contents=prompt)

    if "--verbose" in sys.argv:
        print(f"User prompt: {prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    
    

    print(response.text)
    


if __name__ == "__main__":
    main()
