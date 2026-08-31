from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

def admin_menu() -> ReplyKeyboardMarkup:
    keyboard = [
        [KeyboardButton(text="📋 Mijozlar"), KeyboardButton(text="📊 Statistika")],
        [KeyboardButton(text="🔗 Guruhlarni boshqarish"), KeyboardButton(text="⭐ VIP obuna")],
        [KeyboardButton(text="⬅️ Asosiy menyu")],
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)