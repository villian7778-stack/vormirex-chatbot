# import gspread
# from google.oauth2.service_account import Credentials
# from datetime import datetime
# from backend.config import GOOGLE_SHEET_NAME


# def save_lead(name, phone, message):
#     scopes = [
#         "https://www.googleapis.com/auth/spreadsheets",
#         "https://www.googleapis.com/auth/drive"
#     ]

#     creds = Credentials.from_service_account_file(
#         "credentials/service_account.json",
#         scopes=scopes
#     )

#     client = gspread.authorize(creds)
#     sheet = client.open(GOOGLE_SHEET_NAME).sheet1

#     sheet.append_row([
#         datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#         name,
#         phone,
#         message
#     ])


# from datetime import datetime
# import gspread
# from google.oauth2.service_account import Credentials
# from backend.config import GOOGLE_SHEET_ID, GOOGLE_CREDS_FILE



# def save_lead(name: str, phone: str, source: str, course: str = "Not Selected"):
#     scopes = ["https://www.googleapis.com/auth/spreadsheets"]
#     creds = Credentials.from_service_account_file(
#         GOOGLE_CREDS_FILE, scopes=scopes
#     )
#     client = gspread.authorize(creds)

#     sheet = client.open_by_key(GOOGLE_SHEET_ID).sheet1

#     sheet.append_row([
#         datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#         name,
#         phone,
#         source,
#         course
#     ])

#     print("✅ Lead saved:", name, phone, "Course:", course)

# from datetime import datetime
# import gspread
# from google.oauth2.service_account import Credentials
# from backend.config import GOOGLE_SHEET_ID, GOOGLE_CREDS_FILE


# def save_lead(
#     *,
#     name: str,
#     phone: str,
#     source: str,
#     course: str = "Not Selected"
# ):
#     """
#     Keyword-only arguments enforced using '*'
#     This prevents source & course mix-up forever.
#     """

#     scopes = ["https://www.googleapis.com/auth/spreadsheets"]
#     creds = Credentials.from_service_account_file(
#         GOOGLE_CREDS_FILE, scopes=scopes
#     )
#     client = gspread.authorize(creds)

#     sheet = client.open_by_key(GOOGLE_SHEET_ID).sheet1

#     sheet.append_row([
#         datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#         name,
#         phone,
#         source,
#         course
#     ])

#     print(f"✅ Lead saved | Name={name}, Phone={phone}, Source={source}, Course={course}")

# from datetime import datetime
# import gspread
# from google.oauth2.service_account import Credentials
# from backend.config import GOOGLE_SHEET_ID, GOOGLE_CREDS_FILE


# def save_lead(*, name: str, phone: str, source: str, course: str = "Not Selected"):
#     scopes = ["https://www.googleapis.com/auth/spreadsheets"]
#     creds = Credentials.from_service_account_file(
#         GOOGLE_CREDS_FILE, scopes=scopes
#     )
#     client = gspread.authorize(creds)

#     sheet = client.open_by_key(GOOGLE_SHEET_ID).sheet1

#     sheet.append_row([
#         datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#         name,
#         phone,
#         source,
#         course
#     ])

#     print(f"✅ Lead saved → Name: {name}, Phone: {phone}, Source: {source}, Course: {course}")



from datetime import datetime
import os
import json
import gspread
from google.oauth2.service_account import Credentials

# ========================
# ENV SETUP
# ========================

# Load .env only in local
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

ENVIRONMENT = os.getenv("ENVIRONMENT", "local").lower()
IS_LOCAL = ENVIRONMENT in ["local", "dev", "development"]

print(f"🔧 Google Sheets Environment: {ENVIRONMENT}")

# ========================
# CONFIG
# ========================

SHEET_ID = os.getenv("GOOGLE_SHEET_ID")
SHEET_NAME = os.getenv("GOOGLE_SHEET_NAME", "vormirex_leads")
SERVICE_ACCOUNT_JSON = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")

BACKUP_FILE = "leads_backup.json"

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

# ========================
# GOOGLE SHEETS INIT
# ========================

GOOGLE_SHEETS_ENABLED = True
GSPREAD_CLIENT = None

try:
    if not SERVICE_ACCOUNT_JSON:
        raise RuntimeError("GOOGLE_SERVICE_ACCOUNT_JSON not found")

    service_account_info = json.loads(SERVICE_ACCOUNT_JSON)

    # Fix multiline private key
    service_account_info["private_key"] = (
        service_account_info["private_key"]
        .replace("\\n", "\n")
        .strip()
    )

    creds = Credentials.from_service_account_info(
        service_account_info,
        scopes=SCOPES
    )

    GSPREAD_CLIENT = gspread.authorize(creds)
    print("✅ Google Sheets authenticated")

except Exception as e:
    GOOGLE_SHEETS_ENABLED = False
    print(f"⚠️ Google Sheets disabled: {e}")

# ========================
# BACKUP FUNCTIONS
# ========================

def save_to_backup(name, phone, source, course):
    """Always save locally as backup"""
    try:
        data = []
        if os.path.exists(BACKUP_FILE):
            with open(BACKUP_FILE, "r") as f:
                data = json.load(f)

        data.append({
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "name": name,
            "phone": phone,
            "source": source,
            "course": course,
        })

        with open(BACKUP_FILE, "w") as f:
            json.dump(data, f, indent=2)

        print(f"💾 Backup saved for {name}")
        return True

    except Exception as e:
        print(f"❌ Backup failed: {e}")
        return False

# ========================
# WORKSHEET HANDLING
# ========================

def ensure_worksheet_exists():
    """Create worksheet in LOCAL if missing"""
    spreadsheet = GSPREAD_CLIENT.open_by_key(SHEET_ID)

    for ws in spreadsheet.worksheets():
        if ws.title.lower() == SHEET_NAME.lower():
            return ws

    if IS_LOCAL:
        print(f"➕ Creating worksheet: {SHEET_NAME}")
        sheet = spreadsheet.add_worksheet(
            title=SHEET_NAME,
            rows=1000,
            cols=5
        )
        sheet.update(
            "A1:E1",
            [["Timestamp", "Name", "Phone", "Source", "Course"]]
        )
        return sheet

    raise RuntimeError("Worksheet not found in production")

# ========================
# MAIN FUNCTION
# ========================

def save_lead(*, name: str, phone: str, source: str, course: str = "Not Selected"):
    """
    Save lead to Google Sheets with safe fallback
    """

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    google_saved = False

    # ---- GOOGLE SHEETS ----
    if GOOGLE_SHEETS_ENABLED and SHEET_ID:
        try:
            print(f"📝 Saving lead: {name}")

            spreadsheet = GSPREAD_CLIENT.open_by_key(SHEET_ID)

            if IS_LOCAL:
                sheet = ensure_worksheet_exists()
            else:
                sheet = spreadsheet.worksheet(SHEET_NAME)

            sheet.append_row([
                timestamp,
                name,
                phone,
                source,
                course
            ])

            print("✅ Saved to Google Sheets")
            google_saved = True

        except Exception as e:
            print(f"⚠️ Google Sheets error: {e}")

    else:
        print("⚠️ Google Sheets not enabled")

    # ---- BACKUP (ALWAYS) ----
    backup_saved = save_to_backup(name, phone, source, course)

    # ---- STATUS LOG ----
    if google_saved and backup_saved:
        print("✅ Status: Google Sheets ✓ | Backup ✓\n")
    elif backup_saved:
        print("⚠️ Status: Google Sheets ✗ | Backup ✓\n")
    else:
        print("❌ Status: Both failed\n")
