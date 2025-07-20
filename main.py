import os
from dotenv import load_dotenv
from google import genai
import sys

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

def main():
    model = "gemini-2.0-flash-001"
    if len(sys.argv) > 1:
        contents = sys.argv[1]
        response = client.models.generate_content(model=model, contents=contents)
        print(response.text)
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    else:
        print("No prompt was provided")
        exit(1)

if __name__ == "__main__":
    main()
