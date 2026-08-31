from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
import aiosqlite
from config import DB_PATH
from states.profile import ProfileState
from keyboards.main_menu import main_menu

router = Router()

@router.message(F.text == "👤 Mening profilim")
async def show_profile(message: Message, state: FSMContext):
    telegram_id = message.from_user.id
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "SELECT full_name, phone, car_model, car_number FROM users WHERE telegram_id = ?",
            (telegram_id,)
        )
        row = await cursor.fetchone()
    if row and row[0] and row[1] and row[2] and row[3]:
        text = (
            f"👤 <b>Sizning profilingiz</b>\n\n"
            f"📌 Ism: {row[0]}\n"
            f"📞 Telefon: {row[1]}\n"
            f"🚗 Mashina modeli: {row[2]}\n"
            f"🔢 Davlat raqami: {row[3]}"
        )
        await message.answer(text, reply_markup=main_menu(message.from_user.id))
    else:
        await state.set_state(ProfileState.waiting_for_full_name)
        await message.answer("✏️ Iltimos, to‘liq ismingizni kiriting:", reply_markup=ReplyKeyboardRemove())

@router.message(ProfileState.waiting_for_full_name)
async def process_full_name(message: Message, state: FSMContext):
    await state.update_data(full_name=message.text)
    await state.set_state(ProfileState.waiting_for_phone)
    await message.answer("📞 Telefon raqamingizni kiriting (masalan: +998901234567):")

@router.message(ProfileState.waiting_for_phone)
async def process_phone(message: Message, state: FSMContext):
    await state.update_data(phone=message.text)
    await state.set_state(ProfileState.waiting_for_car_model)
    await message.answer("🚗 Mashina modelingizni kiriting (masalan: Chevrolet Cobalt):")

@router.message(ProfileState.waiting_for_car_model)
async def process_car_model(message: Message, state: FSMContext):
    await state.update_data(car_model=message.text)
    await state.set_state(ProfileState.waiting_for_car_number)
    await message.answer("🔢 Davlat raqamini kiriting (masalan: 01 A 123 AA):")

@router.message(ProfileState.waiting_for_car_number)
async def process_car_number(message: Message, state: FSMContext):
    data = await state.get_data()
    full_name = data.get("full_name")
    phone = data.get("phone")
    car_model = data.get("car_model")
    car_number = message.text
    telegram_id = message.from_user.id
    username = message.from_user.username
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            """INSERT INTO users (telegram_id, username, full_name, phone, car_model, car_number)
               VALUES (?, ?, ?, ?, ?, ?)
               ON CONFLICT(telegram_id) DO UPDATE SET
               username = excluded.username,
               full_name = excluded.full_name,
               phone = excluded.phone,
               car_model = excluded.car_model,
               car_number = excluded.car_number""",
            (telegram_id, username, full_name, phone, car_model, car_number)
        )
        await db.commit()
    await state.clear()
    await message.answer("✅ Profilingiz muvaffaqiyatli saqlandi!", reply_markup=main_menu(message.from_user.id))