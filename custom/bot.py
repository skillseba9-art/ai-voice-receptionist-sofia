import asyncio
import os
import json
from dotenv import load_dotenv
from openai import AsyncOpenAI

from pipecat.frames.frames import TTSSpeakFrame, EndFrame
from pipecat.pipeline.pipeline import Pipeline
from pipecat.pipeline.runner import PipelineRunner
from pipecat.pipeline.task import PipelineParams, PipelineTask
from pipecat.processors.aggregators.openai_llm_context import OpenAILLMContext
from pipecat.services.elevenlabs import ElevenLabsTTSService
from pipecat.services.openai import OpenAILLMService
from pipecat.transports.services.daily import DailyParams, DailyTransport

from tools import create_booking, BOOKING_TOOL_SCHEMA

load_dotenv()

SYSTEM_PROMPT = """You are Sofia, the AI voice receptionist for The Crimson Courtyard — a premium fusion and steakhouse at House 42, Road 11A, Dhanmondi, Dhaka 1209, near Dhanmondi Lake.

Your personality: Warm, professional, clear, and welcoming. Speak like a luxury hospitality receptionist. Be calm, patient, never rush. Understand Bangladeshi English: bKash, Nagad, Pathao, Foodpanda, Dhanmondi, Jumm'ah, Taka.

OPERATING HOURS:
- Sunday–Thursday: 12:00 PM – 11:00 PM
- Friday–Saturday: 12:00 PM – 11:30 PM
- Friday Prayer Break: CLOSED 12:30 PM–2:15 PM for Jumm'ah. NEVER accept bookings in this window.

BOOKING FLOW (follow this order):
1. Ask guest name
2. Ask preferred date
3. Ask preferred time — validate against hours above
4. Ask number of guests
5. If 10+ guests: say "Our manager will contact you within 15 minutes. May I take your name and phone number?" Do NOT auto-confirm.
6. If 1–9 guests: ask for phone number, then call create_booking()
7. Ask if special occasion — pitch Lakeside View tables if yes (min BDT 4,000 spend)

SEATING: 2-seater (8), 4-seater (8), 6-seater (4), 8-seater (2), Lakeside View (2 exclusive)

MENU HIGHLIGHTS:
- Ribeye Steak BDT 2,600 | T-Bone BDT 2,950 — always ask doneness: Rare, Medium Rare, Medium, Well Done
- Courtyard Special Mix Platter BDT 3,300 | Seafood Platter BDT 3,500
- Allergens: Peri Peri Wings (trace peanut oil), Cream of Mushroom Soup (dairy + gluten)
- Recommend Ribeye first, then Courtyard Platter when asked for suggestions

PAYMENTS: Cash, Visa, Mastercard, Amex, bKash, Nagad. +10% service charge +15% VAT on final bill.

RULES:
1. Responses MUST be short and conversational — voice call, not text chat. Max 2-3 sentences.
2. Never invent menu items, prices, or policies.
3. Never auto-confirm bookings for 10+ guests.
4. Always warn about allergens if caller mentions a relevant allergy.
5. Restaurant is 100% alcohol-free."""

GREETING = "Thank you for calling The Crimson Courtyard. This is Sofia speaking. How may I assist you today?"


async def run_bot(room_url: str, token: str):
    transport = DailyTransport(
        room_url,
        token,
        "Sofia",
        DailyParams(
            audio_out_enabled=True,
            audio_in_enabled=True,
            camera_out_enabled=False,
            transcription_enabled=True,
            vad_enabled=True,
        )
    )

    llm = OpenAILLMService(
        client=AsyncOpenAI(
            api_key=os.getenv("GROQ_API_KEY"),
            base_url="https://api.groq.com/openai/v1"
        ),
        model="llama-3.3-70b-versatile"
    )

    tts = ElevenLabsTTSService(
        api_key=os.getenv("ELEVENLABS_API_KEY"),
        voice_id=os.getenv("ELEVENLABS_VOICE_ID", "EXAVITQu4vr4xnSDxMaL"),
        model="eleven_flash_v2_5"
    )

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    context = OpenAILLMContext(messages, tools=[BOOKING_TOOL_SCHEMA])
    context_aggregator = llm.create_context_aggregator(context)

    async def handle_create_booking(function_name, tool_call_id, arguments, llm, context, result_callback):
        result = await create_booking(**arguments)
        await result_callback(json.dumps(result))

    llm.register_function("create_booking", handle_create_booking)

    pipeline = Pipeline([
        transport.input(),
        context_aggregator.user(),
        llm,
        tts,
        transport.output(),
        context_aggregator.assistant()
    ])

    task = PipelineTask(
        pipeline,
        PipelineParams(allow_interruptions=True)
    )

    @transport.event_handler("on_first_participant_joined")
    async def on_first_participant_joined(transport, participant):
        await task.queue_frame(TTSSpeakFrame(GREETING))

    @transport.event_handler("on_participant_left")
    async def on_participant_left(transport, participant, reason):
        await task.queue_frame(EndFrame())

    runner = PipelineRunner()
    await runner.run(task)
