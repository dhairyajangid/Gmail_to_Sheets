"""Sheets Service - Handles Google Sheets API operations"""

import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from config import Config

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

class SheetsService:
    MAX_CELL_LENGTH = 50000  # Google Sheets limit

    def __init__(self):
        self.service = self._authenticate()
        self._create_headers()

    def _authenticate(self):
        """Login to Google Sheets using OAuth 2.0"""
        creds = None
        token_file = Config.TOKEN_FILE.replace('token.json', 'sheets_token.json')

        # Load saved token if exists
        if os.path.exists(token_file):
            creds = Credentials.from_authorized_user_file(token_file, SCOPES)

        # Refresh or create new token
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    Config.CREDENTIALS_FILE, SCOPES)
                creds = flow.run_local_server(port=0)

            # Save token for next time
            with open(token_file, 'w') as token:
                token.write(creds.to_json())

        return build('sheets', 'v4', credentials=creds)

    def _create_headers(self):
        """Add headers if sheet is empty"""
        result = self.service.spreadsheets().values().get(
            spreadsheetId=Config.SPREADSHEET_ID,
            range='A1:D1'
        ).execute()

        # If first row is empty, add headers
        if not result.get('values'):
            self.service.spreadsheets().values().update(
                spreadsheetId=Config.SPREADSHEET_ID,
                range='A1:D1',
                valueInputOption='RAW',
                body={'values': [['From', 'Subject', 'Date', 'Content']]}
            ).execute()

    def _truncate_if_needed(self, text):
        """Truncate text if it exceeds Google Sheets limit"""
        if text and len(text) > self.MAX_CELL_LENGTH:
            return text[:self.MAX_CELL_LENGTH - 50] + "\n\n[TRUNCATED]"
        return text

    def append_emails(self, emails):
        """Append email rows to sheet"""
        rows = []
        for email in emails:
            # Apply truncation to all fields as a safety measure
            rows.append([
                self._truncate_if_needed(email['from']),
                self._truncate_if_needed(email['subject']),
                self._truncate_if_needed(email['date']),
                self._truncate_if_needed(email['content'])
            ])

        self.service.spreadsheets().values().append(
            spreadsheetId=Config.SPREADSHEET_ID,
            range='A:D',
            valueInputOption='RAW',
            insertDataOption='INSERT_ROWS',
            body={'values': rows}
        ).execute()