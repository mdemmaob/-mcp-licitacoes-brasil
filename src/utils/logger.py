import logging
from src.config import LOG_LEVEL
import os

os.makedirs('logs', exist_ok=True)

logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("logs/app.log"),
        logging.StreamHandler()
    ]
)

def get_logger(name):
    return logging.getLogger(name) 