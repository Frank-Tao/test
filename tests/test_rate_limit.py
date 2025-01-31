import pytest
from datetime import datetime, timedelta
from collections import defaultdict
from rate_limit import AccessLimiter  # Assuming the class is in access_limiter.py

@pytest.fixture
def limiter():
    """ Fixture to create a fresh AccessLimiter instance for each test """
    return AccessLimiter(limit=3, window=timedelta(seconds=5))

@pytest.fixture
def user_id():
    """ Fixture to provide a sample user ID """
    return "user_123"

def test_initial_access_allowed(limiter, user_id):
    """ Test that access is allowed initially within the limit """
    for i in range(limiter.limit):
        assert limiter.is_allowed(user_id), f"Request {i+1} should be allowed"

    # Exceeding limit should be blocked
    assert not limiter.is_allowed(user_id), "Request should be blocked after reaching the limit"

def test_access_blocked_after_limit(limiter, user_id):
    """ Test that access is blocked after reaching the limit """
    for _ in range(limiter.limit):
        limiter.is_allowed(user_id)
    assert not limiter.is_allowed(user_id), "Access should be blocked after limit is exceeded"

def test_window_expiry_allows_access_again(limiter, user_id):
    """ Test that access is restored after time window expires """
    for _ in range(limiter.limit):
        limiter.is_allowed(user_id)
    assert not limiter.is_allowed(user_id), "Access should be blocked after limit reached"

    # Simulate passage of time beyond the window
    limiter.access_records[user_id] = [datetime.now() - limiter.window - timedelta(seconds=1)]
    
    assert limiter.is_allowed(user_id), "Access should be allowed after time window resets"

def test_cleanup_old_records(limiter, user_id):
    """ Test that old records are properly removed from tracking """
    limiter.access_records[user_id] = [
        datetime.now() - timedelta(seconds=6),  # Should be cleaned up (expired)
        datetime.now() - timedelta(seconds=2),  # Should remain
    ]
    limiter._cleanup_old_records(user_id, datetime.now())

    assert len(limiter.access_records[user_id]) == 1, "Only valid timestamps should remain"

@pytest.mark.parametrize("access_count, expected_usage", [(1, 1), (2, 2), (3, 3)])
def test_usage_tracking(limiter, user_id, access_count, expected_usage):
    """ Test that get_usage() returns correct count """
    for _ in range(access_count):
        limiter.is_allowed(user_id)

    assert limiter.get_usage(user_id) == expected_usage, f"Usage count should be {expected_usage}"
