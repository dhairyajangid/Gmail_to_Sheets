"""Main script - Gmail to Sheets automation"""

import json
import os
from datetime import datetime
from src.gmail_service import GmailService
from src.sheets_service import SheetsService
from src.email_parser import EmailParser
from config import Config

def log(message):
    """Print message with timestamp"""
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}")

def load_processed_emails():
    """Load list of already processed email IDs"""
    if os.path.exists(Config.STATE_FILE):
        with open(Config.STATE_FILE, 'r') as f:
            data = json.load(f)
            return set(data.get('processed_ids', []))
    return set()

def save_processed_emails(processed_ids):
    """Save list of processed email IDs"""
    with open(Config.STATE_FILE, 'w') as f:
        json.dump({
            'processed_ids': list(processed_ids),
            'last_run': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }, f, indent=2)

def main():
    log("Starting Gmail to Sheets automation...")

    # Load previously processed emails
    processed_ids = load_processed_emails()
    log(f"Already processed: {len(processed_ids)} emails")

    # Connect to Gmail
    log("Connecting to Gmail...")
    gmail = GmailService()

    # Connect to Sheets
    log("Connecting to Google Sheets...")
    sheets = SheetsService()

    # Get unread emails
    log("Fetching unread emails...")
    emails = gmail.get_unread_emails()

    if not emails:
        log("No unread emails found")
        return

    log(f"Found {len(emails)} unread emails")

    # Process emails
    parser = EmailParser()
    new_emails = []

    for email_data in emails:
        email_id = email_data['id']

        # Skip if already processed
        if email_id in processed_ids:
            continue

        # Parse email
        parsed = parser.parse(email_data)

        # Apply subject filter if set
        if Config.FILTER_SUBJECT:
            if Config.FILTER_SUBJECT.lower() not in parsed['subject'].lower():
                processed_ids.add(email_id)
                gmail.mark_as_read(email_id)
                continue

        new_emails.append(parsed)
        processed_ids.add(email_id)
        log(f"Parsed: {parsed['subject'][:50]}")

    # Write to sheet
    if new_emails:
        log(f"Writing {len(new_emails)} emails to sheet...")

        # DEBUG: Check each email for length issues
        for i, email in enumerate(new_emails):
            for field, value in email.items():
                if value and len(str(value)) > 50000:
                    log(f"ERROR: Email #{i+1} '{email['subject'][:30]}...' has {field} with {len(str(value))} chars!")
                    # Force truncate here as emergency fix
                    email[field] = str(value)[:49950] + "\n[TRUNCATED]"

        sheets.append_emails(new_emails)

        # Mark as read
        log("Marking emails as read...")
        for email_data in emails:
            if email_data['id'] in processed_ids:
                gmail.mark_as_read(email_data['id'])

        log(f"Successfully processed {len(new_emails)} emails")
    else:
        log("No new emails to process")

    # Save state
    save_processed_emails(processed_ids)
    log("Done!")

if __name__ == "__main__":
    main()