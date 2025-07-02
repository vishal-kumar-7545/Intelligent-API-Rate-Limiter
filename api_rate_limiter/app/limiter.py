import time
from fastapi import HTTPException
from api_rate_limiter.app.config import RATE_LIMIT_CONFIG
from api_rate_limiter.app.redis_client import r


def is_request_allowed(api_key: str) -> bool:
    config_key = f"config: {api_key}"

    if not r.exists(config_key):
        raise HTTPException(status_code=404, detail="API key not found")
    
    #get all fields
    config = r.hgetall(config_key)
    try:
        limit = int(config["limit"])
        refill_rate = float(config["refill_rate"])
        tokens = float(config["tokens"])
        last_refill = float(config["last_refill"])
    except KeyError:
        raise HTTPException(status_code=500, detail="Incomplete rate limit config")
    except ValueError:
        raise HTTPException(status_code=500, detail="Corrupted rate limit values")
    
    now = time.time()
    elapsed = now - last_refill

    #refill token based on elapsed time and refill rate

    if tokens < 1:
        # not enough tokens -- reject request
        r.hset(config_key, mapping={
            "tokens": tokens,
            "last_refill": now
        })
        return False
    else:
        #allow request and consume a token
        tokens -= 1
        r.hset(config_key, mapping={
            "tokens": tokens,
            "last_refill": now
        })
        return True
