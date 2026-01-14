import os

class Config:
    # Base directory
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    # OAuth files
    CREDENTIALS_FILE = os.path.join(BASE_DIR, 'credentials', 'credentials.json')
    TOKEN_FILE = os.path.join(BASE_DIR, 'credentials', 'token.json')

    # State file (tracks processed emails)
    STATE_FILE = os.path.join(BASE_DIR, 'state.json')

    # Google Sheet ID (get from your sheet URL)
    SPREADSHEET_ID = "put your id here"

    # Optional: Filter emails by subject (set too None to process all)
    FILTER_SUBJECT = None
