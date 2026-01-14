"""Email Parser - Extract data from Gmail messages"""

import base64
from email.utils import parsedate_to_datetime

class EmailParser:
    # Maximum characters allowed in a Google Sheets cell
    MAX_CELL_LENGTH = 49900  # Set slightly below 50000 for safety margin

    def parse(self, email_data):
        """Extract sender, subject, date, and content from email"""
        headers = email_data['payload']['headers']

        # Get header values
        sender = self._get_header(headers, 'From')
        subject = self._get_header(headers, 'Subject')
        date_raw = self._get_header(headers, 'Date')
        date = self._format_date(date_raw)

        # Get email body
        body = self._get_body(email_data['payload'])

        # Truncate all fields to be safe
        sender = self._truncate(sender)
        subject = self._truncate(subject)
        date = self._truncate(date)
        body = self._truncate(body)

        return {
            'from': sender,
            'subject': subject,
            'date': date,
            'content': body
        }

    def _truncate(self, text):
        """Truncate text if too long"""
        if text and len(text) > self.MAX_CELL_LENGTH:
            return text[:self.MAX_CELL_LENGTH - 20] + "\n\n[TRUNCATED]"
        return text

    def _get_header(self, headers, name):
        """Find header by name"""
        for header in headers:
            if header['name'].lower() == name.lower():
                return header['value']
        return ''

    def _format_date(self, date_string):
        """Convert date to readable format"""
        try:
            dt = parsedate_to_datetime(date_string)
            return dt.strftime('%Y-%m-%d %H:%M:%S')
        except:
            return date_string

    def _get_body(self, payload):
        """Extract plain text body"""
        body = ''

        if 'parts' in payload:
            for part in payload['parts']:
                if part['mimeType'] == 'text/plain':
                    body = self._decode(part['body'])
                    break
        elif 'body' in payload:
            body = self._decode(payload['body'])

        return body.strip()

    def _decode(self, body_data):
        """Decode base64 email body"""
        if 'data' in body_data:
            try:
                decoded = base64.urlsafe_b64decode(body_data['data'])
                return decoded.decode('utf-8', errors='ignore')
            except Exception as e:
                print(f"Error decoding email body: {e}")
                return ''
        return ''