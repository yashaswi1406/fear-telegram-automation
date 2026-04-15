import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
from config import GOOGLE_CREDS

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_dict(GOOGLE_CREDS, scope)
client = gspread.authorize(creds)

sheet = client.open("Telegram Leads").sheet1


def get_all_users():
    return sheet.get_all_records()


def already_contacted(user_id):
    try:
        records = get_all_users()
        for row in records:
            if str(row.get("User ID", "")) == str(user_id):
                return True
        return False
    except Exception as e:
        print(f"Error checking already_contacted: {e}")
        return False


def save_user(user, message_text):
    sheet.append_row([
        user.first_name,           # Name
        user.username,             # Username
        user.id,                   # User ID
        "Yes",                     # Message Sent
        "No",                      # Replied
        "Messaged",                # Status
        str(datetime.now()),       # Last Contact
        ""                         # Notes
    ])


def mark_replied(user_id):
    try:
        records = sheet.get_all_records()
        for i, row in enumerate(records, start=2):
            if str(row.get("User ID", "")) == str(user_id):
                sheet.update_cell(i, 5, "Yes")   # Replied
                sheet.update_cell(i, 6, "Responded")
                break
    except Exception as e:
        print(f"Error marking replied: {e}")