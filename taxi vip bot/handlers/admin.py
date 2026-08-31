from aiogram import Router, F
from aiogram.types import Message
from config import ADMIN_IDS, ADMIN_CONTACT
from keyboards.admin_menu import admin_menu
from keyboards.main_menu import main_menu

router = Router()

@router.message(F.text == "👑 Admin paneli")
async def admin_panel(message: Message):
    if message.from_user.id not in ADMIN_IDS:
        await message.answer("❌ Siz admin emassiz.", reply_markup=main_menu(message.from_user.id))
        return
    await message.answer("👑 <b>Admin paneli</b>", reply_markup=admin_menu())

@router.message(F.text == "ℹ️ Yordam")
async def support_handler(message: Message):
    await message.answer(
        f"ℹ️ <b>Yordam</b>\n\n"
        f"Savol yoki muammolar bo‘lsa, admin bilan bog‘laning:\n"
        f"📩 {ADMIN_CONTACT}",
        reply_markup=main_menu(message.from_user.id)
    )

@router.message(F.text == "📋 Mijozlar")
async def admin_clients(message: Message):
    if message.from_user.id not in ADMIN_IDS:
        return
    await message.answer("📋 Mijozlar ro'yxati hozircha mavjud emas.", reply_markup=admin_menu())

@router.message(F.text == "📊 Statistika")
async def admin_stats(message: Message):
    if message.from_user.id not in ADMIN_IDS:
        return
    await message.answer("📊 Statistika hozircha mavjud emas.", reply_markup=admin_menu())

@router.message(F.text == "🔗 Guruhlarni boshqarish")
async def admin_groups(message: Message):
    if message.from_user.id not in ADMIN_IDS:
        return
    await message.answer(
        "🔗 Guruhlarni boshqarish\n\n"
        "Bot hozirda barcha guruhlardan avtomatik xabar oladi.",
        reply_markup=admin_menu()
    )

@router.message(F.text == "⭐ VIP obuna")
async def admin_give_subscription(message: Message):
    if message.from_user.id not in ADMIN_IDS:
        return
    await message.answer(
        "⭐ VIP obuna berish\n\nBu funksiya hozircha ishlamaydi.",
        reply_markup=admin_menu()
    )

@router.message(F.text == "⬅️ Asosiy menyu")
async def back_to_main(message: Message):
    if message.from_user.id not in ADMIN_IDS:
        return
    await message.answer("Asosiy menyu", reply_markup=main_menu(message.from_user.id))