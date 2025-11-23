import os
from dotenv import load_dotenv

load_dotenv()

STREAK_HIGHLIGHT = os.getenv("STREAK_HIGHLIGHT", "#BDFC93")  # Light yellow

# Database path
DB_PATH = os.getenv("DB_PATH", "loyalty.db")

# Reward thresholds
REWARD_VISITS = int(os.getenv("REWARD_VISITS", "4"))

# Admin credentials (3 admins from .env)
ADMINS = {}
for i in range(1, 4):
    cred = os.getenv(f"ADMIN{i}")
    if cred:
        user, pw = cred.split(":")
        ADMINS[user] = pw

# Feature toggles
SHOW_EMAILS = os.getenv("SHOW_EMAILS", "true").lower() == "true"
