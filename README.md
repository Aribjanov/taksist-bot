 Taxi VIP Bot
Taxi VIP Bot — bu Telegram uchun mo‘ljallangan avtomatlashtirilgan tizim bo‘lib, u turli guruhlardan yo‘lovchi e’lonlarini yig‘adi, tahlil qiladi va taksistlarga qulay tarzda yetkazib beradi. Tizim VIP obuna asosida ishlaydi va taksistlarga mijozlar bilan to‘g‘ridan-to‘g‘ri bog‘lanish imkoniyatini taqdim etadi.

📌 Asosiy xususiyatlar
✅ Guruhlardan xabarlarni avtomatik yig‘ish – bot qo‘shilgan barcha guruhlardagi xabarlarni real vaqtda tahlil qiladi.

✅ Aqlli parser – shahar nomlari (hatto noto‘g‘ri yozilganlarini ham), vaqt, sana, yo‘lovchilar soni, telefon raqam va usernameni aniqlaydi.

✅ Ikkita kanalga yuborish:

Umumiy kanal – barcha foydalanuvchilar ko‘radi (aloqa maʼlumotlari yashirilgan).

VIP kanal – faqat VIP obunachilar ko‘radi (to‘liq aloqa maʼlumotlari bilan).

✅ VIP obuna tizimi – foydalanuvchilar obuna orqali mijoz maʼlumotlariga to‘liq kirish huquqini oladi.

✅ Admin panel – foydalanuvchilarni boshqarish, statistikani ko‘rish va obuna berish.

✅ Avtomatik eslatmalar – obuna tugashiga 5, 3 va 1 kun qolganda xabar yuboradi.

✅ Start tugmasi – /start buyrug‘i uchun alohida tugma mavjud.

✅ Barcha foydalanuvchilar uchun avtomatik VIP (sinov davri) – botga /start bosgan har bir foydalanuvchiga 30 kunlik bepul VIP obuna beriladi va ularga guruh linklari yuboriladi.

🛠 Texnologiyalar
Python 3.10+

aiogram 3.x – Telegram Bot API uchun

aiosqlite – asinxron SQLite ishlatish uchun

python-dotenv – muhit o‘zgaruvchilarni boshqarish

📁 Loyiha tuzilishi
text
taxi-vip-bot/
│
├── .env                      # Muhit o‘zgaruvchilari
├── bot.py                    # Botni ishga tushirish fayli
├── config.py                 # Konfiguratsiya
├── database.py               # Baza yaratish va so‘rovlar
├── requirements.txt          # Kutubxonalar ro‘yxati
├── README.md                 # Loyiha haqida maʼlumot
│
├── handlers/                 # Barcha handlerlar
│   ├── __init__.py
│   ├── start.py              # /start buyrug‘i
│   ├── profile.py            # Profil yaratish va ko‘rish
│   ├── group.py              # Guruhlardan xabar olish
│   ├── callback.py           # Inline tugmalar
│   ├── admin.py              # Admin panel
│   └── subscription.py       # Obuna holati
│
├── keyboards/                # Klaviatura tugmalari
│   ├── __init__.py
│   ├── main_menu.py          # Asosiy menyu
│   ├── admin_menu.py         # Admin menyusi
│   └── inline.py             # Inline tugmalar
│
├── services/                 # Yordamchi xizmatlar
│   ├── __init__.py
│   └── message_parser.py     # Xabarlarni tahlil qilish
│
└── states/                   # FSM holatlari
    ├── __init__.py
    └── profile.py            # Profil holatlari
⚙️ O‘rnatish va sozlash
1. Loyihani klonlash
bash
git clone https://github.com/your-username/taxi-vip-bot.git
cd taxi-vip-bot
2. Virtual muhit yaratish (tavsiya etiladi)
bash
python -m venv venv
source venv/bin/activate      # Linux/Mac
venv\Scripts\activate         # Windows
3. Kutubxonalarni o‘rnatish
bash
pip install -r requirements.txt
4. .env faylini yaratish
Loyiha papkasida .env faylini yarating va quyidagi o‘zgaruvchilarni to‘ldiring:

env
BOT_TOKEN=123456789:AAxxxxxxxxxxxxxxxxxxxxxxxx
ADMIN_IDS=123456789
DB_PATH=taxi_vip_bot.db
VIP_CHAT_ID=-1001234567890
PUBLIC_CHAT_ID=-1009876543210
ADMIN_CONTACT=@admin_username
O‘zgaruvchi	Tavsif
BOT_TOKEN	Telegram bot tokeningiz
ADMIN_IDS	Admin Telegram ID raqamlari (vergul bilan ajratilgan)
DB_PATH	SQLite baza fayli nomi
VIP_CHAT_ID	VIP kanal ID si (manfiy son)
PUBLIC_CHAT_ID	Umumiy kanal ID si (manfiy son)
ADMIN_CONTACT	Admin bilan bog‘lanish uchun kontakt
🚀 Botni ishga tushirish
bash
python bot.py
Agar hammasi to‘g‘ri bo‘lsa, terminalda quyidagi xabar chiqadi:

text
✅ Imports muvaffaqiyatli
📊 Bazani yaratish...
✅ Database tayyor
🚕 Taxi VIP Bot ishga tushdi!
📱 Botdan foydalanish
Taksist uchun:
Botga /start yuboring.

Avtomatik ravishda 30 kunlik VIP obuna olasiz va guruh linklari yuboriladi.

Asosiy menyu orqali profilingizni to‘ldiring.

Guruhlarga yo‘lovchi e’lonlari yozilsa, bot ularni tahlil qilib, kanallarga yuboradi.

Umumiy kanalda e’lonni ko‘rasiz. “Mijozni olish” tugmasini bosing:

VIP bo‘lsangiz – VIP kanal havolasi chiqadi.

VIP bo‘lmasangiz – obuna taklifi chiqadi.

VIP kanalda mijozning telefon raqami, username yoki profili havolasi ko‘rsatiladi.

“Mijoz bilan bog‘lanish” tugmasi orqali to‘liq aloqa maʼlumotlarini olasiz.

Admin uchun:
Admin menyusi orqali:

📋 Mijozlar – barcha mijozlar ro‘yxati.

📊 Statistika – taksistlar, VIPlar, guruhlar soni.

🔗 Guruhlarni boshqarish – qo‘shimcha sozlamalar.

⭐ VIP obuna – foydalanuvchilarga VIP obuna berish.

📦 Hammasini VIP qilish – barcha foydalanuvchilarni VIP qilish (sinov uchun).

🔐 Xavfsizlik va cheklovlar
Bot faqat ishonchli guruhlarda ishlatilishi tavsiya etiladi.

Foydalanuvchi maʼlumotlari (telefon, username) faqat VIP obunachilarga ko‘rsatiladi.

Admin huquqlari faqat .env dagi ADMIN_IDS ga ega foydalanuvchilarga beriladi.

🧪 Sinov davri uchun maxsus sozlamalar
handlers/start.py da barcha foydalanuvchilarga avtomatik 30 kunlik VIP obuna beriladi. Bu sizga taksistlarni tez yig‘ish imkonini beradi. Sinov davri tugagach, ushbu qismni o‘chirib qo‘yishingiz mumkin.

🌐 Joylashtirish (Deployment)
Botni doimiy ishlash uchun serverga joylashtirish tavsiya etiladi:

Oracle Cloud (Always Free) – eng ishonchli va quvvatli variant.

Render.com – oson va tez, lekin uyqu holatiga o‘tishi mumkin.

Railway / Heroku – boshqa mashhur platformalar.

Deploy qilish uchun asosiy buyruqlar:
bash
# Oracle Cloud / VPS da
sudo apt update
sudo apt install python3-pip
pip install -r requirements.txt
python bot.py
Doimiy ishlatish uchun screen yoki systemd dan foydalaning.

🤝 Hissa qo‘shish
Loyihani yaxshilashga hissa qo‘shmoqchi bo‘lsangiz:

Fork qiling.

O‘zgarishlarni qo‘shing.

Pull request yuboring.

📄 Litsenziya
Ushbu loyiha MIT litsenziyasi asosida tarqatiladi. Siz uni erkin foydalanishingiz, o‘zgartirishingiz va tarqatishingiz mumkin.

👨‍💻 Muallif
Ismingiz / Username
Telegram: @username
GitHub: github.com/your-username

🌟 Qo‘llab-quvvatlash
Agar loyiha sizga foydali bo‘lsa, ⭐ bosing va do‘stlaringiz bilan ulashing!

📌 Eslatma: Loyiha doimiy ravishda takomillashtirilmoqda. Yangi funksiyalar va yaxshilanishlar uchun repository’ni kuzatib boring.

