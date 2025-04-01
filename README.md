# 📚 AI-Powered Slide-to-Lecture Audio System

Transform boring PowerPoint/PDF slides into engaging AI-generated lecture videos with synchronized voiceover and an interactive AI chatbot professor.

---

## 🚀 Features

- 🧠 **AI Lecture Generation**: Converts slide content into natural-sounding voice lectures using Google TTS.
- 🗂️ **PDF/PPTX Upload Support**: Upload slides in either format and process them in seconds.
- 🎙️ **Synchronized Audio Playback**: Each slide is paired with generated audio for a full lecture experience.
- 💬 **AI Chatbot Professor**: Ask questions and get instant responses using context from your slides.
- ⚙️ **Adjustable Playback Settings**: Control playback speed, volume, and audio settings through a smooth UI.
- 🌐 **Full-Stack App**: FastAPI backend + React frontend + Dockerized deployment.
## 💡 How It Works
1. Upload a PowerPoint or PDF slide deck
2. Backend extracts and summarizes slide text
3. Text is converted to audio using Google TTS
4. React frontend syncs audio with slide visuals
5. AI chatbot answers questions about the content

---

## 🏁 Getting Started
```bash
# Clone repo
git clone https://github.com/yourusername/ai-slide-to-video-project.git
cd ai-slide-to-video-project

# Start backend (in /backend)
uvicorn app:app --reload

# Start frontend (in /frontend)
npm install
npm run dev
```
