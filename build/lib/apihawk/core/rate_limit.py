# Rate limit handler for API requests
import time
import logging

class RateLimitHandler:
    def __init__(self, rate_limit=10, per_seconds=1):
        self.rate_limit = rate_limit
        self.per_seconds = per_seconds
        self.last_request_time = 0
        self.request_count = 0
        
    def wait_for_next_request(self):
        current_time = time.time()
        elapsed_time = current_time - self.last_request_time
        
        if elapsed_time < self.per_seconds:
            wait_time = self.per_seconds - elapsed_time
            logging.debug(f"Rate limit exceeded. Waiting for {wait_time:.2f} seconds.")
            time.sleep(wait_time)
        
        self.last_request_time = time.time()
        self.request_count += 1
        
        if self.request_count >= self.rate_limit:
            logging.debug(f"Rate limit reached. Resetting request count.")
            self.request_count = 0