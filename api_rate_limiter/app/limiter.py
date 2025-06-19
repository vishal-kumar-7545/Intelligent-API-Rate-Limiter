import time

TOKEN_LIMIT = 10
REFILL_RATE = 10

buckets = {}

def get_tokens(api_key: str):
    current_time = time.time()
    if api_key not in buckets:
        buckets[api_key] = {
            "tokens": TOKEN_LIMIT,
            "last_refill": current_time
        }

    bucket = buckets[api_key]
    print(current_time, bucket["last_refill"])

    time_passed = current_time - bucket["last_refill"]
    token_to_add = int((time_passed/60) * REFILL_RATE)

    if token_to_add > 0:
        bucket["tokens"] = min(TOKEN_LIMIT, bucket["tokens"]+token_to_add)
        bucket["last_refill"] = current_time
    
    if bucket["tokens"]>0:
        bucket["tokens"] -= 1
        return True, bucket["tokens"]
    else:
        return False, 0