# Vapi.ai Assistant Setup Guide

# The Crimson Courtyard — AI Voice Receptionist

---

## Step 1 — Create Assistant in Vapi Dashboard

```
1. vapi.ai → Login → Dashboard
2. Left sidebar → "Assistants" → "+ Create Assistant"
3. Template: Select "Blank Assistant"
4. Name: "Crimson Courtyard Receptionist"
5. Save
```

---

## Step 2 — LLM Configuration (Groq)

```
Assistant Settings → Model tab:

Provider     : Groq
Model        : llama-3.3-70b-versatile   (or mixtral-8x7b-32768)
Temperature  : 0.4   (consistent, not too creative)
Max Tokens   : 300   (shorter responses are better for voice)
```

**Where to find Groq API Key:**

```
console.groq.com → API Keys → Create API Key → Copy
Vapi → Assistant → Model → Groq → Paste API Key
```

---

## Step 3 — Voice Configuration (ElevenLabs)

```
Assistant Settings → Voice tab:

Provider : ElevenLabs
Voice    : "Rachel" (warm, professional, clear)
          or "Charlotte" (sophisticated female)
Model    : eleven_flash_v2_5   (fastest, lowest latency)
Stability       : 0.5
Similarity Boost: 0.75
```

**Where to find ElevenLabs API Key:**

```
elevenlabs.io → Profile → API Key → Copy
Vapi → Assistant → Voice → ElevenLabs → Paste API Key
```

---

## Step 4 — First Message (Greeting)

Paste into Assistant Settings → "First Message" field:

```
Thank you for calling The Crimson Courtyard, Dhanmondi's premier fine dining destination. I'm your AI receptionist. How may I assist you today? I can help you with table reservations, menu information, or answer any questions about our restaurant.
```

---

## Step 5 — System Prompt

Paste the contents of **vapi_system_prompt.md** into Assistant Settings → "System Prompt" field.

---

## Step 6 — Call Settings

```
Assistant Settings → Call tab:

Max Duration        : 600 seconds (10 min)
Silence Timeout     : 30 seconds
Background Sound    : "office" (subtle ambiance)
End Call Phrases    : ["goodbye", "thank you bye", "that's all", "hang up"]
```

---

## Step 7 — Phone Number (Vapi Built-in)

```
Left sidebar → "Phone Numbers" → "+ Add Phone Number"
Provider : Vapi (recommended) or Twilio
Country  : United States (+1) — Use US number for demo purposes
           (This will work for the demo)
→ Buy Number (deducts ~$1.15 from credit)
→ Assign to: "Crimson Courtyard Receptionist"
```

---

## Step 8 — Test Call

```
Assistant Dashboard → "Test" button (web call, no physical phone needed)
Or: If a phone number is purchased, call that number directly

Test scenarios:
1. "I'd like to book a table for 2 on Saturday at 7pm"
2. "What's on your menu?"
3. "Are you open on Fridays at 1pm?"  ← Friday prayer break test
4. "Do you have vegetarian options?"
5. "I need to speak to the manager"   ← warm transfer test
```

---

## Step 9 — n8n Webhook Connect (Later)

```
Assistant Settings → Functions tab → "+ Add Function"
Name: "create_booking"
Description: "Save a table booking to the system"
→ URL: [n8n webhook URL — will be added later]
```

---

## Checklist

- [ ] Assistant created in Vapi dashboard
- [ ] Groq API key connected (llama-3.3-70b)
- [ ] ElevenLabs voice connected (Rachel)
- [ ] First message set
- [ ] System prompt pasted
- [ ] Call settings configured
- [ ] Phone number purchased + assigned
- [ ] First test call completed
