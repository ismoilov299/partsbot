# 🎉 BOT TO'LIQ TAYYOR VA ISHLAYAPTI!

## ✅ Bot muvaffaqiyatli ishga tushdi!

Bot token yangilandi va bot to'liq ishlayapti! ✨

## 📱 Bot funksiyalari

### 1️⃣ Til tanlash
- Birinchi marta `/start` bosganida
- 🇺🇿 O'zbekcha / 🇷🇺 Русский

### 2️⃣ Do'kon qidirish (✅ To'liq ishlaydi)
- Model bo'yicha qidirish
- 7 ta avtomobil markasi
- 14 ta shahar
- Do'konlar ro'yxati telefon va manzil bilan

### 3️⃣ Do'kon kiritish (✅ TO'LIQ YANGI!)
Foydalanuvchidan quyidagi ma'lumotlar so'raladi:

1. **Do'kon nomi** - Tekstda
2. **Telefon raqam** - Masalan: +998901234567
3. **Shahar** - Inline button orqali tanlash (14 ta shahar)
4. **Manzil** - Tekstda, masalan: Chilonzor, 12-kvartal
5. **Do'kon rasmi** - Fotosuratni yuklash
6. **Avtomobil markalari** - Qaysi marka uchun zapchast sotishi (7 ta variant)
7. **Tavsif** - Qanday zapchastlar sotish haqida

Keyin barcha ma'lumotlar rasm bilan birgalikda tasdiqlanadi va ma'lumotlar bazasiga saqlanadi!

### 4️⃣ So'rov qoldirish (📝 Keyingi versiyada)
- Tez orada qo'shiladi

## 🚀 Botni ishga tushirish

```powershell
# Virtual environment aktivatsiya qilish
.\venv\Scripts\Activate.ps1

# Botni ishga tushirish
python run.py
```

## 🛑 Botni to'xtatish

Terminal'da `Ctrl+C` bosing

## 📊 Ma'lumotlar

**Tayyor shaharlar (14):**
Toshkent, Andijon, Buxoro, Farg'ona, Jizzax, Namangan, Navoiy, Qashqadaryo, Qoraqalpog'iston, Samarqand, Sirdaryo, Surxondaryo, Toshkent viloyati, Xorazm

**Avtomobil markalari (7):**
1. KIA/HYUNDAI
2. CHEVROLET GM
3. CHERY/JETOUR/HAVAL
4. BYD
5. BMW
6. MERCEDES BENZ
7. Другие Иномарки

## 🎨 Django Admin Panel

1. Ishga tushirish:
```powershell
python manage.py runserver
```

2. Kirish:
- URL: http://localhost:8000/admin
- Login: admin
- Parol: 123

Admin panelda:
- Barcha foydalanuvchilarni ko'rish
- Do'konlarni boshqarish va o'chirish
- Rasmlar (photo_file_id) ko'rish
- Shaharlar va markalarni tahrirlash

## 📝 Bot test qilish

1. Telegram'da botingizga `/start` yuboring
2. Til tanlang
3. **Do'kon qidirish** tugmasini bosing:
   - Model bo'yicha qidirish
   - Marka tanlang
   - Shahar tanlang
   - Natijalarni ko'ring

4. **Do'kon kiritish** tugmasini bosing:
   - Do'kon nomini kiriting
   - Telefon raqam kiriting
   - Shahar tanlang
   - Manzil kiriting
   - Rasm yuboring
   - Marka tanlang
   - Tavsif yozing
   - Tasdiqlang
   - ✅ Do'kon saqlanadi!

## 🔧 Texnologiyalar

- **Aiogram 3.15** - Telegram Bot Framework
- **Django 5.1** - Web Framework + ORM
- **SQLite** - Ma'lumotlar bazasi
- **Redis (Memurai)** - FSM State storage
- **Python 3.10+**

## 📸 Rasmlar saqlash

Rasmlar Telegram serverlarida saqlanadi. Faqat `photo_file_id` ma'lumotlar bazasida saqlanadi. Bu:
- Joyni tejaydi
- Tezroq ishlaydi
- Telegram orqali rasmlarni yuklash oson

## ⚙️ .env konfiguratsiyasi

```env
BOT_TOKEN=YANGI_TOKEN
ADMIN_CHAT_ID=1272338806
DATABASE_URL=sqlite+aiosqlite:///./zapchast_bot.db
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
```

## 🎯 Qo'shimcha funksiyalar (ixtiyoriy)

1. **Ko'p markalarga qo'shish** - Hozirda bitta marka, keraksa ko'p marka tanlash qo'shish mumkin
2. **Rasm'larni ko'rish** - Qidirishda rasmlarni ko'rsatish
3. **So'rov qoldirish** - Agar foydalanuvchi do'kon topmasa
4. **Admin bildirishnoma** - Yangi do'kon qo'shilganda admin'ga xabar

## 🎊 TAYYOR!

Bot professional darajada tayyorlandi va to'liq ishlayapti!

**Barcha funksiyalar:**
- ✅ Til tanlash
- ✅ Do'kon qidirish
- ✅ Do'kon kiritish (YANGI!)
- ✅ Rasm yuklash
- ✅ Ma'lumotlarni tasdiqlash
- ✅ Admin panel

Muvaffaqiyatlar! 🚀
