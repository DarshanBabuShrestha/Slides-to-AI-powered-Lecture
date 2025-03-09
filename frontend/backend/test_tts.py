import os
from google.cloud import texttospeech

# Ensure Google Cloud credentials are set
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/dbs6231/Downloads/SWM-main/backend/tts-service-key.json"

def text_to_speech(text, output_filename="output.mp3"):
    """Synthesizes speech from the input string of text using Google's Studio Voices."""
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Use Studio-quality voice
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name="en-US-Studio-O",  # You can change this to another studio-quality voice
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.LINEAR16,  # Higher-quality audio format
        speaking_rate=1.0  # Adjust if you want a faster or slower speech
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # Save the audio file
    with open(output_filename, "wb") as out:
        out.write(response.audio_content)
    print(f'✅ Audio content written to file "{output_filename}" (Studio Voice Used!)')

# **Test the AI voice**
text_to_speech(
    "Hello, this is a test of the Google Voice synthesis system. "
    "The quick brown fox jumps over the lazy dog. "
    "How does the audio sound? Please let us know if further adjustments are needed. Thank you!",
    "output.mp3"
)
