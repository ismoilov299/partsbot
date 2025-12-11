# 🎉 Loyiha tayyor!

## ✅ Bajarilgan ishlar

1. **Django + Aiogram integratsiyasi** - Professional tarzda
2. **Ma'lumotlar bazasi** - SQLite + Redis
3. **Modellar:**
   - User (foydalanuvchilar)
   - City (shaharlar) - 14 ta
   - CarBrand (avtomobil markalari) - 7 ta
   - Shop (do'konlar)
   - Request (so'rovlar)

4. **Bot funksiyalari:**
   - ✅ Til tanlash (O'zbek/Rus)
   - ✅ Do'kon qidirish (marka va shahar bo'yicha)
   - ✅ Inline klaviaturalar
   - ⏳ So'rov qoldirish (keyingi versiyada)
   - ⏳ Do'kon kiritish (keyingi versiyada)

5. **Test ma'lumotlar:**
   - 3 ta test do'kon yaratildi
   - Toshkent va Samarqand uchun

## 🚀 Ishga tushirish

### 1-qadam: Redis o'rnatish

**WSL orqali (Tavsiya):**
```powershell
wsl --install
wsl
sudo apt update && sudo apt install redis-server -y
sudo service redis-server start
```

**Yoki Docker:**
```powershell
docker run -d -p 6379:6379 --name redis redis:alpine
```

### 2-qadam: Botni ishga tushirish

```powershell
# Redis tekshirish
.\start_redis.ps1

# Botni ishga tushirish
.\start_bot.ps1
```

## 📱 Botni test qilish

1. Telegram'da botingizga `/start` yuboring
2. Til tanlang (O'zbek yoki Rus)
3. "🔍 Do'kon qidirish" tugmasini bosing
4. "🚗 Model bo'yicha qidirish" tanlang
5. Markani tanlang (masalan, "1. KIA/HYUNDAI")
6. Shaharni tanlang (masalan, "Toshkent")
7. Do'konlar ro'yxatini ko'ring!

## 🎨 Django Admin

**Kirish:**
```powershell
python manage.py runserver
```
**URL:** http://localhost:8000/admin
**Login:** admin
**Parol:** 123

Admin panelda:
- Foydalanuvchilarni ko'rish
- Do'konlarni boshqarish
- Shaharlar va markalarni tahrirlash

## 📁 Fayl strukturasi

```
zapchastbot/
├── .env                    # Bot konfiguratsiyasi
├── manage.py              # Django management
├── run.py                 # Bot entry point
├── start_bot.ps1          # Bot ishga tushirish
├── start_redis.ps1        # Redis ishga tushirish
├── init_db.py             # Ma'lumotlar bazasini to'ldirish
├── create_test_data.py    # Test ma'lumotlar
├── requirements.txt       # Python kutubxonalar
│
├── src/
│   ├── bot/
│   │   ├── handlers/      # start, search, shop_add, request
│   │   ├── keyboards/     # Inline klaviaturalar
│   │   ├── states/        # FSM states
│   │   ├── utils/         # Database utilities
│   │   └── bot.py        # Bot konfiguratsiyasi
│   │
│   └── django_app/
│       ├── models.py      # User, Shop, City, CarBrand, Request
│       ├── admin.py       # Admin panel
│       └── settings.py    # Django settings
│
└── zapchast_bot.db       # SQLite database
```

## 🔄 Keyingi qadamlar (agar kerak bo'lsa)

### 1. So'rov qoldirish funksiyasini qo'shish

`src/bot/handlers/request.py` faylini to'ldirish kerak:
- Foydalanuvchidan qism tavsifini so'rash
- Telefon raqam so'rash
- Shahar tanlash
- Ma'lumotlar bazasiga saqlash

### 2. Do'kon qo'shish funksiyasini qo'shish

`src/bot/handlers/shop_add.py` faylini to'ldirish kerak:
- Do'kon nomi so'rash
- Shahar tanlash
- Markalarni tanlash (ko'p tanlash)
- Telefon raqam
- Manzil va tavsif
- Tasdiqlash

### 3. Yangi markalara qo'shish

Django Admin orqali yoki `init_db.py` ni o'zgartirish

### 4. Rasm yuklash

Shop modeliga `photo` field qo'shish va handler'da file upload qo'shish

## 🐛 Muammolarni hal qilish

### Redis ulanmaydi:
```powershell
# Status tekshirish
wsl redis-cli ping

# Qayta ishga tushirish
wsl sudo service redis-server restart
```

### Bot javob bermaydi:
1. Redis ishayotganini tekshiring
2. Terminal'dagi xatolarni o'qing
3. `.env` fayldagi `BOT_TOKEN` to'g'riligini tekshiring

### Database xatolar:
```powershell
# Migratsiyalarni qayta qo'llash
python manage.py makemigrations
python manage.py migrate

# Ma'lumotlarni qayta yuklash
python init_db.py
```

## 📊 Ma'lumotlar

**Shaharlar (14):**
Toshkent, Andijon, Buxoro, Farg'ona, Jizzax, Namangan, Navoiy, Qashqadaryo, Qoraqalpog'iston, Samarqand, Sirdaryo, Surxondaryo, Toshkent viloyati, Xorazm

**Avtomobil markalari (7):**
1. KIA/HYUNDAI
2. CHEVROLET GM
3. CHERY/JETOUR/HAVAL
4. BYD
5. BMW
6. MERCEDES BENZ
7. Другие Иномарки

## 🎯 Bot texnologiyalari

- **Python 3.10+**
- **Aiogram 3.15** - Telegram Bot Framework
- **Django 5.1** - Web Framework
- **SQLite** - Ma'lumotlar bazasi
- **Redis** - State storage (FSM)
- **AsyncIO** - Asinxron dasturlash

## 🔐 Xavfsizlik

- `.env` faylini git'ga yuklamang
- `BOT_TOKEN` ni hech kimga ko'rsatmang
- Production'da `DEBUG=False` qiling
- Django `SECRET_KEY`ni o'zgartiring

## ✅ Ishlaydigan funksiyalar

1. **Start command** - `/start`
2. **Til tanlash** - Birinchi marta
3. **Asosiy menyu** - 2 ta tugma
4. **Do'kon qidirish** - To'liq ishlaydi
5. **Marka tanlash** - 7 ta variant
6. **Shahar tanlash** - 14 ta variant
7. **Natija ko'rsatish** - Do'konlar ro'yxati

## 📞 Yordam

- **README.md** - Umumiy ma'lumot
- **START_GUIDE_UZ.md** - O'zbekcha yo'riqnoma
- **REDIS_SETUP.md** - Redis o'rnatish

---

**Bot tayyor va ishga tayyor! 🎊**

Savol bo'lsa, so'rang! 😊
