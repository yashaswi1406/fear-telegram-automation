import os
import json
from dotenv import load_dotenv

# Load .env
load_dotenv()

# Telegram
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")

# Google Sheets
GOOGLE_CREDS = json.loads(os.getenv("GOOGLE_CREDS"))

# Limits
DAILY_LIMIT = 40

# Keywords
KEYWORDS = [
    "website", "web development", "developer",
    "ai", "automation", "bot",
    "marketing", "app", "seo", "ads"
]