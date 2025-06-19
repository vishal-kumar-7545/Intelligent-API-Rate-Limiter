from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from limiter import get_tokens

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


@app.get("/ping")
async def ping():
    return {"message": "pong"}

