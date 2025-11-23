import os
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

class IngestionAgent:
    def __init__(self):
        self.creds = None
        self.service = None

    def authenticate(self):
        if os.path.exists('token.json'):
            self.creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                self.creds = flow.run_local_server(port=0)
            with open('token.json', 'w') as token:
                token.write(self.creds.to_json())
        
        self.service = build('gmail', 'v1', credentials=self.creds)

    def fetch_emails(self, days=7):
        if not self.service:
            self.authenticate()
        
        query = f"newer_than:{days}d"
        results = self.service.users().messages().list(userId='me', q=query).execute()
        messages = results.get('messages', [])
        
        email_data = []
        for message in messages:
            msg = self.service.users().messages().get(userId='me', id=message['id']).execute()
            email_data.append(msg)
            
        return email_data

    def run(self, params):
        days = params.get('days', 7)
        emails = self.fetch_emails(days)
        return {"status": "success", "count": len(emails), "data": emails}

if __name__ == "__main__":
    agent = IngestionAgent()
    # print(agent.run({'days': 1})) # Commented out to avoid auto-running auth
