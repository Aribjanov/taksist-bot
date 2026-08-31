import aiosqlite
from config import DB_PATH

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        # 1. Clients (Mijozlar) jadvali
        await db.execute("""
            CREATE TABLE IF NOT EXISTS clients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_chat_id INTEGER,
                source_message_id INTEGER,
                text TEXT,
                from_location TEXT,
                to_location TEXT,
                phone TEXT,
                username TEXT,
                telegram_id INTEGER
            )
        """)

        # 2. Subscriptions (VIP Obunalar) jadvali
        await db.execute("""
            CREATE TABLE IF NOT EXISTS subscriptions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                telegram_id INTEGER,
                status TEXT,
                start_date TEXT,
                end_date TEXT
            )
        """)

        # 3. Payments (To'lovlar) jadvali
        await db.execute("""
            CREATE TABLE IF NOT EXISTS payments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                telegram_id INTEGER,
                amount INTEGER,
                receipt_file_id TEXT,
                status TEXT
            )
        """)

        await db.commit()