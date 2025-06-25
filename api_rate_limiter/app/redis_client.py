import redis
import redis.exceptions
from config import REDIS_HOST, REDIS_PORT

try:
    r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses = True)
    r.ping()
except redis.exceptions.ConnectionError:
    print("Redis is not running")
    r = None