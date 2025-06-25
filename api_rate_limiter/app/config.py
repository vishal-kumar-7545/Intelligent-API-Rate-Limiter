import os

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
TOKEN_LIMIT = 10
REFILL_RATE = 10

RATE_LIMIT_CONFIG = {
    "test123":{
        "TOKEN_LIMIT":10,
        "REFILL_RATE": 10 #token per minute
    },
    "gold-user":{
        "TOKEN_LIMIT":100,
        "REFILL_RATE": 50
    },
    "basic-user":{
        "TOKEN_LIMIT":5,
        "REFILL_RATE": 2
    }
}