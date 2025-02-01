import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

test_text = "Binary numbers are the foundation of computer science. They only have two digits: 0 and 1."
try:
    response = openai.ChatCompletion.create(
        model="gpt-4",  # or "gpt-3.5-turbo"
        messages=[
            {"role": "system", "content": "You are an AI that converts slide text into a well-structured lecture transcript."},
            {"role": "user", "content": f"Convert the following slide text into a lecture transcript:\n\n{test_text}"}
        ]
    )
    transcript = response["choices"][0]["message"]["content"].strip()
    print("Transcript:", transcript)
except Exception as e:
    print("OpenAI API Error:", e)
