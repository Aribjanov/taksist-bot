from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
import aiosqlite

from config import DB_PATH, ADMIN_CONTACT, VIP_CHAT_ID

router = Router()

@router.callback_query(F.data.startswith("get_contact_"))
async def get_contact_public(callback: CallbackQuery):
    user_id = callback.from_user.id
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "SELECT status FROM subscriptions WHERE telegram_id = ? AND status = 'active'",
            (user_id,)
        )
        row = await cursor.fetchone()

    if row:
        # VIP – VIP kanalga havola
        await callback.message.answer(
            f"✅ Siz VIP obunachisiz!\n\n"
            f"🔗 Mijoz bilan bog‘lanish uchun VIP kanalga o‘ting:\n"
            f"https://t.me/your_vip_channel",  # O'z kanalingiz linki
            parse_mode="HTML"
        )
        await callback.answer()
    else:
        # VIP emas – alert va obuna taklifi
        await callback.answer(
            "❌ Siz VIP obunaga ega emassiz!\n"
            "Mijoz bilan bog‘lanish uchun VIP kanalga a'zo bo'ling!",
            show_alert=True
        )
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="⭐ VIP obuna bo‘lish", callback_data="subscribe_now")]
        ])
        await callback.message.answer(
            "⭐ VIP obuna orqali mijozning telefon raqami, username yoki profiliga kirishingiz mumkin.\n\n"
            "Obuna bo‘lish uchun admin bilan bog‘laning:",
            reply_markup=keyboard,
            parse_mode="HTML"
        )
        await callback.answer()

@router.callback_query(F.data == "admin_contact")
async def admin_contact(callback: CallbackQuery):
    await callback.message.answer(
        f"👤 <b>Admin bilan bog‘lanish</b>\n\n📩 {ADMIN_CONTACT}",
        parse_mode="HTML"
    )
    await callback.answer()

@router.callback_query(F.data.startswith("contact_vip_"))
async def contact_vip(callback: CallbackQuery):
    user_id = callback.from_user.id
    # VIPmi tekshirish
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "SELECT status FROM subscriptions WHERE telegram_id = ? AND status = 'active'",
            (user_id,)
        )
        row = await cursor.fetchone()

    if not row:
        await callback.answer("❌ Siz VIP obunaga ega emassiz!", show_alert=True)
        return

    # Ma'lumotni olish
    parts = callback.data.split("_")
    chat_id = int(parts[2])
    msg_id = int(parts[3])

    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "SELECT phone, username, telegram_id FROM clients WHERE source_chat_id = ? AND source_message_id = ?",
            (chat_id, msg_id)
        )
        client_row = await cursor.fetchone()

    if not client_row:
        await callback.answer("❌ Mijoz ma'lumoti topilmadi.", show_alert=True)
        return

    phone = client_row[0]
    username = client_row[1]
    client_telegram_id = client_row[2]

    response = "📞 <b>Mijoz bilan bog‘lanish</b>\n\n"
    if phone:
        response += f"📱 Telefon: <code>{phone}</code>\n"
    if username:
        response += f"👤 Username: {username}\n"
    if not phone and not username and client_telegram_id:
        response += f"🔗 <a href='tg://user?id={client_telegram_id}'>Mijoz profili</a>\n"
    if not phone and not username and not client_telegram_id:
        response += "❌ Aloqa ma'lumoti mavjud emas."

    await callback.message.answer(response, parse_mode="HTML")
    await callback.answer()

@router.callback_query(F.data == "subscribe_now")
async def subscribe_now(callback: CallbackQuery):
    await callback.message.answer(
        f"⭐ <b>VIP obuna</b>\n\nObuna bo‘lish uchun admin bilan bog‘laning:\n{ADMIN_CONTACT}",
        parse_mode="HTML"
    )
    await callback.answer()