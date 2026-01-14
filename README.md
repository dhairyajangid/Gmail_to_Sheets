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
1. Go to the google cloud console make the project name whatever you like.
2. Then enable the api by searching Gmail API and Google Sheets API.
3. Then create OAuth client ID there you find the json file to download ` it's client secret `
4. Put it in: `credentials/credentials.json` you can rename the json file to credentials.json.
5. In google cloud project go to Audience section to add test
6. You will see there test user you need to add your gmail there from which you will parser the emails and show it on sheets.

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
### Proof of Work
---
**Following error can occur if you not add the gmail in test user**
<img width="1604" height="597" alt="Screenshot 2026-01-14 215118" src="https://github.com/user-attachments/assets/b39d359e-8ea7-4560-8dea-98aa79f0644d" />
**make sure to add gmail here**
<img width="1918" height="852" alt="image" src="https://github.com/user-attachments/assets/2ac31145-5f83-4bc8-a9c9-8840124c4ad1" />

- After this run the program again if you face this error
- then you will see web page open there gonna be some mail select one that you put it in the test user section.
- then there will be this thing pop up
- <img width="1919" height="939" alt="Screenshot 2026-01-14 221149" src="https://github.com/user-attachments/assets/7f0373f1-e549-4cd4-bc33-9fbd7e42f2da" />
- click on continue then it will show this
- <img width="1919" height="933" alt="Screenshot 2026-01-14 221346" src="https://github.com/user-attachments/assets/8d856cb0-6a86-4976-92df-695e5668603b" />
- it means your project start and parser you mail
- <img width="1826" height="907" alt="Screenshot 2026-01-14 225912" src="https://github.com/user-attachments/assets/674283e9-80d4-4a29-98ef-932f22a82d3f" />
**It will take time at first to run then your google sheet looks like this** 
<img width="1919" height="940" alt="Screenshot 2026-01-14 225725" src="https://github.com/user-attachments/assets/76706db0-9a96-4609-8fe6-b47f9f457c61" />

---

