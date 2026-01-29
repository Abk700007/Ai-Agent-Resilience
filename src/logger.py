import os
import csv
import time
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import config

class AgentLogger:
    def __init__(self):
        # Ensure log directory exists
        os.makedirs(os.path.dirname(config.LOG_FILE), exist_ok=True)
        self.sheets_service = self._get_sheets_service()

    def _get_sheets_service(self):
        creds = None
        if os.path.exists('credentials/token.json'):
            try:
                creds = Credentials.from_authorized_user_file('credentials/token.json', config.SCOPES)
            except:
                creds = None

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                except:
                    creds = None
            
            if not creds and os.path.exists('credentials/credentials.json'):
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials/credentials.json', config.SCOPES)
                creds = flow.run_local_server(port=0)
                # Save token for next time
                with open('credentials/token.json', 'w') as token:
                    token.write(creds.to_json())

        if creds:
            return build('sheets', 'v4', credentials=creds)
        else:
            print("⚠️ Warning: No Google Sheets credentials found. Logging to file only.")
            return None

    def log_event(self, service_name, event_type, details, retry_count=0, circuit_state="CLOSED"):
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        
        # 1. Log to Console
        print(f"📝 [LOG] {timestamp} | {service_name} | {event_type} | {details}")

        # 2. Log to File (Structured CSV format)
        with open(config.LOG_FILE, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([timestamp, service_name, event_type, details, retry_count, circuit_state])

        # 3. Log to Google Sheets
        if self.sheets_service:
            try:
                values = [[timestamp, service_name, event_type, details, retry_count, circuit_state]]
                body = {'values': values}
                self.sheets_service.spreadsheets().values().append(
                    spreadsheetId=config.SPREADSHEET_ID,
                    range="Sheet1!A1",
                    valueInputOption="RAW",
                    body=body
                ).execute()
            except Exception as e:
                print(f"❌ Failed to log to Sheets: {e}")