# AI Voice Receptionist — Tools Required (FREE Stack)

## Goal

This project is for demonstration purposes and will not be delivered to a client.
Goal: Build the complete project to demonstrate capabilities.
**All tools = Free tier / Free trial — zero cost.**

---

## Current Account Status

| Tool | Status |
|------|--------|
| Vapi.ai | ✅ Created |
| ElevenLabs | ✅ Created |
| Groq | ✅ Created |
| Pinecone | ✅ Created |
| Twilio | ❌ Limit exhausted — replaced |
| n8n self-hosted | ⏳ Install needed |
| Google APIs | ⏳ Setup needed |

---

## Final Free Stack (Twilio Removed)

| Layer | Tool | Free Limit | Status |
|-------|------|-----------|--------|
| Voice Orchestration | **Vapi.ai** | $10 free credit (~100+ min) | ✅ Ready |
| TTS Voice | **ElevenLabs Free Tier** | 10,000 chars/month | ✅ Ready |
| LLM Brain | **Groq Free Tier** | 14,400 req/day | ✅ Ready |
| Knowledge Base | **Pinecone Free Tier** | 1 index, 100K vectors | ✅ Ready |
| Phone Number (calls) | **Vapi.ai Built-in Number** | Uses $10 credit (~$1.15/number) | ✅ No Twilio needed |
| SMS | **Vonage Free Trial** | €2 credit on signup | ⏳ Sign up needed |
| Workflow | **n8n Self-Hosted** | Unlimited free | ⏳ Install needed |
| Calendar | **Google Calendar API** | Free always | ⏳ Setup needed |
| Booking Storage | **Google Sheets** | Free always | ⏳ Setup needed |
| Email | **Gmail SMTP** | Free always | ⏳ Setup needed |
| Booking Storage | Supabase (paid) | **Google Sheets** | Free always | sheets.google.com |
| Email | SendGrid (paid) | **Gmail SMTP** | Free always | gmail.com |
| SMS | Twilio (paid) | **Twilio Trial Credit** | Included in $15.50 | — |

---

## Tool Details

### 1. Vapi.ai — Voice Agent Orchestration

```
Free tier: $10 credit on signup (no card needed initially)
What it does: Similar to Retell AI — call routing, LLM connection, TTS injection
Why Vapi over Retell: Retell's free tier is limited, Vapi's $10 credit is much more useful
Setup: vapi.ai → Sign up → Create Assistant → Connect ElevenLabs + Groq
```

### 2. ElevenLabs — TTS Voice

```
Free tier: 10,000 characters/month
What it does: Natural English voice (warm, professional receptionist tone)
Voice selection: "Rachel" or "Charlotte" — sophisticated female voice
Setup: elevenlabs.io → Free account → Copy API Key → Paste into Vapi
```

### 3. Vapi.ai Built-in Phone Number — Telephony (Without Twilio)

```
Cost: Deducted from $10 credit (~$1.15/month per number)
What it does: Buy phone number directly from Vapi dashboard
No Twilio required — Vapi provisions numbers natively
Setup: vapi.ai → Dashboard → Phone Numbers → Buy Number → Done
```

### 3b. Vonage Free Trial — SMS Only

```
Free credit: €2 on signup (no card required)
Covers: ~40–60 test SMS messages
What it does: Booking confirmation SMS → sent to customer's phone
Setup: vonage.com → Sign up → API key + secret → plug into n8n
Alternative: For the demo, SMS can be skipped; email-only is fine
```

### 4. n8n Self-Hosted — Workflow Automation

```
Cost: Completely free (open source)
Runs on: Your own laptop/PC (localhost:5678)
What it does: Booking → Google Sheets, SMS trigger, Email sender, after-hours lead capture
Setup: npm install n8n -g → n8n start → open localhost:5678
```

### 5. Groq — LLM (AI Brain)

```
Free tier: 14,400 requests/day (Llama 3.1 70B or Mixtral)
Speed: Fastest free LLM available (500+ tokens/sec)
Why Groq: Free, fast, good quality — perfect for voice agent (low latency critical)
Setup: console.groq.com → Free account → Copy API Key → Paste into Vapi
```

### 6. Pinecone Free Tier — Knowledge Base / RAG

```
Free tier: 1 serverless index, 100K vectors
What it does: Stores menu, FAQ, hours as embeddings — agent queries in real time
Alternative: Vapi has built-in KB too (simpler, use this first)
Setup: pinecone.io → Free account → Create index → Upload restaurant data
```

### 7. Google Services (Always Free)

```
Google Calendar API  → Booking slot management
Google Sheets        → Booking log, after-hours leads
Gmail SMTP           → Post-call summary email to owner
Setup: Google Cloud Console → Enable APIs → Service account key
```

---

## Account Status & Remaining Setup

```
✅ DONE — Already Created:
  → vapi.ai          ($10 free credit)
  → elevenlabs.io    (10K chars/month free)
  → console.groq.com (14,400 req/day free)
  → pinecone.io      (100K vectors free)

⏳ TODO — Still Needed:
  Step 1 → vonage.com        (5 min) — SMS only (€2 free credit)
  Step 2 → Google Cloud      (10 min) — Calendar + Sheets + Gmail APIs
  Step 3 → npm install n8n   (5 min) — workflow automation (localhost)
  Step 4 → Vapi Dashboard    (3 min) — Buy phone number from Vapi directly

Total remaining time: ~25 minutes
Total cost: $0
```

---

## What Each Free Limit Means in Practice

| Tool | Free Limit | Enough for Demo? |
|------|-----------|-----------------|
| Vapi.ai | $10 credit | ~100 minutes of calls ✅ |
| ElevenLabs | 10K chars/month | ~20–30 full conversations ✅ |
| Twilio Trial | $15.50 credit | 1 number + ~200 SMS + test calls ✅ |
| n8n self-hosted | Unlimited | Yes ✅ |
| Groq | 14,400 req/day | Unlimited for demo ✅ |
| Pinecone | 100K vectors | Restaurant KB is ~500 vectors ✅ |
| Google APIs | Free always | Yes ✅ |

**Total cost for this demo = $0**

---

## Demo Completion Checklist (Free Stack)

### Accounts

- [x] Vapi.ai account created
- [x] ElevenLabs account created
- [x] Groq account created
- [x] Pinecone account created
- [ ] Vonage account created (SMS)
- [ ] Google Cloud project + APIs enabled

### Configuration

- [ ] Vapi assistant created + ElevenLabs voice connected
- [ ] Groq LLM (Llama 3.1 70B) connected to Vapi
- [ ] Phone number bought from Vapi dashboard (~$1.15 from credit)
- [ ] n8n installed + running on localhost:5678

### Integrations

- [ ] Google Sheets: booking log + after-hours leads sheets created
- [ ] Google Calendar: test calendar connected to n8n
- [ ] Gmail SMTP: post-call summary email working
- [ ] Vonage SMS: booking confirmation SMS working
- [ ] Pinecone: Crimson Courtyard KB uploaded (menu, FAQ, hours)

### Testing & Delivery

- [ ] End-to-end test call completed (book a table scenario)
- [ ] All 10 call scenarios tested
- [ ] Loom demo video recorded (60 seconds)
