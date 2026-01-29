import random
import time
from src.exceptions import TransientError, PermanentError

class ElevenLabsService:
    """
    Mock Service for Audio Generation.
    """
    def generate_audio(self, text):
        print(f"🎤 Calling ElevenLabs API for: '{text[:10]}...'")
        time.sleep(0.5) # Simulate network

        # Randomly decide what happens
        # 0.0 - 0.6: Success
        # 0.6 - 0.9: Transient Error (503 Service Unavailable) - REQUIRED SCENARIO
        # 0.9 - 1.0: Permanent Error (401 Unauthorized)
        
        dice = random.random()

        if dice < 0.6:
            return "audio_file.mp3"
        elif dice < 0.9:
            raise TransientError("503 Service Unavailable")
        else:
            raise PermanentError("401 Unauthorized")

class LLMService:
    """
    Mock Service for Text Generation.
    """
    def generate_text(self, prompt):
        print(f"🤖 Calling LLM API...")
        time.sleep(0.5)
        # LLM is more stable, 90% success
        if random.random() < 0.9:
            return "This is a generated response."
        else:
            raise TransientError("LLM Timeout")