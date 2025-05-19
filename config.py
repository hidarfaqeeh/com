import os

BOT_TOKEN = os.getenv("BOT_TOKEN", "7533295302:AAEgqpo4SXf0K5IH4bFTWfNZc5LSxMcHE4E")
ADMIN_IDS = os.getenv("ADMIN_IDS", "6194809472").split(",")
EVENTS_CHANNEL = os.getenv("LOG_CHANNEL_ID", "-1001861242334")  # مطابق للبيئة
COMP_CHANNELS = [
    channel.strip() for channel in os.getenv("MANDATORY_CHANNELS", "@yepoets,@SSOUND_AAESA_AALAYATH").split(",")
]
COMPETITION_END = os.getenv("CONTEST_END_TIMESTAMP", "2025-06-01T23:59:59")
REFERRAL_POINTS = int(os.getenv("REFERRAL_POINTS", "100"))
TOP_LIMIT = int(os.getenv("TOP_LIMIT", "10"))
BOT_USERNAME = os.getenv("BOT_USERNAME", "Competyebot")
