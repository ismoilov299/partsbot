# 🚀 Zapchast Bot - Ishga tushirish bo'yicha to'liq yo'riqnoma

## ✅ Hozirgi holat

Loyiha to'liq tayyor! Quyidagilar bajarildi:
- ✅ Django va Aiogram o'rnatildi
- ✅ Ma'lumotlar bazasi yaratildi (SQLite)
- ✅ Shaharlar va avtomobil markalari qo'shildi
- ✅ Bot handlerlari va klaviaturalar tayyor

## 🔴 Redis o'rnatish (MUHIM!)

Bot ishlashi uchun Redis zarur. Quyidagi usullardan birini tanlang:

### Usul 1: WSL orqali (Tavsiya etiladi)

1. **WSL o'rnatish:**
```powershell
wsl --install
```

2. **WSL terminalida Redis o'rnatish:**
```bash
sudo apt update
sudo apt install redis-server -y
```

3. **Redisni ishga tushirish:**
```bash
sudo service redis-server start
```

4. **Yoki qisqacha (PowerShell):**
```powershell
.\start_redis.ps1
```

### Usul 2: Docker orqali

```powershell
docker run -d -p 6379:6379 --name redis redis:alpine
```

### Usul 3: Memurai (Windows Redis)

1. https://www.memurai.com/get-memurai dan yuklab oling
2. O'rnating va service ishga tushadi

## 🎯 Botni ishga tushirish

### Oddiy usul:
```powershell
.\start_bot.ps1
```

### Qo'lda usul:
```powershell
.\venv\Scripts\Activate.ps1
python run.py
```

## 🎨 Django Admin Panel

1. **Superuser yaratish:**
```powershell
python manage.py createsuperuser
```

2. **Admin panelni ishga tushirish:**
```powershell
python manage.py runserver
```

3. **Kirish:** http://localhost:8000/admin

Admin panelda:
- Foydalanuvchilarni ko'rish
- Do'konlarni boshqarish
- Shaharlar va markalarni tahrirlash
- So'rovlarni ko'rish

## 📱 Bot funksiyalari

Bot quyidagi imkoniyatlarga ega:

1. **Til tanlash** - Birinchi marta /start bosganida
   - 🇺🇿 O'zbekcha
   - 🇷🇺 Русский

2. **Do'kon qidirish** 
   - Model bo'yicha qidirish
   - 7 ta avtomobil markasi
   - Barcha shaharlar bo'yicha
   - Do'konlar ro'yxati

3. **So'rov qoldirish** (tez orada)

4. **Do'kon kiritish** (tez orada)

## 🗂️ Loyiha strukturasi

```
zapchastbot/
├── src/
│   ├── bot/
│   │   ├── handlers/      # Bot handlerlari
│   │   ├── keyboards/     # Inline klaviaturalar
│   │   ├── states/        # FSM states
│   │   ├── utils/         # Database utilities
│   │   └── bot.py        # Bot konfiguratsiyasi
│   └── django_app/
│       ├── models.py      # Ma'lumotlar bazasi modellari
│       ├── admin.py       # Admin panel
│       └── settings.py    # Django sozlamalari
├── run.py                # Bot ishga tushirish
├── manage.py             # Django management
├── init_db.py            # Ma'lumotlar bazasini to'ldirish
├── start_bot.ps1         # Bot ishga tushirish skripti
└── start_redis.ps1       # Redis ishga tushirish skripti
```

## 🧪 Test qilish

1. **Redis test:**
```powershell
wsl redis-cli ping
# Javob: PONG
```

2. **Bot test:**
Telegram'da botingizga:
- `/start` buyrug'ini yuboring
- Til tanlang
- "Do'kon qidirish" tugmasini bosing
- Marka va shahar tanlang

## 🔧 Muammolarni hal qilish

### Redis ulanmasa:
```powershell
# WSL'da qayta ishga tushirish
wsl sudo service redis-server restart

# Yoki Docker'da
docker restart redis
```

### Bot ishlamasa:
1. Redis ishayotganini tekshiring
2. `.env` faylini tekshiring
3. Loglarni ko'ring (terminal'da)

### Django xatoliklari:
```powershell
# Migratsiyalarni qayta qo'llash
python manage.py migrate

# Ma'lumotlarni qayta yuklash
python init_db.py
```

## 📊 Ma'lumotlar bazasi

**Tayyor ma'lumotlar:**
- 14 ta shahar (Toshkent, Samarqand, Buxoro, ...)
- 7 ta avtomobil markasi:
  1. KIA/HYUNDAI
  2. CHEVROLET GM
  3. CHERY/JETOUR/HAVAL
  4. BYD
  5. BMW
  6. MERCEDES BENZ
  7. Другие Иномарки

## 🔒 Xavfsizlik

- `.env` faylini hech qachon git'ga yuklamang (`.gitignore`'da)
- `BOT_TOKEN` ni maxfiy saqlang
- Django `SECRET_KEY` ni o'zgartiring production uchun

## 📞 Yordam

Muammolar bo'lsa:
1. `README.md` ni o'qing
2. `REDIS_SETUP.md` ni ko'ring
3. Terminal loglarini tekshiring

Muvaffaqiyat! 🎉
