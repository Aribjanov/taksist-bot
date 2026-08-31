from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime, timedelta
import aiosqlite

from config import DB_PATH, VIP_CHANNEL_LINK, PUBLIC_CHANNEL_LINK
from keyboards.main_menu import main_menu

router = Router()

@router.message(CommandStart())
async def start_handler(message: Message):
    user_id = message.from_user.id
    username = message.from_user.username or ""

    # 1. Foydalanuvchini `users` jadvaliga qo'shish
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT OR IGNORE INTO users (telegram_id, username) VALUES (?, ?)",
            (user_id, username)
        )
        await db.commit()

    # 2. Avtomatik VIP obuna berish (30 kun)
    start_date = datetime.now()
    end_date = start_date + timedelta(days=30)

    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "SELECT status, end_date FROM subscriptions WHERE telegram_id = ? ORDER BY id DESC LIMIT 1",
            (user_id,)
        )
        row = await cursor.fetchone()

        if not row or row[0] != 'active' or datetime.fromisoformat(row[1]) < datetime.now():
            await db.execute(
                """INSERT INTO subscriptions (telegram_id, status, start_date, end_date, last_notification_day)
                   VALUES (?, 'active', ?, ?, 0)""",
                (user_id, start_date.isoformat(), end_date.isoformat())
            )
            await db.commit()
            vip_status = "🎉 <b>Tabriklaymiz!</b>\n\nSizga <b>30 kunlik VIP obuna</b> bepul berildi!\n"
        else:
            remaining = (datetime.fromisoformat(row[1]) - datetime.now()).days
            vip_status = f"✅ Siz allaqachon VIP obunachisiz!\n⏳ Tugashiga {remaining} kun qoldi.\n"

    # 3. Guruhlarga qo'shilish linklari
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔗 VIP kanalga qo'shilish", url=VIP_CHANNEL_LINK)],
        [InlineKeyboardButton(text="🔗 Umumiy kanalga qo'shilish", url=PUBLIC_CHANNEL_LINK)]
    ])

    # 4. Xabar matni
    text = (
        f"{vip_status}\n"
        f"📅 Tugash sanasi: {end_date.strftime('%d.%m.%Y')}\n\n"
        "Quyidagi tugmalar orqali guruhlarga qo'shiling:\n"
        "🔹 VIP kanal – mijozlar bilan bog‘lanish uchun\n"
        "🔹 Umumiy kanal – barcha e'lonlarni ko‘rish uchun"
    )

    await message.answer(text, parse_mode="HTML", reply_markup=keyboard)

    # 5. Asosiy menyuni ko'rsatish
    await message.answer(
        "🚕 <b>Assalomu alaykum!</b>\n\n"
        "🇺🇿 O‘zbekiston Taxi VIP botiga xush kelibsiz!\n\n"
        "Quyidagi menyudan kerakli bo‘limni tanlang:",
        reply_markup=main_menu(message.from_user.id)
    )