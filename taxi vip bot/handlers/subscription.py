from aiogram import Router, F
from aiogram.types import Message
import aiosqlite
from config import DB_PATH
from keyboards.main_menu import main_menu

router = Router()

@router.message(F.text == "📅 Obuna holati")
async def subscription_status(message: Message):
    telegram_id = message.from_user.id
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "SELECT status, end_date FROM subscriptions WHERE telegram_id = ? ORDER BY id DESC LIMIT 1",
            (telegram_id,)
        )
        row = await cursor.fetchone()
    if row and row[0] == "active":
        end_date = row[1] if row[1] else "Noma'lum"
        await message.answer(
            f"📅 <b>Obuna holati</b>\n\n✅ Siz VIP obuna egasisiz!\n⏳ Tugash sanasi: {end_date}",
            reply_markup=main_menu(message.from_user.id),
            parse_mode="HTML"
        )
    else:
        await message.answer(
            "📅 <b>Obuna holati</b>\n\n❌ Siz hali VIP obunaga ega emassiz.",
            reply_markup=main_menu(message.from_user.id),
            parse_mode="HTML"
        )