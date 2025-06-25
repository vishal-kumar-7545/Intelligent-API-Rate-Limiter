import time
import redis
from config import REDIS_HOST, REDIS_PORT, TOKEN_LIMIT, REFILL_RATE


#Connet to redis
r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses = True)

def get_tokens(api_key:str):
    current_time = time.time()

    token_key = f"tokens:{api_key}"
    time_key = f"time:{api_key}"

    tokens = r.get(token_key)
    last_refill = r.get(time_key)

    if tokens is None:
        tokens = TOKEN_LIMIT
        r.set(token_key, TOKEN_LIMIT)
    else:
        tokens = int(tokens)

    if last_refill is None:
        last_refill = current_time
        r.set(time_key, current_time)
    else:
        last_refill = float(last_refill)

    #calculate time
    time_passed = current_time - last_refill
    tokens_to_add = int((time_passed/60)* REFILL_RATE)

    if tokens_to_add > 0:
        tokens = min(TOKEN_LIMIT, tokens + tokens_to_add)
        r.set(token_key, tokens)
        r.set(time_key, current_time)

    if tokens > 0:
        tokens -= 1
        r.set(token_key, tokens)
        return True, tokens
    else:
        return False, 0
