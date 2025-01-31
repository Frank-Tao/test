import redis
import time
from datetime import timedelta

class RedisAccessLimiter:
    def __init__(self, limit: int, window: timedelta, redis_client: redis.Redis):
        """
        Initialize the Redis-based access limiter.
        
        :param limit: Maximum number of allowed accesses within the time window.
        :param window: Time window for the limit (e.g., timedelta(hours=1)).
        :param redis_client: Redis client instance.
        """
        self.limit = limit
        self.window = window
        self.redis = redis_client

    def is_allowed(self, user_id: str) -> bool:
        """
        Check if the user is allowed to access the resource.
        
        :param user_id: Unique identifier for the user.
        :return: True if access is allowed, False otherwise.
        """
        key = f"access:{user_id}"
        now = int(time.time())  # Current timestamp in seconds
        pipeline = self.redis.pipeline()
        
        # Add the current access timestamp to the sorted set
        pipeline.zadd(key, {now: now})
        
        # Remove old records outside the time window
        pipeline.zremrangebyscore(key, 0, now - self.window.total_seconds())
        
        # Get the count of accesses within the window
        pipeline.zcard(key)
        
        # Execute the pipeline
        _, _, count = pipeline.execute()
        
        # Check if the count is within the limit
        return count <= self.limit

    def get_usage(self, user_id: str) -> int:
        """
        Get the current usage count for a user.
        
        :param user_id: Unique identifier for the user.
        :return: Number of accesses within the current window.
        """
        key = f"access:{user_id}"
        now = int(time.time())
        
        # Remove old records and get the count
        self.redis.zremrangebyscore(key, 0, now - self.window.total_seconds())
        return self.redis.zcard(key)