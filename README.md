# 🚀 Biznes AI Sotuvchi — Telegram Savdo & Maslahatchi Boti

Ushbu loyiha har qanday savdo yoki xizmat ko'rsatish biznesi uchun mo'ljallangan universal **Telegram AI Sotuvchi Maslahatchi** boti hisoblanadi. Bot mahsulotlarni taqdim etadi, savat va buyurtmalarni boshqaradi, mijozlarning erkin matnli va ovozli savollariga **Google Gemini AI** orqali professional sotuvchi sifatida javob beradi hamda adminlarga real vaqtda buyurtmalarni nazorat qilish imkonini beradi.

---

## 🌟 Asosiy Imkoniyatlar

1. **🤖 Aqlli AI Sotuvchi (Gemini 1.5 Flash / Smart Heuristic Fallback):**
   - Mijozning mahsulotlar bo'yicha savollariga, narx so'rovlariga, tavsiya talablariga professional sotuvchi sifatida javob beradi.
   - Javoblar ichidan mos tovarlarni avtomatik aniqlab, bir bosishda savatga qo'shish inline tugmalarini chiqaradi.
   - Ovozli xabarlarni (`.ogg` audio) to'g'ridan-to'g'ri tahlil qilib, matnga o'giradi va sotuv taklifini beradi.
   - Gemini API kaliti kiritilmagan holatda ham aqlli kalit so'zlar va ko'p tilli sinonimlar asosida to'xtovsiz ishlaydi.

2. **🛍 Interaktiv Katalog va Mahsulotlar:**
   - Kategoriyalar va mahsulot kartochkalari (rasm, tavsif, narx, mavjudlik soni).
   - Har bir tovar ostida `[➕ Savatga qo'shish]`, `[➖ / ➕ Miqdor]`, va `[💬 AI dan ushbu mahsulot haqida so'rash]` tugmalari.

3. **🛒 Savat va Buyurtmani Rasmiylashtirish (Checkout FSM):**
   - Savat tarkibini interaktiv o'zgartirish (qo'shish, ayirish, o'chirish, tozalash).
   - Qulay buyurtma berish bosqichlari:
     - Ism kiritish
     - Telefon raqamni kontakt tugmasi yoki matn orqali yuborish
     - Yetkazib berish manzilini matn yoki Telegram geolokatsiyasi orqali yuborish
     - To'lov usulini tanlash (Naqd, Click, Payme)
   - Avtomatik noyob buyurtma raqami yaratilishi (`#261028-4821`).

4. **👑 Qulay Admin Paneli (`/admin`):**
   - Yangi buyurtma tushishi bilan barcha adminlarga darhol buyurtma tafsilotlari va xaridor geolokatsiyasi yetib boradi.
   - Inline holat boshqaruvi: `[✅ Qabul qilish]`, `[🚚 Yetkazilmoqda]`, `[🏁 Bajarildi]`, `[❌ Bekor qilish]`. Holat o'zgarganda xaridorga Telegram orqali darhol bildirishnoma boradi.
   - Yangi mahsulot qo'shish (FSM orqali tovar nomi, narxi, tavsifi va rasmini kiritish).
   - Kunlik va umumiy savdo statistikasi (buyurtmalar soni va jami tushum).
   - AI sotuvchi yo'riqnomasini (System Prompt) Telegram ichidan o'zgartirish.

5. **🌐 Ko'p Tillilik (i18n):**
   - O'zbekcha (Lotin) 🇺🇿
   - Ўзбекча (Кирилл) 🇺🇿
   - Русский 🇷🇺

---

## 🛠 Texnologiyalar

- **Python:** 3.12+
- **Telegram Bot Framework:** `aiogram 3.17+`
- **Database:** SQLite (Async SQLAlchemy 2.0 + `aiosqlite`)
- **AI Integratsiya:** Google Gemini Generative AI (`google-generativeai`)
- **Konfiguratsiya:** `pydantic-settings`, `.env`
- **Testlash:** `pytest`, `pytest-asyncio`
- **Deploy:** Docker, Docker Compose, Systemd service

---

## 📁 Loyiha Tuzilmasi

```
d:/Telegram bot 2/
├── bot/
│   ├── config.py             # Pydantic sozlamalar (.env yuklanishi)
│   ├── database/
│   │   ├── base.py           # DeclarativeBase
│   │   ├── models.py         # User, Category, Product, CartItem, Order, OrderItem modellar
│   │   ├── session.py        # Async engine va session fabrikasi
│   │   └── seed.py           # Boshlang'ich mahsulotlar va toifalar
│   ├── handlers/
│   │   ├── common.py         # /start, /til, do'kon haqida, bog'lanish
│   │   ├── catalog.py        # Mahsulotlar katalogi va tovar kartalari
│   │   ├── cart.py           # Savat boshqaruvi
│   │   ├── checkout.py       # Buyurtma rasmiylashtirish FSM
│   │   ├── orders.py         # Xaridorning o'z buyurtmalari
│   │   ├── voice.py          # Ovozli xabarlarni AI bilan ishlash
│   │   ├── ai_chat.py        # Erkin matnli savollar va AI sotuvchi javoblari
│   │   └── admin.py          # Admin paneli, buyurtma statuslari, statistika
│   ├── keyboards/
│   │   ├── reply.py          # Asosiy menyu, kontakt, lokatsiya tugmalari
│   │   └── inline.py         # Tillar, toifalar, savat, admin amallari tugmalari
│   ├── middlewares/
│   │   └── user_middleware.py # Foydalanuvchini ro'yxatga olish va DB sessiyasi
│   ├── services/
│   │   ├── catalog_service.py # Katalog CRUD
│   │   ├── cart_service.py   # Savat hisob-kitoblari
│   │   ├── order_service.py  # Buyurtma yaratish va statistika
│   │   └── gemini_sales.py   # Gemini AI sotuvchi va ovozli xabar tahlili
│   └── utils/
│       ├── i18n.py           # 3 tildagi matnlar va tarjimalar
│       └── formatters.py     # Narxlar, cheklar va buyurtma formatlari
├── tests/
│   ├── test_models.py        # Baza modellari testi
│   ├── test_cart_order.py    # Savat va buyurtma sikli testi
│   └── test_sales_ai.py      # AI sotuvchi mantiqiy testi
├── .env                      # Muhit o'zgaruvchilari (maxfiy)
├── .env.example              # Namunaviy konfiguratsiya
├── Dockerfile                # Docker tasviri
├── docker-compose.yml        # Docker compose sozlamasi
├── requirements.txt          # Python kutubxonalari
├── run.py                    # Ishga tushirish fayli
└── sotuvchi.service          # VPS systemd servisi
```

---

## ⚙️ O'rnatish va Ishga Tushirish

### 1. Virtual muhitni faollashtirish va kutubxonalarni o'rnatish:
```powershell
python -m venv .venv
.\.venv\Scripts\pip.exe install -r requirements.txt
```

### 2. Sozlamalar (`.env`):
`.env` faylida quyidagi ma'lumotlar saqlanadi:
```env
BOT_TOKEN=9277921986:AAFriz9__oOJgaqrhNdW3NeIfjdg1jZcBM8
ADMIN_IDS=SIZNING_TELEGRAM_IDINGIZ
GEMINI_API_KEY=SIZNING_GEMINI_API_KALITINGIZ
GEMINI_MODEL=gemini-1.5-flash
DATABASE_URL=sqlite+aiosqlite:///sotuvchi.db
STORE_NAME=Biznes AI Do'koni
STORE_DESCRIPTION=Universal internet do'koni va professional xizmatlar markazi
STORE_PHONE=+998901234567
DELIVERY_PRICE=20000
```
> **Eslatma:** Agar siz o'zingizning Telegram ID raqamingizni bilmasangiz, Telegramda `@userinfobot` ga `/start` yuborib bilib oling va `ADMIN_IDS` ga yozing.

### 3. Testlarni tekshirish:
```powershell
.\.venv\Scripts\pytest.exe -v
```

### 4. Botni ishga tushirish:
```powershell
.\.venv\Scripts\python.exe run.py
```

---

## 🐳 Docker Orqali Ishga Tushirish

Serverda yoki konteynerda ishga tushirish uchun:
```bash
docker compose up -d --build
```

---

## 📱 Botdan Foydalanish

1. Telegramda botni oching: **`@Ai_sotuvchii_bot`**
2. `/start` buyrug'ini bering.
3. Asosiy menyudan:
   - **`🛍 Mahsulotlar katalogi`**: Toifalarni ko'rish, mahsulotlarni tanlash va savatga solish.
   - **`🛒 Savat`**: Tanlangan tovarlar sonini boshqarish va buyurtma berish.
   - **`💬 AI Maslahatchi`**: Do'konda qanday tovarlar borligi, qaysi birini tanlash afzalligi haqida yozish yoki ovozli xabar yuborish.
   - **`📦 Buyurtmalarim`**: Buyurtmangiz holati (`Yangi`, `Qabul qilindi`, `Yetkazilmoqda`, `Bajarildi`) ni tekshirish.
   - **`⚙️ Admin Panel`**: (Adminlar uchun) Buyurtmalarni boshqarish, yangi tovar qo'shish va statistika.
