# Pipecat Custom Stack — Setup Guide

# The Crimson Courtyard AI Voice Receptionist

**Stack:** Pipecat + Daily.co + Groq + ElevenLabs + n8n
**Total Cost:** $0
**Time to first call:** ~45 minutes

---

## Architecture

```
[Your Browser]
     |
     | WebRTC (Daily.co — free 10K min/month)
     v
[Pipecat Bot — Python, runs on your PC]
     |
     |── Transcription ──► Daily.co built-in STT (Deepgram, free within Daily)
     |── LLM ────────────► Groq Llama 3.3-70B (free tier)
     |── Voice ──────────► ElevenLabs Rachel (free 10K chars/month)
     |── Booking ────────► n8n webhook ──► Google Sheets
```

---

## Step 1 — Account Setup (10 min)

### Daily.co (free — 10,000 minutes/month)

1. Go to daily.co → Sign Up
2. Dashboard → Developers → API Keys → Copy key
3. Save as `DAILY_API_KEY` in `.env`

### Groq (free LLM + STT)

Already set up. Get key from console.groq.com → API Keys

### ElevenLabs (free 10K chars/month)

Already set up. Get key from elevenlabs.io → Profile → API Key

---

## Step 2 — Python Setup (10 min)

### Check Python version (need 3.10+)

```powershell
python --version
```

### Navigate to project folder

```powershell
cd "C:\Users\SkillSeba PC-2\Project\Job_Hunter\Upwork_Jobs_Tracker\ai_voice_receptionist_restaurant\custom_stack"
```

### Create virtual environment

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### Install dependencies

```powershell
pip install -r requirements.txt
```

> Note: `pipecat-ai[silero]` downloads a ~30MB VAD model on first run. Normal.

---

## Step 3 — Configure Environment (5 min)

```powershell
copy .env.example .env
```

Open `.env` and fill in your keys:

```
DAILY_API_KEY=your_daily_api_key_here
GROQ_API_KEY=your_groq_api_key_here
ELEVENLABS_API_KEY=your_elevenlabs_api_key_here
ELEVENLABS_VOICE_ID=EXAVITQu4vr4xnSDxMaL
N8N_WEBHOOK_URL=http://localhost:5678/webhook/booking
```

Rachel voice ID is already set — no change needed.

---

## Step 4 — Run the Bot (2 min)

```powershell
python server.py
```

You should see:

```
 The Crimson Courtyard Voice Bot
 Open: http://localhost:8000
```

Open your browser → go to `http://localhost:8000`
→ Click **"Start Voice Call"**
→ Allow microphone access
→ Sofia will greet you within 3–5 seconds

---

## Step 5 — Test the Call

Try these test scenarios:

### Basic booking
>
> "I'd like to make a reservation for 2 people this Saturday at 7 PM"

### Allergen test
>
> "Do you have anything for someone with a peanut allergy?"

### Menu recommendation
>
> "What do you recommend?"

### Special occasion
>
> "It's my anniversary — do you have anything special?"

### Large group (should NOT auto-confirm)
>
> "I need a table for 12 people"

### Friday prayer block
>
> "Can I book a table for Friday at 1 PM?"

---

## Step 6 — Record Demo for Portfolio (OBS Screen Record)

1. Download OBS Studio (free) — obsproject.com
2. Add sources: Display Capture + Audio Output Capture
3. Click Start Recording
4. Run test scenarios above
5. Stop recording → upload to Loom → add to Upwork portfolio

---

## Step 7 — n8n Booking Integration (Optional, Phase 2)

### Install n8n

```powershell
npm install -g n8n
n8n start
```

Open <http://localhost:5678> → Create workflow:

```
Webhook (POST /booking)
    → Google Sheets (Append Row)
    → Gmail (Send confirmation email)
```

### n8n Workflow Fields to map

| n8n Field | From Bot |
|-----------|----------|
| Guest Name | guest_name |
| Phone | phone |
| Date | date |
| Time | time |
| Party Size | party_size |
| Occasion | occasion |
| Timestamp | timestamp |

> Without n8n running, bookings are just printed to console. Bot still works fully for demo purposes.

---

## Troubleshooting

### "ModuleNotFoundError: pipecat"

```powershell
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### "Silero VAD download failed"

First run downloads ~30MB model. Check internet and retry.

### Microphone not working in browser

- Use Chrome or Edge (not Firefox — Daily.co works best in Chromium)
- Check Windows microphone permissions: Settings → Privacy → Microphone → Allow

### Bot speaks but doesn't hear you

- Check browser microphone permissions (lock icon in address bar)
- Try clicking the microphone icon inside the Daily.co room UI

### ElevenLabs quota exceeded

- Free tier: 10,000 chars/month
- Switch voice model to `eleven_turbo_v2` (uses fewer chars per sentence)

---

## File Structure

```
custom_stack/
├── bot.py              ← Pipecat voice pipeline (Sofia's brain)
├── server.py           ← FastAPI web server
├── tools.py            ← Booking tool (calls n8n webhook)
├── requirements.txt
├── .env                ← Your API keys (never commit this)
├── .env.example        ← Template
└── static/
    └── index.html      ← Browser UI (Crimson Courtyard branded)
```

---

## Cost Summary

| Service | Free Tier | Usage |
|---------|-----------|-------|
| Daily.co | 10,000 min/month | ~5 hours testing |
| Groq LLM | Unlimited (rate limited) | Free |
| Groq STT | 28,800 audio-sec/day | Free |
| ElevenLabs | 10,000 chars/month | ~100 test calls |
| n8n | Self-hosted | Free |

**Total: $0**
