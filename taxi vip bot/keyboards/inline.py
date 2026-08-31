from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def public_buttons(chat_id: int, message_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="📞 Mijozni olish", callback_data=f"get_contact_{chat_id}_{message_id}"),
            InlineKeyboardButton(text="👤 Admin bilan bog‘lanish", callback_data="admin_contact")
        ]
    ])

def vip_buttons(chat_id: int, message_id: int, client_telegram_id: int = None) -> InlineKeyboardMarkup:
    # Agar mijozning Telegram ID si ma'lum bo'lsa, tugma profilga havola bo'ladi
    if client_telegram_id:
        url = f"tg://user?id={client_telegram_id}"
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📞 Mijoz bilan bog‘lanish", url=url)]
        ])
    else:
        # Aks holda callback_data orqali ma'lumot chiqarish
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📞 Mijoz bilan bog‘lanish", callback_data=f"contact_vip_{chat_id}_{message_id}")]
        ])