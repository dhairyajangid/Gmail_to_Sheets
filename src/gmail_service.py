"""Gmail Service - Handles Gmail API operations"""

import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from config import Config

SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

class GmailService:
    def __init__(self):
        self.service = self._authenticate()

    def _authenticate(self):
        """Login to Gmail using OAuth 2.0"""
        creds = None

        # Load saved token if exists
        if os.path.exists(Config.TOKEN_FILE):
            creds = Credentials.from_authorized_user_file(Config.TOKEN_FILE, SCOPES)

        # Refresh or create new token
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    Config.CREDENTIALS_FILE, SCOPES)
                creds = flow.run_local_server(port=0)

            # Save token for next time
            with open(Config.TOKEN_FILE, 'w') as token:
                token.write(creds.to_json())

        return build('gmail', 'v1', credentials=creds)

    def get_unread_emails(self):
        """Fetch unread emails from inbox"""
        result = self.service.users().messages().list(
            userId='me',
            q='is:unread in:inbox',
            maxResults=100
        ).execute()

        messages = result.get('messages', [])

        # Get full email details
        emails = []
        for msg in messages:
            email = self.service.users().messages().get(
                userId='me',
                id=msg['id'],
                format='full'
            ).execute()
            emails.append(email)

        return emails

    def mark_as_read(self, email_id):
        """Mark email as read"""
        self.service.users().messages().modify(
            userId='me',
            id=email_id,
            body={'removeLabelIds': ['UNREAD']}
        ).execute()