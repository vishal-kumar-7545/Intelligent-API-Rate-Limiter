from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from api_rate_limiter.app.limiter import is_request_allowed
from fastapi import Path
from api_rate_limiter.app.config import RATE_LIMIT_CONFIG
from api_rate_limiter.app.redis_client import r
import time

app = FastAPI(title = "Intelligent API Rate Limiting Service")


class RequestModel(BaseModel):
    api_key: str


class RegisterKeyInput(BaseModel):
    api_key : str
    limit: int
    refill_Rate: float


@app.post("/register_key")
def register_key(data:RegisterKeyInput):
    key = f"config: {data.api_key}"
    if r.exists(key):
        raise HTTPException(status_code=400, detail="API key alreay exists")
    
    now = time.time()
    r.hset(key, mapping={
        "limit": data.limit,
        "refill_rate": data.refill_Rate,
        "tokens": data.limit,
        "last_refill": now
    })

    return {"message": f"API key {data.api_key} registered succussfully"}


@app.post("/check")
def check_limit(api_key: str = Query(...)):
    allowed = is_request_allowed(api_key)
    return {"allowed": allowed}


@app.get("/status/{api_key}")
def get_status(api_key: str = Path(...)):
    key = f"config: {api_key}"
    if not r.exists(key):
        raise HTTPException(status_code=404, detail="API key not found")
    return r.hgetall(key)