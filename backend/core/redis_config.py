"""Module for Redis configuration"""
import redis

from core.config import Config


redis_cli = redis.Redis(
    host=Config.REDIS_HOST,
    port=Config.REDIS_PORT,
    db=Config.REDIS_DB,
    password=Config.REDIS_PASSWORD,
    decode_responses=True,
)
