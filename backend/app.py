from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
import fitz
from pptx import Presentation
import os
import requests
from google.cloud import texttospeech
from dotenv import load_dotenv
import shutil
import uuid
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import json
import uvicorn
app = FastAPI()
@app.get("/")
def read_root():
    return {"message": "Hello, Render!"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # This is `backend/`
JSON_FILE_PATH = os.path.join(BASE_DIR, "backend", "your_file.json")

# Load JSON data
def load_json():
    with open(JSON_FILE_PATH, "r", encoding="utf-8") as file:
        data = json.load(file)
    return data
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

EXTRACTED_TEXT = ""

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow frontend access
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = texttospeech.TextToSpeechClient()
load_dotenv()

def extract_text_from_pdf(file_path):
    global EXTRACTED_TEXT
    doc = fitz.open(file_path)
    text = "\n".join(page.get_text() for page in doc)
    EXTRACTED_TEXT = text.strip() if text.strip() else "Error: No readable text found in PDF."
    return EXTRACTED_TEXT

def extract_text_from_pptx(file_path):
    global EXTRACTED_TEXT
    prs = Presentation(file_path)
    text = "\n".join(shape.text for slide in prs.slides for shape in slide.shapes if hasattr(shape, "text"))
    EXTRACTED_TEXT = text.strip() if text.strip() else "Error: No readable text found in PPTX."
    return EXTRACTED_TEXT

def generate_lecture_transcript_gemini(extracted_text):
    if not extracted_text or "Error" in extracted_text:
        return "Error: No valid text found in the document."

    gemini_api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={os.getenv('GEMINI_API_KEY')}"

    payload = {
        "contents": [{
            "parts": [{
                "text": f"Convert the following slide text into a structured, well-explained lecture transcript. Ensure it is natural-sounding, deep, and engaging and make it below 4890 bytes:\n\n{extracted_text}"
            }]
        }]
    }

    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(gemini_api_url, json=payload, headers=headers, timeout=15)
        response_data = response.json()

        if response.status_code == 200 and "candidates" in response_data:
            return response_data["candidates"][0]["content"]["parts"][0]["text"].strip()
        else:
            return "Error generating transcript"

    except Exception as e:
        print(f"❌ Gemini API Error: {e}")
        return "Error generating transcript"

def text_to_speech(transcript):
    audio_filename = f"lecture_{uuid.uuid4().hex}.mp3"
    output_audio_path = os.path.join(UPLOAD_DIR, audio_filename)

    synthesis_input = texttospeech.SynthesisInput(text=transcript)
    voice = texttospeech.VoiceSelectionParams(language_code="en-US", name="en-US-Studio-O")
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3, speaking_rate=1.0)

    try:
        print("🚀 Generating AI Audio...")
        response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)

        with open(output_audio_path, "wb") as out:
            out.write(response.audio_content)

        return audio_filename  

    except Exception as e:
        print(f"❌ ERROR generating TTS audio: {e}")
        return None

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    global EXTRACTED_TEXT
    try:
        file_ext = file.filename.split('.')[-1].lower()
        file_path = os.path.join(UPLOAD_DIR, file.filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        if not os.path.exists(file_path):
            return JSONResponse(content={"message": "File save failed."}, status_code=500)

        print(f"✅ File successfully saved at: {file_path}")

        extracted_text = extract_text_from_pdf(file_path) if file_ext == 'pdf' else extract_text_from_pptx(file_path)

        ai_transcript = generate_lecture_transcript_gemini(extracted_text)
        if "Error" in ai_transcript:
            return JSONResponse(content={"message": "Transcript generation failed."}, status_code=400)

        audio_filename = text_to_speech(ai_transcript)
        if not audio_filename:
            return JSONResponse(content={"message": "Audio generation failed."}, status_code=500)

        file_url = f"http://127.0.0.1:8080/uploads/{file.filename}"
        audio_url = f"http://127.0.0.1:8080/uploads/{audio_filename}"

        print(f"✅ Returning JSON Response:\nFile URL: {file_url}\nAudio URL: {audio_url}")  

        return JSONResponse(content={"file_url": file_url, "audio_url": audio_url}, status_code=200)

    except Exception as e:
        print(f"❌ FastAPI Error: {e}")  
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.post("/chat")
async def chat(query: str = Form(...)):
    global EXTRACTED_TEXT

    if not EXTRACTED_TEXT:
        return JSONResponse(content={
            "response": "I don't have access to the course material. Please upload a PDF or PPTX first.",
            "audio_url": None
        })

    if not query.strip():
        return JSONResponse(content={"response": "Please ask a valid question.", "audio_url": None})

    gemini_api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={os.getenv('GEMINI_API_KEY')}"

    payload = {
        "contents": [{
            "parts": [{
                "text": f"""
                You are an AI assistant with access to the following document:

                ---
                {EXTRACTED_TEXT}
                ---

                Your primary task is to answer the question based on the provided document. If the document does not contain enough information, supplement the response with reliable external sources.


                **Question:** {query}
                """
                
            }]
        }]
    }

    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(gemini_api_url, json=payload, headers=headers, timeout=15)
        response_data = response.json()

        if response.status_code == 200 and "candidates" in response_data:
            response_text = response_data["candidates"][0]["content"]["parts"][0]["text"].strip()
        else:
            response_text = "I couldn't find a relevant answer in the course material."

    except Exception as e:
        print(f"❌ Error calling Gemini API: {e}")
        response_text = "Error generating AI response."

    try:
        synthesis_input = texttospeech.SynthesisInput(text=response_text)
        voice = texttospeech.VoiceSelectionParams(language_code="en-US", name="en-US-Studio-O")
        audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)

        tts_response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)

        audio_filename = f"chat_{uuid.uuid4().hex}.mp3"
        audio_path = os.path.join(UPLOAD_DIR, audio_filename)

        with open(audio_path, "wb") as out:
            out.write(tts_response.audio_content)

        audio_url = f"http://127.0.0.1:8080/uploads/{audio_filename}"

    except Exception as e:
        print(f"❌ Error generating AI audio: {e}")
        audio_url = None

    return JSONResponse(content={
        "response": response_text,
        "audio_url": audio_url
    })
