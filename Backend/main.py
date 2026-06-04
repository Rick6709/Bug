import asyncio
import hmac
import hashlib
import time
import json
import os
from contextlib import asynccontextmanager
from datetime import datetime, timezone

import httpx
import websockets
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from uvicorn import run
from dotenv import load_dotenv

load_dotenv()

# Global state to store the latest data
app_state = {
    "price": "0.00",
    "wallet": "0.00",
    "equity": "0.00",
    "pnl": "0.00",
    "last_update": 0,
}

@asynccontextmanager
async def lifespan(app: FastAPI):
    price_task = asyncio.create_task(price_streamer())
    balance_task = asyncio.create_task(balance_poller())
    yield
    price_task.cancel()
    balance_task.cancel()

app = FastAPI(
    title="Binance Bug Bot Backend",
    description="Asynchronous crypto tracking and trading bot platform for Binance Futures.",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

async def price_streamer():
    """Persistent WebSocket connection to Binance for BTCUSDT mark price."""
    url = "wss://fstream.binance.com/ws/btcusdt@markPrice"
    while True:
        try:
            async with websockets.connect(url) as websocket:
                print("-> WebSocket: Connected to BTCUSDT stream")
                while True:
                    msg = await websocket.recv()
                    data = json.loads(msg)
                    if "p" in data:
                        app_state["price"] = f"{float(data['p']):.2f}"
        except Exception as e:
            print(f"WebSocket Error: {e}. Reconnecting in 5s...")
            await asyncio.sleep(5)

async def balance_poller():
    """Periodic balance check via REST API (every 30 seconds)."""
    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_SECRET_KEY")
    url = "https://fapi.binance.com/fapi/v2/account"

    if not api_key or not api_secret:
        print("API Keys missing in .env! Balance polling disabled.")
        return

    async with httpx.AsyncClient() as client:
        while True:
            try:
                timestamp = int(time.time() * 1000)
                query_string = f"timestamp={timestamp}"
                signature = hmac.new(
                    api_secret.encode("utf-8"),
                    query_string.encode("utf-8"),
                    hashlib.sha256,
                ).hexdigest()

                headers = {"X-MBX-APIKEY": api_key}
                params = {"timestamp": timestamp, "signature": signature}

                response = await client.get(url, headers=headers, params=params)
                data = response.json()

                if response.status_code != 200:
                    print(f"Binance API Error: {data}")
                    continue

                app_state["wallet"] = f"{float(data.get('totalWalletBalance', 0)):.2f}"
                app_state["equity"] = f"{float(data.get('totalMarginBalance', 0)):.2f}"
                app_state["pnl"] = f"{float(data.get('totalUnrealizedProfit', 0)):.2f}"
                app_state["last_update"] = timestamp
                print(f"-> Balance Updated: {app_state['wallet']} USDT (PnL: {app_state['pnl']})")
            except Exception as e:
                print(f"Balance Poller Error: {e}")

            await asyncio.sleep(30)

def _format_last_update() -> str | None:
    ts = app_state["last_update"]
    if not ts:
        return None
    return datetime.fromtimestamp(ts / 1000, tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

def _status_payload():
    return {
        "price": app_state["price"],
        "wallet": app_state["wallet"],
        "equity": app_state["equity"],
        "pnl": app_state["pnl"],
        "symbol": "BTCUSDT",
        "currency": "USDT",
        "last_update": _format_last_update(),
    }

@app.get("/")
async def read_root():
    return {"message": "Binance Bug Bot Backend is running!"}

@app.get("/api/status")
@app.get("/api/v1/status")
async def get_status():
    """Serves the latest price and balance from memory."""
    return _status_payload()

if __name__ == "__main__":
    run(app, host="0.0.0.0", port=8000)
