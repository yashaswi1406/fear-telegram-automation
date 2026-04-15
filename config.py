import os
import json

API_ID = 34368477
API_HASH = "2fc3a434abba372ee86d42c6277fb636"

DAILY_LIMIT = 30

KEYWORDS = [
    "website",
    "web development",
    "app",
    "automation",
    "ai",
    "chatbot",
    "seo"
]

# ✅ Load from GitHub Secret
GOOGLE_CREDS = json.loads(os.getenv("GOOGLE_CREDS"))
