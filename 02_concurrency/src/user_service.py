import asyncio
import os
import random
import time
from typing import Dict, Any

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

app = FastAPI(title="User Enrichment Service (fake)")

SEED = int(os.getenv("USER_SVC_SEED", "123"))
rng = random.Random(SEED)


async def jitter_sleep():
    delay = rng.randint(MIN_DELAY_MS, MAX_DELAY_MS) / 1000.0
    await asyncio.sleep(delay)

# Configurable behaviour
MIN_DELAY_MS = int(os.getenv("USER_SVC_MIN_DELAY_MS", "20"))
MAX_DELAY_MS = int(os.getenv("USER_SVC_MAX_DELAY_MS", "120"))
ERROR_RATE = float(os.getenv("USER_SVC_ERROR_RATE", "0.01"))      # 1% 500s
RATE_LIMIT_RATE = float(os.getenv("USER_SVC_RL_RATE", "0.02"))    # 2% 429s

TIERS = ["free", "pro", "enterprise"]
COUNTRIES = ["GB", "DE", "PL", "US", "CA", "FR", "NL"]

def profile_for(user_id: str) -> Dict[str, Any]:
    # Stable-ish synthetic profile based on user_id hash
    h = abs(hash(user_id))
    return {
        "user_id": user_id,
        "tier": TIERS[h % len(TIERS)],
        "country": COUNTRIES[h % len(COUNTRIES)],
        "age_days": (h % 3650),
        "flags": {
            "beta": (h % 10 == 0),
            "fraud_risk": (h % 97 == 0),
        },
    }

@app.get("/user/{user_id}")
async def get_user(user_id: str):
    await jitter_sleep()

    x = rng.random()
    if x < RATE_LIMIT_RATE:
        raise HTTPException(status_code=429, detail="rate limited (simulated)")
    if x < RATE_LIMIT_RATE + ERROR_RATE:
        raise HTTPException(status_code=500, detail="internal error (simulated)")

    return JSONResponse(content=profile_for(user_id))

@app.get("/health")
def health():
    return {"ok": True}
