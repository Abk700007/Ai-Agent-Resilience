import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

import time
import random
import config 
from src.exceptions import TransientError, PermanentError
from src.resilience import RetryHandler, CircuitBreaker
from src.services import ElevenLabsService
from src.logger import AgentLogger
from alert import AlertSystem

def main():
    print("🚀 AI Agent Starting... (Press Ctrl+C to stop)")
    
    # 1. Initialize Components
    logger = AgentLogger()
    retry_handler = RetryHandler(
        max_retries=config.MAX_RETRIES, 
        initial_delay=config.INITIAL_DELAY, 
        backoff_factor=config.BACKOFF_FACTOR
    )
    
    # Circuit Breaker for ElevenLabs
    eleven_labs_breaker = CircuitBreaker(
        service_name="ElevenLabs",
        failure_threshold=config.CIRCUIT_FAILURE_THRESHOLD,
        recovery_timeout=config.CIRCUIT_RECOVERY_TIMEOUT
    )
    
    service = ElevenLabsService()
    
    # 2. Simulate a Queue of Contacts to Call
    contacts = [f"User_{i}" for i in range(1, 21)] # User 1 to User 20

    for contact in contacts:
        print(f"\n📞 Processing Call: {contact}")
        
        # --- CIRCUIT BREAKER CHECK ---
        # We wrap the service call in a lambda so the breaker can control execution
        def safe_call():
            return retry_handler.execute(service.generate_audio, f"Hello {contact}")

        try:
            # The Circuit Breaker runs the 'safe_call' (which contains the Retry logic)
            result = eleven_labs_breaker.call(safe_call)
            
            if result:
                logger.log_event("ElevenLabs", "SUCCESS", f"Audio generated for {contact}", circuit_state=eleven_labs_breaker.state)
                print(f"✅ Success: {result}")
            else:
                # If result is None, the Circuit Breaker blocked the call (Graceful Degradation)
                logger.log_event("ElevenLabs", "SKIPPED", f"Circuit Open - Skipping {contact}", circuit_state=eleven_labs_breaker.state)
                print(f"⏩ Circuit is OPEN. Skipping {contact} (Graceful Degradation).")
                # Simulate doing other work instead of crashing
                time.sleep(0.5)

        except Exception as e:
            # This block runs if Retries failed AND the Circuit Breaker logic let the error through
            logger.log_event("ElevenLabs", "FAILURE", str(e), circuit_state=eleven_labs_breaker.state)
            print(f"❌ Final Failure for {contact}: {e}")
            
            # ALERTING LOGIC [cite: 43-44]
            if eleven_labs_breaker.state == "OPEN":
                AlertSystem.notify_admin("CIRCUIT_OPEN", f"ElevenLabs is down. Stopping calls.")

        # Simulate time between calls
        time.sleep(1)

if __name__ == "__main__":
    main()