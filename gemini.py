from dotenv import load_dotenv,find_dotenv
import os
import json
from google import genai
from google.genai import types
import requests

def process_document_with_gemini(docLink: str, prompt: str) -> str:
    """
    Process a document using Gemini API and return the response.

    Args:
        docLink (str): URL of the document to process
        prompt (str): The prompt to send to Gemini API

    Returns:
        str: The response from Gemini API
    """
    # Load environment variables
    load_dotenv(find_dotenv())
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

    # Initialize Gemini client
    client = genai.Client(api_key = GEMINI_API_KEY)

    # Download the file content
    response = requests.get(docLink)
    docData = response.content

    # Process with Gemini
    response = client.models.generate_content(
        model = "gemini-1.5-flash",
        config={"response_mime_type": "application/json"},
        contents = [
            types.Part.from_bytes(
                data = docData,
                mime_type = 'application/pdf',
            ),
            prompt
        ]
    )

    return response.text

# Example usage
# if __name__ == "__main__":
#     docLink = "https://discovery.ucl.ac.uk/id/eprint/10089234/1/343019_3_art_0_py4t4l_convrt.pdf"
#     prompt = "summarize this"
#     result = process_document_with_gemini(docLink, prompt)

#     try:
#         # Try to parse the response as JSON first
#         json_result = json.loads(result)
#         print('acha vala\n\n')
#         print(json.dumps(json_result, indent=4))
#     except json.JSONDecodeError:
#         # If it's not valid JSON, print the raw text
#         print(result)
