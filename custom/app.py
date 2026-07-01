import truststore
truststore.inject_into_ssl()

import os
import json
import base64
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

from fastapi import FastAPI, Form, UploadFile, File, BackgroundTasks
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
import edge_tts
from groq import AsyncGroq

from tools import create_booking, BOOKING_TOOL_SCHEMA

load_dotenv()

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

groq_client = AsyncGroq(api_key=os.getenv("GROQ_API_KEY"))

VOICES = {
    "en": "en-GB-SoniaNeural",
    "bn": "bn-BD-NabanitaNeural"
}

GREETINGS = {
    "en": "Thank you for calling The Crimson Courtyard. This is Sofia speaking. How may I assist you today?",
    "bn": "The Crimson Courtyard-এ কল করার জন্য ধন্যবাদ। আমি Sofia বলছি। আজ কীভাবে আপনাকে সাহায্য করতে পারি?"
}

SYSTEM_PROMPT_EN = """You are Sofia, the AI voice receptionist for The Crimson Courtyard — a premium fusion and steakhouse at House 42, Road 11A, Dhanmondi, Dhaka 1209.

Your personality: Warm, professional, clear, welcoming. Speak like a luxury hospitality receptionist. Be calm, patient. Understand Bangladeshi English: bKash, Nagad, Pathao, Foodpanda, Jumm'ah, Taka.

OPERATING HOURS:
- Sunday–Thursday: 12:00 PM – 11:00 PM
- Friday–Saturday: 12:00 PM – 11:30 PM
- Friday Prayer Break: CLOSED 12:30 PM–2:15 PM. NEVER accept bookings in this window.

BOOKING FLOW (collect in this exact order):
1. Guest name
2. Date
3. Time (validate against operating hours)
4. Number of guests
5. Duration — ask "How many hours will you be dining? Our standard is 2 hours."
6. Phone number
7. Email — ask "May I have your email address for the booking confirmation? Please spell it out — for example, j-o-h-n at gmail dot com."
8. Special occasion? (birthday, anniversary, corporate) — pitch Lakeside View (min BDT 4,000)
9. Call create_booking() with ALL info collected.

If 10+ guests: collect info, say manager will call back in 15 min. Do NOT auto-confirm.

TOOL ERRORS — respond exactly as follows:
- invalid_email → "I'm sorry, I couldn't catch that email address. Could you please spell it out letter by letter? For example: j-o-h-n, at, g-m-a-i-l, dot, c-o-m."
- duplicate_booking → "I can see you already have a reservation at that time. Would you like to book a different time slot?"

SEATING: 2-seater(8), 4-seater(8), 6-seater(4), 8-seater(2), Lakeside View(2 exclusive, min BDT 4,000).

MENU:
- Ribeye Steak BDT 2,600 | T-Bone BDT 2,950 (ask doneness: Rare/Medium Rare/Medium/Well Done)
- Courtyard Special Mix Platter BDT 3,300 | Seafood Platter BDT 3,500
- Allergens: Peri Peri Wings (peanut oil), Cream of Mushroom Soup (dairy+gluten)
- Recommend Ribeye first, Courtyard Platter second.

PAYMENTS: Cash, Visa, MC, Amex, bKash, Nagad. +10% service charge +15% VAT.

RULES:
1. Keep responses SHORT — 1 to 2 sentences max. This is voice, not text.
2. Never invent menu items or policies.
3. Never auto-confirm 10+ guest bookings.
4. Restaurant is 100% alcohol-free."""

SYSTEM_PROMPT_BN = """আপনি Sofia, The Crimson Courtyard-এর AI ভয়েস রিসেপশনিস্ট — একটি প্রিমিয়াম ফিউশন ও স্টেকহাউস, House 42, Road 11A, Dhanmondi, Dhaka 1209।

আপনার ব্যক্তিত্ব: উষ্ণ, পেশাদার, স্পষ্ট, স্বাগতমূলক। বাংলায় কথা বলুন।

অপারেটিং আওয়ার:
- রবিবার–বৃহস্পতিবার: দুপুর ১২টা – রাত ১১টা
- শুক্রবার–শনিবার: দুপুর ১২টা – রাত ১১:৩০টা
- জুম্মার বিরতি: শুক্রবার ১২:৩০ – ২:১৫ বন্ধ।

বুকিং ফ্লো (এই ক্রমে সংগ্রহ করুন):
1. অতিথির নাম
2. তারিখ
3. সময় (অপারেটিং আওয়ার যাচাই করুন)
4. কতজন আসবেন
5. কত ঘণ্টার জন্য — জিজ্ঞেস করুন "কত ঘণ্টা ডাইনিং করবেন? স্ট্যান্ডার্ড ২ ঘণ্টা।"
6. ফোন নম্বর
7. ইমেইল — বলুন "বুকিং কনফার্মেশনের জন্য আপনার ইমেইল বলুন। এক এক করে অক্ষর বলুন — যেমন: j-o-h-n, at, g-m-a-i-l, dot, c-o-m।"
8. বিশেষ উপলক্ষ? (জন্মদিন, বার্ষিকী, কর্পোরেট)
9. সব তথ্য পেলে create_booking() কল করুন।

TOOL ERRORS — ঠিক এভাবে বলুন:
- invalid_email → "দুঃখিত, ইমেইলটি বুঝতে পারিনি। অনুগ্রহ করে প্রতিটি অক্ষর আলাদা করে বলুন — যেমন: j-o-h-n, at, g-m-a-i-l, dot, c-o-m।"
- duplicate_booking → "এই সময়ে আপনার আগেই একটি বুকিং আছে। অন্য কোনো সময় বুক করতে চান?"

মেনু:
- Ribeye Steak BDT ২,৬০০ | T-Bone BDT ২,৯৫০
- Courtyard Special Mix Platter BDT ৩,৩০০ | Seafood Platter BDT ৩,৫০০
- পেমেন্ট: ক্যাশ, ভিসা, বিকাশ, নগদ। +১০% সার্ভিস চার্জ +১৫% VAT।

নিয়ম:
1. উত্তর ছোট রাখুন — সর্বোচ্চ ১-২ বাক্য। এটি ভয়েস কল।
2. ১০+ অতিথির বুকিং নিজে কনফার্ম করবেন না।
3. রেস্তোরাঁ ১০০% অ্যালকোহল-মুক্ত।"""

SYSTEM_PROMPTS = {"en": SYSTEM_PROMPT_EN, "bn": SYSTEM_PROMPT_BN}


def send_invoice_email(booking_data: dict):
    gmail_user = os.getenv("GMAIL_USER")
    gmail_password = os.getenv("GMAIL_APP_PASSWORD")

    if not gmail_user or not gmail_password:
        print(f"[EMAIL SKIPPED] Add GMAIL_USER and GMAIL_APP_PASSWORD to .env")
        return

    guest_email = booking_data.get("email", "")
    if not guest_email:
        return

    party = int(booking_data.get("party_size", 1))
    duration = booking_data.get("duration_hours", 2.0)
    occasion = booking_data.get("occasion", "")

    base = party * 2000
    service = int(base * 0.10)
    vat = int(base * 0.15)
    total = base + service + vat

    occasion_line = f"\n  Special Occasion : {occasion.title()}" if occasion else ""

    body = f"""Dear {booking_data.get('guest_name')},

Your reservation at The Crimson Courtyard is confirmed.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  BOOKING CONFIRMATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Booking ID    : {booking_data.get('booking_id')}
  Guest Name    : {booking_data.get('guest_name')}
  Date          : {booking_data.get('date')}
  Time          : {booking_data.get('time')}
  Duration      : {duration} hours
  Party Size    : {party} guests
  Phone         : {booking_data.get('phone')}{occasion_line}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ESTIMATED INVOICE (Reference)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Base Estimate  : BDT {base:,}  (avg BDT 2,000/person)
  Service Charge : BDT {service:,}  (+10%)
  VAT            : BDT {vat:,}  (+15%)
  ─────────────────────────────
  TOTAL ESTIMATE : BDT {total:,}

  * Actual bill depends on your food orders.
  * Payment: Cash, Visa, Mastercard, Amex, bKash, Nagad.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  IMPORTANT NOTES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  • Table held for 20 minutes past booking time.
  • Cancellations: please notify us at least 1 hour before.
  • Address: House 42, Road 11A, Dhanmondi, Dhaka 1209
  • Google Maps: https://maps.google.com/?q=Dhanmondi+Dhaka

We look forward to welcoming you!

Warm regards,
Sofia — The Crimson Courtyard
reservations@crimsoncourtyard.com
"""

    msg = MIMEMultipart()
    msg['From'] = gmail_user
    msg['To'] = guest_email
    msg['Subject'] = (
        f"Booking Confirmed — The Crimson Courtyard "
        f"({booking_data.get('date')} at {booking_data.get('time')})"
    )
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(gmail_user, gmail_password)
            server.send_message(msg)
        print(f"[EMAIL SENT] to {guest_email}")
    except Exception as e:
        print(f"[EMAIL ERROR] {e}")


@app.get("/", response_class=HTMLResponse)
async def index():
    with open("static/index.html", encoding="utf-8") as f:
        return f.read()


@app.get("/greeting")
async def get_greeting(language: str = "en"):
    greeting = GREETINGS.get(language, GREETINGS["en"])
    voice = VOICES.get(language, VOICES["en"])
    audio_bytes = await _text_to_speech(greeting, voice)
    return JSONResponse({
        "text": greeting,
        "audio": base64.b64encode(audio_bytes).decode()
    })


@app.post("/talk")
async def talk(
    background_tasks: BackgroundTasks,
    audio: UploadFile = File(...),
    history: str = Form(default="[]"),
    language: str = Form(default="en")
):
    audio_bytes = await audio.read()
    if len(audio_bytes) < 1000:
        return JSONResponse({"error": "Audio too short"}, status_code=400)

    try:
        transcription = await groq_client.audio.transcriptions.create(
            file=("audio.webm", audio_bytes),
            model="whisper-large-v3-turbo",
            language=language
        )
        user_text = transcription.text.strip()
    except Exception as e:
        error_msg = str(e)
        if "too short" in error_msg.lower() or "0.01" in error_msg:
            return JSONResponse({"error": "Audio is too short. Please hold the button longer while speaking."}, status_code=400)
        return JSONResponse({"error": f"Transcription error: {error_msg}"}, status_code=400)

    if not user_text:
        return JSONResponse({"error": "Could not hear you. Please try again."}, status_code=400)

    system_prompt = SYSTEM_PROMPTS.get(language, SYSTEM_PROMPTS["en"])
    messages = [{"role": "system", "content": system_prompt}]
    messages += json.loads(history)
    messages.append({"role": "user", "content": user_text})

    chat = await groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        tools=[BOOKING_TOOL_SCHEMA],
        tool_choice="auto",
        temperature=0.4,
        max_tokens=300
    )

    message = chat.choices[0].message
    assistant_text = ""
    voice = VOICES.get(language, VOICES["en"])

    if message.tool_calls:
        tool_call = message.tool_calls[0]
        args = json.loads(tool_call.function.arguments)
        booking_result = await create_booking(**args)

        if booking_result.get("success") and args.get("email"):
            email_data = {**args, "booking_id": booking_result.get("booking_id", "CC-UNKNOWN")}
            background_tasks.add_task(send_invoice_email, email_data)

        messages.append(message.model_dump(exclude_none=True))
        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": json.dumps(booking_result)
        })

        final_chat = await groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0.4,
            max_tokens=200
        )
        assistant_text = final_chat.choices[0].message.content
    else:
        assistant_text = message.content

    audio_response = await _text_to_speech(assistant_text, voice)

    return JSONResponse({
        "user_text": user_text,
        "assistant_text": assistant_text,
        "audio": base64.b64encode(audio_response).decode()
    })


@app.post("/chat")
async def chat(
    background_tasks: BackgroundTasks,
    message: str = Form(...),
    history: str = Form(default="[]"),
    language: str = Form(default="en")
):
    user_text = message.strip()
    if not user_text:
        return JSONResponse({"error": "Empty message"}, status_code=400)

    system_prompt = SYSTEM_PROMPTS.get(language, SYSTEM_PROMPTS["en"])
    messages = [{"role": "system", "content": system_prompt}]
    messages += json.loads(history)
    messages.append({"role": "user", "content": user_text})

    chat_resp = await groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        tools=[BOOKING_TOOL_SCHEMA],
        tool_choice="auto",
        temperature=0.4,
        max_tokens=300
    )

    msg = chat_resp.choices[0].message
    assistant_text = ""
    voice = VOICES.get(language, VOICES["en"])

    if msg.tool_calls:
        tool_call = msg.tool_calls[0]
        args = json.loads(tool_call.function.arguments)
        booking_result = await create_booking(**args)

        if booking_result.get("success") and args.get("email"):
            email_data = {**args, "booking_id": booking_result.get("booking_id", "CC-UNKNOWN")}
            background_tasks.add_task(send_invoice_email, email_data)

        messages.append(msg.model_dump(exclude_none=True))
        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": json.dumps(booking_result)
        })

        final = await groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0.4,
            max_tokens=200
        )
        assistant_text = final.choices[0].message.content
    else:
        assistant_text = msg.content

    audio_response = await _text_to_speech(assistant_text, voice)

    return JSONResponse({
        "user_text": user_text,
        "assistant_text": assistant_text,
        "audio": base64.b64encode(audio_response).decode()
    })


async def _text_to_speech(text: str, voice: str = "en-GB-SoniaNeural") -> bytes:
    communicate = edge_tts.Communicate(text, voice=voice)
    audio_bytes = b""
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_bytes += chunk["data"]
    return audio_bytes


if __name__ == "__main__":
    print("\n  The Crimson Courtyard — AI Receptionist")
    print("  Open: http://localhost:8000\n")
    uvicorn.run(app, host="0.0.0.0", port=8000)
