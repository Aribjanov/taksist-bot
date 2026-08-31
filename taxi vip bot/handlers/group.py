from aiogram import Router, F
from aiogram.types import Message
from aiogram.enums import ChatType
from aiogram.exceptions import TelegramBadRequest
import aiosqlite

from config import DB_PATH, VIP_CHAT_ID, PUBLIC_CHAT_ID
from services.message_parser import parse_trip_message
from keyboards.inline import public_buttons, vip_buttons

router = Router()

@router.message(F.chat.type.in_({ChatType.GROUP, ChatType.SUPERGROUP}))
async def handle_group_message(message: Message):
    chat_id = message.chat.id
    print(f"📩 Guruhdan xabar keldi: {chat_id}")

    if not message.text:
        return

    parsed = parse_trip_message(message.text)

    if not parsed['from_city'] and not parsed['to_city']:
        print(f"ℹ️ Shaharlar topilmadi: {message.text[:50]}")
        return

    if not parsed['from_city']:
        parsed['from_city'] = "Noma'lum"
    if not parsed['to_city']:
        parsed['to_city'] = "Noma'lum"

    print(f"✅ Shaharlar: {parsed['from_city']} → {parsed['to_city']}")

    # Umumiy kanal uchun matn
    public_caption = (
        f"🚕 <b>Yangi yo'lovchi</b>\n\n"
        f"📍 <b>Qayerdan:</b> {parsed['from_city']}\n"
        f"📍 <b>Qayerga:</b> {parsed['to_city']}\n"
    )
    if parsed.get('date'):
        public_caption += f"📅 <b>Sana:</b> {parsed['date']}\n"
    if parsed.get('time'):
        public_caption += f"🕐 <b>Vaqt:</b> {parsed['time']}\n"
    if parsed.get('passengers'):
        public_caption += f"👥 <b>Yo'lovchilar:</b> {parsed['passengers']} kishi\n"
    public_caption += "\n🔒 <i>Aloqa ma'lumotlari faqat VIP obunachilar uchun</i>"

    # VIP kanal uchun matn
    vip_caption = (
        f"🚕 <b>Yangi yo'lovchi (VIP)</b>\n\n"
        f"📍 <b>Qayerdan:</b> {parsed['from_city']}\n"
        f"📍 <b>Qayerga:</b> {parsed['to_city']}\n"
    )
    if parsed.get('date'):
        vip_caption += f"📅 <b>Sana:</b> {parsed['date']}\n"
    if parsed.get('time'):
        vip_caption += f"🕐 <b>Vaqt:</b> {parsed['time']}\n"
    if parsed.get('passengers'):
        vip_caption += f"👥 <b>Yo'lovchilar:</b> {parsed['passengers']} kishi\n"
    
    # Aloqa ma'lumotlari
    contact_info = []
    client_telegram_id = message.from_user.id  # mijozning ID si
    if parsed.get('phone'):
        contact_info.append(f"📞 Telefon: <code>{parsed['phone']}</code>")
    if parsed.get('username'):
        contact_info.append(f"👤 Username: {parsed['username']}")
    if not contact_info:
        contact_info.append(f"🔗 <a href='tg://user?id={client_telegram_id}'>Mijoz profili</a>")
    vip_caption += "\n" + "\n".join(contact_info)

    # Yuborish
    try:
        await message.bot.send_message(
            chat_id=PUBLIC_CHAT_ID,
            text=public_caption,
            parse_mode="HTML",
            reply_markup=public_buttons(chat_id, message.message_id)
        )
        print(f"✅ Umumiy kanalga yuborildi: {PUBLIC_CHAT_ID}")

        await message.bot.send_message(
            chat_id=VIP_CHAT_ID,
            text=vip_caption,
            parse_mode="HTML",
            reply_markup=vip_buttons(chat_id, message.message_id, client_telegram_id)
        )
        print(f"✅ VIP kanalga yuborildi: {VIP_CHAT_ID}")
    except TelegramBadRequest as e:
        print(f"❌ Xatolik: {e}")

    # Mijozni bazaga saqlash
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            """INSERT INTO clients (source_chat_id, source_message_id, text, from_location, to_location, phone, username, telegram_id)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (chat_id, message.message_id, message.text, parsed['from_city'], parsed['to_city'],
             parsed.get('phone'), parsed.get('username'), message.from_user.id)
        )
        await db.commit()
        print("✅ Mijoz bazaga saqlandi")