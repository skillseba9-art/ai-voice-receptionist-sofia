import asyncio
import os
import httpx
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from bot import run_bot

load_dotenv()

app = FastAPI(title="Crimson Courtyard Voice Bot")
app.mount("/static", StaticFiles(directory="static"), name="static")

DAILY_API_KEY = os.getenv("DAILY_API_KEY")
DAILY_API_BASE = "https://api.daily.co/v1"


async def create_daily_room() -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{DAILY_API_BASE}/rooms",
            headers={"Authorization": f"Bearer {DAILY_API_KEY}"},
            json={
                "properties": {
                    "max_participants": 2,
                    "exp": 3600,
                    "enable_screenshare": False,
                    "enable_chat": False,
                }
            }
        )
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Failed to create Daily room")
        return response.json()


async def create_bot_token(room_name: str) -> str:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{DAILY_API_BASE}/meeting-tokens",
            headers={"Authorization": f"Bearer {DAILY_API_KEY}"},
            json={
                "properties": {
                    "room_name": room_name,
                    "is_owner": True,
                }
            }
        )
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Failed to create bot token")
        return response.json()["token"]


@app.get("/", response_class=HTMLResponse)
async def index():
    with open("static/index.html", "r", encoding="utf-8") as f:
        return f.read()


@app.post("/start-call")
async def start_call():
    room = await create_daily_room()
    bot_token = await create_bot_token(room["name"])
    asyncio.create_task(run_bot(room["url"], bot_token))
    return {"room_url": room["url"]}


if __name__ == "__main__":
    import uvicorn
    print("\n The Crimson Courtyard Voice Bot")
    print(" Open: http://localhost:8000\n")
    uvicorn.run(app, host="0.0.0.0", port=8000)
