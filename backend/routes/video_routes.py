from python_pptx import Presentation
from gtts import gTTS
from moviepy.editor import TextClip, AudioFileClip

def process_slide(slide_content):
    ppt = Presentation(slide_content)
    text = []
    for slide in ppt.slides:
        for shape in slide.shapes:
            if hasattr(shape, "text"):
                text.append(shape.text)
    return "\n".join(text)

def generate_video(text):
    # Convert text to speech (TTS)
    tts = gTTS(text)
    tts.save("audio.mp3")

    # Generate a text overlay video (for example purposes)
    text_clip = TextClip(text, fontsize=24, color='white', size=(800, 600))
    text_clip = text_clip.set_duration(5)  # 5 seconds duration

    # Add TTS audio to the video
    audio_clip = AudioFileClip("audio.mp3")
    video = text_clip.set_audio(audio_clip)

    # Save final video
    video.write_videofile("output_video.mp4")
    return "output_video.mp4"
