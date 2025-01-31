from collections import defaultdict
from datetime import datetime, timedelta

class AccessLimiter:
    def __init__(self, limit: int, window: timedelta):
        """
        Initialize the access limiter.
        
        :param limit: Maximum number of allowed accesses within the time window.
        :param window: Time window for the limit (e.g., timedelta(hours=1)).
        """
        self.limit = limit
        self.window = window
        self.access_records = defaultdict(list)  # {user_id: [timestamps]}

    def is_allowed(self, user_id: str) -> bool:
        """
        Check if the user is allowed to access the resource.
        
        :param user_id: Unique identifier for the user.
        :return: True if access is allowed, False otherwise.
        """
        now = datetime.now()
        self._cleanup_old_records(user_id, now)

        if len(self.access_records[user_id]) < self.limit:
            self.access_records[user_id].append(now)
            return True
        return False

    def _cleanup_old_records(self, user_id: str, current_time: datetime):
        """
        Remove access records that are outside the current time window.
        
        :param user_id: Unique identifier for the user.
        :param current_time: Current timestamp.
        """
        self.access_records[user_id] = [
            timestamp for timestamp in self.access_records[user_id]
            if current_time - timestamp <= self.window
        ]

    def get_usage(self, user_id: str) -> int:
        """
        Get the current usage count for a user.
        
        :param user_id: Unique identifier for the user.
        :return: Number of accesses within the current window.
        """
        self._cleanup_old_records(user_id, datetime.now())
        return len(self.access_records[user_id])