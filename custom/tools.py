import os
import json
import re
import httpx
from datetime import datetime

# in-memory duplicate guard: (phone, date, time) → booking_id
_booked_slots: dict = {}


def _is_valid_email(email: str) -> bool:
    return bool(re.match(r'^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$', email.strip()))


async def create_booking(
    guest_name: str,
    phone: str,
    email: str,
    date: str,
    time: str,
    party_size: int,
    duration_hours: float = 2.0,
    occasion: str = ""
) -> dict:

    if not _is_valid_email(email):
        return {
            "success": False,
            "error": "invalid_email",
            "message": "Email address is invalid. Ask the guest to spell it out letter by letter."
        }

    slot_key = (phone.strip(), date.strip(), time.strip())
    if slot_key in _booked_slots:
        return {
            "success": False,
            "error": "duplicate_booking",
            "message": f"A booking already exists for this phone number at {date} {time}. Existing ID: {_booked_slots[slot_key]}"
        }

    base = party_size * 2000
    service = int(base * 0.10)
    vat = int(base * 0.15)
    estimated_amount_bdt = base + service + vat

    payload = {
        "guest_name": guest_name,
        "phone": phone,
        "email": email,
        "date": date,
        "time": time,
        "party_size": party_size,
        "duration_hours": duration_hours,
        "occasion": occasion,
        "estimated_amount_bdt": estimated_amount_bdt,
        "timestamp": datetime.now().isoformat(),
        "source": "voice_bot"
    }

    webhook_url = os.getenv("N8N_WEBHOOK_URL", "http://localhost:5678/webhook/booking")
    booking_id = f"CC-{datetime.now().strftime('%Y%m%d%H%M%S')}"

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(webhook_url, json=payload)
            if response.status_code == 200:
                _booked_slots[slot_key] = booking_id
                return {
                    "success": True,
                    "booking_id": booking_id,
                    "estimated_amount_bdt": estimated_amount_bdt
                }
            else:
                return {"success": False, "message": "Booking system temporarily unavailable"}
    except httpx.ConnectError:
        print(f"[BOOKING LOG] {json.dumps(payload)}")
        booking_id = f"CC-LOCAL-{datetime.now().strftime('%H%M%S')}"
        _booked_slots[slot_key] = booking_id
        return {
            "success": True,
            "booking_id": booking_id,
            "estimated_amount_bdt": estimated_amount_bdt
        }


BOOKING_TOOL_SCHEMA = {
    "type": "function",
    "function": {
        "name": "create_booking",
        "description": (
            "Create a table reservation at The Crimson Courtyard. "
            "Call ONLY after collecting: guest name, phone, email, date, time, party size, and duration."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "guest_name": {
                    "type": "string",
                    "description": "Full name of the guest making the reservation"
                },
                "phone": {
                    "type": "string",
                    "description": "Guest's phone number (Bangladeshi format preferred)"
                },
                "email": {
                    "type": "string",
                    "description": "Guest's email address for booking confirmation"
                },
                "date": {
                    "type": "string",
                    "description": "Reservation date in YYYY-MM-DD format"
                },
                "time": {
                    "type": "string",
                    "description": "Reservation time in HH:MM 24-hour format"
                },
                "party_size": {
                    "type": "integer",
                    "description": "Number of guests in the party"
                },
                "duration_hours": {
                    "type": "number",
                    "description": "How many hours the table is needed. Default is 2.",
                    "default": 2.0
                },
                "occasion": {
                    "type": "string",
                    "description": "Special occasion if any: birthday, anniversary, corporate, etc.",
                    "default": ""
                }
            },
            "required": ["guest_name", "phone", "email", "date", "time", "party_size"]
        }
    }
}
