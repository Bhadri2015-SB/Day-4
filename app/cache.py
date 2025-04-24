import redis
import json
import dotenv
import os

dotenv.load_dotenv()
# host = os.getenv("REDIS_HOST")
# port = os.getenv("REDIS_PORT")

# r = redis.Redis(host=host, port=port, db=0, decode_responses=True)
REDIS_URL = os.getenv("REDIS_URL") 

r = redis.from_url(REDIS_URL, decode_responses=True)

def get_user_cache(email: str):
    user = r.get(f"user:{email}")
    return json.loads(user) if user else None

def set_user_cache(email: str, data: dict):
    r.setex(f"user:{email}", 300, json.dumps(data))  # 5 mins cache
