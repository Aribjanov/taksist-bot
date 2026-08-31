from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from config import ADMIN_IDS

def main_menu(telegram_id: int = None) -> ReplyKeyboardMarkup:
    is_admin = telegram_id in ADMIN_IDS if telegram_id else False

    if is_admin:
        help_button = KeyboardButton(text="👑 Admin paneli")
    else:
        help_button = KeyboardButton(text="ℹ️ Yordam")

    keyboard = [
        [
            KeyboardButton(text="👤 Mening profilim"),
            KeyboardButton(text="⭐ VIP obuna")
        ],
        [
            KeyboardButton(text="📅 Obuna holati"),
            help_button
        ],
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)