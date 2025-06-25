from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from api_rate_limiter.app.limiter import get_tokens
from fastapi import Path
from api_rate_limiter.app.config import RATE_LIMIT_CONFIG
from api_rate_limiter.app.redis_client import r

app = FastAPI(title = "Intelligent API Rate Limiting Service")


class RequestModel(BaseModel):
    api_key: str


@app.post("/check")
def check_limit(data: RequestModel):
    allowed, remaining = get_tokens(data.api_key)

    if not allowed:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    return {
        "allowed": allowed,
        "remaining_tokens": remaining
    }

@app.get("/status/{api_key}")
def status(api_key: str = Path(...)):
    token_key = f"tokens:{api_key}"
    time_key  = f"time:{api_key}"

    if not r:
        raise HTTPException(status_code=500, detail="Redis not available")

    tokens = r.get(token_key)
    last_refill = r.get(time_key)

    config = RATE_LIMIT_CONFIG.get(api_key, RATE_LIMIT_CONFIG["basic-user"])

    return {
        "api_key": api_key,
        "remaining_tokens": int(tokens) if tokens else config["TOKEN_LIMIT"],
        "last_refill": float(last_refill) if last_refill else None,
        "limit": config["TOKEN_LIMIT"],
        "refill_rate": config["REFILL_RATE"]
    }