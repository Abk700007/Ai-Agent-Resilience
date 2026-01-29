import time
import random
from src.exceptions import TransientError

class RetryHandler:
    """
    Handles logic for retrying operations with exponential backoff.
    """
    def __init__(self, max_retries=3, initial_delay=2, backoff_factor=2):
        self.max_retries = max_retries
        self.initial_delay = initial_delay
        self.backoff_factor = backoff_factor

    def execute(self, func, *args, **kwargs):
        attempt = 0
        delay = self.initial_delay

        while True:
            try:
                return func(*args, **kwargs)
            except TransientError as e:
                attempt += 1
                if attempt > self.max_retries:
                    print(f" Max retries ({self.max_retries}) reached. Giving up.")
                    raise e  
                
                print(f"Transient Error: {e}. Retrying in {delay}s... (Attempt {attempt}/{self.max_retries})")
                time.sleep(delay)
                delay *= self.backoff_factor  # Exponential Backoff
            except Exception as e:
                
                raise e

class CircuitBreaker:
    """
    Prevents calling a dead service to avoid cascading failures.
    States: CLOSED (Normal) -> OPEN (Broken) -> HALF-OPEN (Testing)
    """
    def __init__(self, service_name, failure_threshold=3, recovery_timeout=10):
        self.service_name = service_name
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        
        self.state = "CLOSED"  
        self.failures = 0
        self.last_failure_time = 0

    def call(self, func, *args, **kwargs):
        # 1. Check Circuit State
        if self.state == "OPEN":
            if (time.time() - self.last_failure_time) > self.recovery_timeout:
                print(f"🔄 {self.service_name} Circuit recovery timeout passed. Switching to HALF-OPEN.")
                self.state = "HALF-OPEN"
            else:
                print(f"{self.service_name} Circuit is OPEN. Blocking call.")
                return None  # Fail fast!

        # 2. Try the function
        try:
            result = func(*args, **kwargs)
            
            # If successful in HALF-OPEN, we are back to normal!
            if self.state == "HALF-OPEN":
                print(f" {self.service_name} recovered! Circuit Reset to CLOSED.")
                self.reset()
            return result

        except Exception as e:
            self.failures += 1
            self.last_failure_time = time.time()
            print(f" {self.service_name} Failure detected ({self.failures}/{self.failure_threshold})")

            if self.failures >= self.failure_threshold:
                if self.state != "OPEN":
                    print(f" {self.service_name} Failure Threshold Reached! Circuit OPENed.")
                self.state = "OPEN"
            
            raise e

    def reset(self):
        self.state = "CLOSED"
        self.failures = 0