# 📧 Gmail to Sheets Automation

**Author:** [Your Full Name]

## 📖 What This Does

Automatically reads unread emails from Gmail and saves them to Google Sheets.

**Features:**
- ✅ No duplicate emails
- ✅ Marks emails as read after processing
- ✅ Logs everything with timestamps
- ✅ Optional subject-based filtering (bonus)

---

## 🏗️ How It Works

```
Gmail Inbox → Python Script → Google Sheet
     ↓              ↓              ↓
Unread Emails   Parse Data    Save Rows
Mark as Read    Check State   Avoid Duplicates
```

**Flow:**
1. Script reads unread Gmail emails
2. Checks `state.json` to see which emails we already processed
3. Only processes NEW emails
4. Saves email details to Google Sheet
5. Marks emails as read
6. Updates `state.json` with processed email IDs

---

## 📂 Project Structure

```
gmail-to-sheets/
│
├── src/
│   ├── gmail_service.py      # Gmail API (login, fetch, mark read)
│   ├── sheets_service.py     # Sheets API (login, append rows)
│   ├── email_parser.py       # Extract data from emails
│   └── main.py               # Main script (runs everything)
│
├── credentials/
│   └── credentials.json      # Your OAuth credentials
│
├── config.py                 # Settings (Spreadsheet ID, filter)
├── requirements.txt          # Python packages needed
├── state.json                # Tracks processed emails (auto-created)
├── .gitignore                # Protects credentials
└── README.md                 # This file
```

---

## 🚀 Setup Instructions

### Step 1: Install Python Packages
```bash
pip install -r requirements.txt
```

### Step 2: Add credentials.json
1. You already have this from Google Cloud Console
2. Put it in: `credentials/credentials.json`

### Step 3: Create Google Sheet
1. Go to Google Sheets
2. Create a new blank sheet
3. Copy the ID from URL:
   ```
   https://docs.google.com/spreadsheets/d/COPY_THIS_PART/edit
   ```

### Step 4: Update config.py
Open `config.py` and paste your Spreadsheet ID:
```python
SPREADSHEET_ID = 'paste_your_id_here'
```

### Step 5: Run!
```bash
python main.py
```

**First Run:**
- Browser opens for Gmail login → Click "Allow"
- Browser opens again for Sheets login → Click "Allow"
- Script runs and processes emails

**Next Runs:**
- No browser needed (uses saved tokens)

---

## 🔐 How OAuth Works

**First Time:**
1. Script looks for saved tokens
2. Not found → Opens browser
3. You login and allow access
4. Token saved in `credentials/`

**Next Times:**
1. Script uses saved token
2. If expired → Auto-refreshes
3. No browser needed

---

## 🔄 How Duplicate Prevention Works

**Problem:** If we run script twice, same emails get added again

**Solution:** Track processed email IDs

**Method:**
1. Every Gmail message has unique ID (never changes)
2. After processing → Save ID to `state.json`
3. Next run → Check if ID exists in state
4. If exists → Skip
5. If new → Process

**Example state.json:**
```json
{
  "processed_ids": ["msg_123", "msg_456", "msg_789"],
  "last_run": "2026-01-14 10:30:00"
}
```

**Why this works:**
- ✅ Fast (no need to check Google Sheets)
- ✅ Reliable (email IDs never change)
- ✅ Simple (just one JSON file)

---

## 💾 State Persistence

**File:** `state.json`

**What it stores:**
- List of processed email IDs
- Last run timestamp

**Why JSON file:**
- Simple and readable
- No database needed
- Easy to reset (just delete file)
- Won't be committed to Git (.gitignore protects it)

---

## 📊 Bonus Features

### 1. Logging with Timestamps
Every action is logged with timestamp:
```
[2026-01-14 10:30:45] 🚀 Starting Gmail to Sheets automation...
[2026-01-14 10:30:46] 📧 Connecting to Gmail...
[2026-01-14 10:30:47] 📬 Found 5 unread emails
```

### 2. Subject-Based Filtering
Only process emails with specific words in subject.

**How to enable:** Edit `config.py`
```python
# Only process invoices
FILTER_SUBJECT = 'Invoice'

# Only process orders
FILTER_SUBJECT = 'Order'

# Process all emails
FILTER_SUBJECT = None
```

---

## 🧗 Challenge Faced

**Problem:** Emails have complex formats (HTML, plain text, attachments)

Gmail stores email bodies in different parts:
- Some emails = plain text only
- Some emails = HTML only
- Some emails = both + attachments

**Solution:**
- Check if email has multiple parts
- Look for `text/plain` type
- Decode from base64
- Handle nested parts (recursion)
- Limit to 50,000 characters (Google Sheets limit)

Code in `email_parser.py` → `_get_body()` method

---

## ⚠️ Limitations

1. **Max 100 emails per run**
   - Gmail API default limit
   - Solution: Run script multiple times

2. **No concurrent runs**
   - Running twice at same time = possible duplicates
   - Solution: Use cron/scheduler

3. **Email body truncated at 50,000 chars**
   - Google Sheets cell limit
   - Long emails will be cut off

4. **State file grows with emails**
   - 1000 emails = ~50KB state file
   - Not a problem unless millions of emails

---

## 🧪 Testing Duplicate Prevention

1. Run script once:
   ```bash
   python main.py
   ```

2. Check Google Sheet - emails appear

3. Run script again (without new emails):
   ```bash
   python main.py
   ```

4. Check logs - should say:
   ```
   ⏭️  Skipping already processed: msg_...
   ℹ️  No new emails to add
   ```

5. Check Google Sheet - NO duplicates

---

## 📸 Proof of Execution

See `proof/` folder for:
- Gmail inbox screenshots
- Google Sheet with data
- OAuth consent screens
- Demo video

---

## 🔧 Troubleshooting

**"credentials.json not found"**
→ Put file in `credentials/` folder

**"SPREADSHEET_ID not found"**
→ Update in `config.py`

**OAuth error**
→ Make sure Gmail & Sheets APIs are enabled
→ Add yourself as test user in Google Console

---

**Submission:** [Date]  
**Repository:** [GitHub Link]
