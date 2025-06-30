from dotenv import load_dotenv
import os

load_dotenv()

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
CACHE_TTL = int(os.getenv("CACHE_TTL", 300))
USE_REDIS_CACHE = os.getenv("USE_REDIS_CACHE", "false").lower() == "true" 