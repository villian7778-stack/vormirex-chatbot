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
import gspread
from google.oauth2.service_account import Credentials
from backend.config import GOOGLE_SHEET_ID, GOOGLE_CREDS_FILE

def save_lead(*, name: str, phone: str, source: str, course: str = "Not Selected"):
    """
    Save lead info to Google Sheet
    """
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    creds = Credentials.from_service_account_file(
        GOOGLE_CREDS_FILE, scopes=scopes
    )
    client = gspread.authorize(creds)
    sheet = client.open_by_key(GOOGLE_SHEET_ID).sheet1

    sheet.append_row([
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        name,
        phone,
        source,
        course
    ])

    print(f"✅ Lead saved → Name: {name}, Phone: {phone}, Source: {source}, Course: {course}")
