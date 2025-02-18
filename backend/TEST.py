from google.cloud import texttospeech

# Initialize TTS Client
client = texttospeech.TextToSpeechClient()

# Sample input
synthesis_input = texttospeech.SynthesisInput(text="Hello, this is a test.")

# Configure voice and audio format
voice = texttospeech.VoiceSelectionParams(
    language_code="en-US",
    name="en-US-Studio-O",
)

audio_config = texttospeech.AudioConfig(
    audio_encoding=texttospeech.AudioEncoding.MP3,
    speaking_rate=1.0
)

# Generate speech
try:
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )
    
    # Save the generated audio
    with open("test_output.mp3", "wb") as out:
        out.write(response.audio_content)

    print("✅ TTS Test Successful: Audio generated as 'test_output.mp3'.")

except Exception as e:
    print("❌ TTS Test Failed:", e)
