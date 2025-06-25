import redis
import redis.exceptions
from api_rate_limiter.app.config import REDIS_HOST, REDIS_PORT

try:
    r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, decode_responses = True)
    r.ping()
except redis.exceptions.ConnectionError:
    print("Redis is not running")
    r = None