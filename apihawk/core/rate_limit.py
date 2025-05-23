# Rate limit handler for API requests
import time
import logging


# Set on hold for now
"""class RateLimitHandler:
    def __init__(self, rate_limit=10, per_seconds=1):
        self.rate_limit = rate_limit
        self.per_seconds = per_seconds
        self.request_count = 0
        self.last_reset_time = self._get_current_time()
    
    def _get_current_time(self):
        return time.time()
        
    def wait_for_next_request(self):
        current_time = self._get_current_time()

        # Only reset count if we're in a new time window (full second has passed)
        elapsed = int(current_time) - int(self.last_reset_time)
        if elapsed >= self.per_seconds:
            self.request_count = 0
            self.last_reset_time = current_time

        # If we've hit the rate limit, sleep until next window
        if self.request_count >= self.rate_limit:
            time.sleep(self.per_seconds)
            self.request_count = 0
            self.last_reset_time = self._get_current_time()

        self.request_count += 1
        return self.request_count"""


class RateLimitHandler:
    def __init__(self, rate_limit=10, per_seconds=1):
        self.rate_limit = rate_limit
        self.per_seconds = per_seconds
        self.request_count = 0
        self.last_reset_time = time.time()

        def wait_for_next_request(self):
            current_time = time.time()

            elapsed = int(current_time) - int(self.last_reset_time)
            if elapsed >= self.per_seconds:
                self.request_count = 0
                self.last_reset_time = time.time()


if __name__ == "__main__":

    rate_limit_handler = RateLimitHandler(rate_limit=5, per_seconds=1)

    try:
        while True:
            rate_limit_handler.wait_for_next_request()
            print(f"Request count: {rate_limit_handler.request_count}")
            time.sleep(0.2)  # Simulate some work being done
    except KeyboardInterrupt:
        print("\nExiting rate limit handler...")
