import redis
import json

r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

def get_user_cache(email: str):
    user = r.get(f"user:{email}")
    return json.loads(user) if user else None

def set_user_cache(email: str, data: dict):
    r.setex(f"user:{email}", 300, json.dumps(data))  # 5 mins cache
