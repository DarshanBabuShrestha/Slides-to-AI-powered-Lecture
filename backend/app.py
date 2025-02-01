from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import fitz  # PyMuPDF for PDF text extraction
from pptx import Presentation
import openai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set the OpenAI API Key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    print("Error: OPENAI_API_KEY is missing. Please set it in your .env file.")

# Initialize FastAPI app
app = FastAPI()

# Function to extract text from PDFs using PyMuPDF
def extract_text_from_pdf(file_path):
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text.strip()

# Function to extract text from PPTX files using python-pptx
def extract_text_from_pptx(file_path):
    prs = Presentation(file_path)
    text = ""
    for slide in prs.slides:
        for shape in slide.shapes:
            if hasattr(shape, "text"):
                text += shape.text + "\n"
    return text.strip()

# Function to generate an AI lecture transcript using OpenAI's ChatCompletion
def generate_lecture_transcript(extracted_text):
    if not extracted_text.strip():
        return "Error: No valid text found in the document."
    try:
        # Use gpt-3.5-turbo instead of gpt-4
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Switch to this model if you don't have GPT-4 access
            messages=[
                {
                    "role": "system",
                    "content": "You are an AI that converts slide text into a well-structured lecture transcript."
                },
                {
                    "role": "user",
                    "content": f"Convert the following slide text into a structured, well-explained lecture transcript:\n\n{extracted_text}"
                }
            ]
        )
        transcript = response["choices"][0]["message"]["content"].strip()
        print("DEBUG: Generated Transcript:")
        print(transcript)
        return transcript
    except openai.OpenAIError as e:
        return f"OpenAI API Error: {str(e)}"

# API endpoint to upload a file, extract text, and generate a lecture transcript
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        # Save the uploaded file to disk
        file_path = f"uploaded_{file.filename}"
        contents = await file.read()
        with open(file_path, "wb") as f:
            f.write(contents)

        # Extract text from the file based on its extension
        extracted_text = ""
        if file.filename.endswith('.pdf'):
            extracted_text = extract_text_from_pdf(file_path)
        elif file.filename.endswith('.pptx'):
            extracted_text = extract_text_from_pptx(file_path)
        else:
            return JSONResponse(content={"message": "Unsupported file type"}, status_code=400)

        # Print extracted text for debugging
        print("DEBUG: Extracted Text:")
        print(extracted_text)

        if not extracted_text.strip():
            return JSONResponse(content={"message": "No readable text found in the file"}, status_code=400)

        # Generate the lecture transcript using OpenAI
        lecture_transcript = generate_lecture_transcript(extracted_text)

        return JSONResponse(
            content={"message": "File uploaded and transcript generated", "transcript": lecture_transcript},
            status_code=200
        )
    except Exception as e:
        return JSONResponse(content={"message": str(e)}, status_code=400)
