# AI Voice Receptionist — Project Roadmap

## Overview

Production-ready English-speaking AI voice receptionist for a Dhanmondy, Dhaka restaurant.
Built as a portfolio demo to win the Spike Media (Upwork row 3030) contract.

---

## Phase Breakdown

```
Phase 0 → Setup & Credentials      (Day 1–2)
Phase 1 → Core Voice Agent Build    (Day 3–5)
Phase 2 → Telephony Integration     (Day 6–8)
Phase 3 → Booking & Workflows       (Day 9–14)
Phase 4 → Knowledge Base / RAG      (Day 15–18)
Phase 5 → Edge Cases & Testing      (Day 19–22)
Phase 6 → Loom Demo & Handover      (Day 23–25)
```

---

## Phase Details

### Phase 0 — Setup & Credentials (Day 1–2)

- Create Retell AI account, configure project
- Create ElevenLabs account, select English voice
- Create Twilio account, buy a phone number
- Set up n8n (self-hosted or cloud)
- Connect all accounts together

### Phase 1 — Core Voice Agent Build (Day 3–5)

- Configure Retell AI agent with English language
- Attach ElevenLabs Flash voice to Retell
- Write base conversation script (greet → identify caller intent)
- Test basic call flow via Retell dashboard

### Phase 2 — Telephony Integration (Day 6–8)

- Twilio number BYOC into Retell AI
- Inbound call routing: Twilio → Retell → Agent
- Warm transfer setup: agent → human manager number
- After-hours message configuration

### Phase 3 — Booking & Workflows (Day 9–14)

- Google Calendar API: check available table slots
- Booking flow: ask date / time / party size → confirm slot
- n8n workflow: save booking to Google Sheets
- Twilio SMS: send confirmation to customer
- Gmail/SMTP: post-call summary email to restaurant owner

### Phase 4 — Knowledge Base / RAG (Day 15–18)

- Upload restaurant info to Retell Knowledge Base
  - Menu items & prices
  - Opening/closing hours
  - Location & parking
  - Popular dishes & allergen info
  - Reservation policies
- Test Q&A: "What's on the menu?", "Are you open on Friday?"

### Phase 5 — Edge Cases & Testing (Day 19–22)

- 20+ test calls covering different scenarios
- Handle: wrong input, unclear speech, repeated questions
- Handle: fully booked slots, outside business hours
- Fix all issues found during testing

### Phase 6 — Loom Demo & Handover (Day 23–25)

- Record 60-second Loom video showing live call
- Write onboarding documentation
- Package all configs, scripts, n8n workflows
- Final delivery

---

## Success Criteria

- [ ] Inbound call answered within 2 rings
- [ ] Booking completed end-to-end without human help
- [ ] SMS confirmation sent within 30 seconds of booking
- [ ] Post-call summary email delivered to owner
- [ ] Warm transfer works when agent can't help
- [ ] Loom demo recorded and shareable
