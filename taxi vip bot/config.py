import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
DB_PATH = os.getenv("DB_PATH", "taxi_vip_bot.db")
VIP_CHAT_ID = int(os.getenv("VIP_CHAT_ID", 0))
PUBLIC_CHAT_ID = int(os.getenv("PUBLIC_CHAT_ID", 0))
VIP_CHANNEL_LINK = os.getenv("VIP_CHANNEL_LINK", "")
PUBLIC_CHANNEL_LINK = os.getenv("PUBLIC_CHANNEL_LINK", "")
ADMIN_CONTACT = os.getenv("ADMIN_CONTACT", "@admin")
ADMIN_IDS = [
    int(admin_id.strip())
    for admin_id in os.getenv("ADMIN_IDS", "").split(",")
    if admin_id.strip()
]

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN .env faylida topilmadi!")
if not ADMIN_IDS:
    raise ValueError("ADMIN_IDS .env faylida topilmadi!")
if not VIP_CHAT_ID:
    raise ValueError("VIP_CHAT_ID .env faylida topilmadi!")
if not PUBLIC_CHAT_ID:
    raise ValueError("PUBLIC_CHAT_ID .env faylida topilmadi!")
if not VIP_CHANNEL_LINK:
    raise ValueError("VIP_CHANNEL_LINK .env faylida topilmadi!")
if not PUBLIC_CHANNEL_LINK:
    raise ValueError("PUBLIC_CHANNEL_LINK .env faylida topilmadi!")