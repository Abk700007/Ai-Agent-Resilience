import os

# --- Google Sheets Config ---
SPREADSHEET_ID = "197qIsQmYkqqFCQSUDct184qiGmb4H2d1ALcvaIPwDzE"  
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# --- Resilience Config ---
MAX_RETRIES = 3
INITIAL_DELAY = 5        # Seconds
BACKOFF_FACTOR = 2       # Double the wait time each retry
CIRCUIT_FAILURE_THRESHOLD = 3
CIRCUIT_RECOVERY_TIMEOUT = 10  # Seconds before trying again

# --- Alert Config ---
ADMIN_EMAIL = "admin@example.com"
TELEGRAM_CHAT_ID = "123456789"
WEBHOOK_URL = "https://example.com/webhook"

# --- Logging Config ---
LOG_FILE = "logs/agent_activity.log"