# AI Voice Receptionist - The Crimson Courtyard

This is a real-time AI Voice Receptionist built for restaurant table reservations. The AI agent, Sofia, interacts with callers in natural language, answers questions based on a knowledge base, and schedules bookings.

## Tech Stack
- **Backend**: Python, FastAPI
- **Frontend**: React (served via FastAPI)
- **AI/LLM**: Groq (Whisper for STT, Llama-3 for NLP)
- **TTS**: ElevenLabs
- **Automation**: n8n (Webhooks)

## Project Setup

1. **Clone the repository:**
   ```bash
   git clone <your-repository-url>
   cd clone_project/custom_stack
   ```

2. **Create a Virtual Environment:**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On Mac/Linux:
   source venv/bin/activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables:**
   Rename `.env.example` to `.env` and fill in your API keys (Groq, ElevenLabs, Daily.co).

5. **Run the Application:**
   ```bash
   python app.py
   ```
   Open `http://localhost:8000` in your browser.

## Features
- Hold-to-speak voice interface.
- Conversational AI with low latency using Groq.
- Custom knowledge base integration for restaurant details.
- Clean and modern "glassmorphism" UI.
