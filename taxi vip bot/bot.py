import asyncio
import sys
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BotCommand

try:
    from config import BOT_TOKEN
    from database import init_db
    from handlers import router as main_router
    print("✅ Imports muvaffaqiyatli")
except ImportError as e:
    print(f"❌ Import xatolik: {e}")
    sys.exit(1)

dp = Dispatcher()
dp.include_router(main_router)

async def main():
    try:
        print("📊 Bazani yaratish...")
        await init_db()
        print("✅ Database tayyor")

        bot = Bot(
            token=BOT_TOKEN,
            default=DefaultBotProperties(parse_mode=ParseMode.HTML)
        )

        await bot.set_my_commands([
            BotCommand(command="start", description="🚕 Botni ishga tushirish")
        ])

        print("🚕 Taxi VIP Bot ishga tushdi!")
        await dp.start_polling(bot)
    except Exception as e:
        print(f"❌ Xatolik: {e}")
        raise
    finally:
        await bot.session.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("🛑 Bot to‘xtatildi")
    except Exception as e:
        print(f"❌ Asosiy xatolik: {e}")