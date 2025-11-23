from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
import os

class OrganizerAgent:
    def __init__(self):
        self.creds = None
        if os.path.exists('token.json'):
            self.creds = Credentials.from_authorized_user_file('token.json')
        
        self.calendar_service = build('calendar', 'v3', credentials=self.creds) if self.creds else None
        self.drive_service = build('drive', 'v3', credentials=self.creds) if self.creds else None

    def create_event(self, event_data):
        if not self.calendar_service:
            return "Error: No credentials"
            
        event = {
            'summary': event_data.get('title'),
            'location': event_data.get('location', ''),
            'description': event_data.get('description', ''),
            'start': {
                'dateTime': event_data.get('start_time'), # ISO format
                'timeZone': 'UTC',
            },
            'end': {
                'dateTime': event_data.get('end_time'),
                'timeZone': 'UTC',
            },
        }
        
        event = self.calendar_service.events().insert(calendarId='primary', body=event).execute()
        return f"Event created: {event.get('htmlLink')}"

    def upload_file(self, file_path, folder_id=None):
        if not self.drive_service:
            return "Error: No credentials"
            
        file_metadata = {'name': os.path.basename(file_path)}
        if folder_id:
            file_metadata['parents'] = [folder_id]
            
        media = MediaFileUpload(file_path, resumable=True)
        file = self.drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        return f"File ID: {file.get('id')}"

    def run(self, categorized_items):
        results = []
        for item in categorized_items:
            category = item['classification'].get('category')
            metadata = item['classification'].get('metadata', {})
            
            if category == 'event':
                res = self.create_event(metadata)
                results.append(res)
            elif category == 'bill' or category == 'document':
                # Logic to save to drive would go here
                results.append(f"Would upload {item['file']} to Drive")
                
        return results

if __name__ == "__main__":
    pass
