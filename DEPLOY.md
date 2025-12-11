# Ubuntu Server Deployment Guide

## Serverga ulanish
```bash
ssh root@YOUR_SERVER_IP
```

## Loyihani joylashtirish

### 1. Loyihani /home/partsbot ga ko'chirish
```bash
# Katalog yaratish
mkdir -p /home/partsbot
cd /home/partsbot

# GitHub'dan clone qilish
git clone https://github.com/ismoilov299/partsbot.git .

# yoki scp bilan yuklash (local kompyuterdan)
# scp -r /path/to/zapchastbot/* root@YOUR_SERVER_IP:/home/partsbot/
```

### 2. Deploy scriptni ishga tushirish
```bash
cd /home/partsbot
chmod +x deploy.sh
./deploy.sh
```

### 3. .env faylni sozlash
```bash
nano .env
```

`.env` fayl:
```env
BOT_TOKEN=your_real_bot_token
ADMIN_CHAT_ID=your_telegram_chat_id
DATABASE_URL=sqlite:///./db.sqlite3
REDIS_HOST=localhost
REDIS_PORT=6379
DJANGO_SECRET_KEY=your_long_random_secret_key
DEBUG=False
ALLOWED_HOSTS=*
```

### 4. Django superuser yaratish
```bash
source venv/bin/activate
python manage.py createsuperuser
```

### 5. Servislarni restart qilish
```bash
sudo systemctl restart zapchastbot zapchast-django
```

## Django admin panel

Server IP orqali kirish:
```
http://YOUR_SERVER_IP/admin/
```

Masalan:
- `http://45.123.45.67/admin/`
- `http://192.168.1.100/admin/`

## Foydali komandalar

### Statusni tekshirish
```bash
sudo systemctl status zapchastbot
sudo systemctl status zapchast-django
sudo systemctl status redis
sudo systemctl status nginx
```

### Loglarni ko'rish
```bash
# Bot loglari (real-time)
sudo journalctl -u zapchastbot -f

# Django loglari
sudo journalctl -u zapchast-django -f

# Nginx loglari
sudo tail -f /var/log/nginx/error.log
sudo tail -f /var/log/nginx/access.log
```

### Servislarni boshqarish
```bash
# Restart
sudo systemctl restart zapchastbot
sudo systemctl restart zapchast-django

# Stop
sudo systemctl stop zapchastbot
sudo systemctl stop zapchast-django

# Start
sudo systemctl start zapchastbot
sudo systemctl start zapchast-django
```

### Kodni yangilash
```bash
cd /home/partsbot
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart zapchastbot zapchast-django
```

## Xavfsizlik

### Firewall
```bash
sudo ufw status
sudo ufw allow 22/tcp   # SSH
sudo ufw allow 80/tcp   # HTTP
sudo ufw allow 443/tcp  # HTTPS
sudo ufw enable
```

### SSL (Let's Encrypt)
Agar domen bo'lsa:
```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d yourdomain.com
```

## Database backup

### Manual backup
```bash
cd /home/partsbot
cp db.sqlite3 backup_$(date +%Y%m%d_%H%M%S).sqlite3
```

### Avtomatik backup (cron)
```bash
crontab -e
```

Qo'shish:
```
0 3 * * * cd /home/partsbot && cp db.sqlite3 /home/backups/db_$(date +\%Y\%m\%d).sqlite3
```

## Muammolarni hal qilish

### Bot ishlamayotgan bo'lsa
```bash
# Status tekshirish
sudo systemctl status zapchastbot

# Loglarni ko'rish
sudo journalctl -u zapchastbot -n 50

# Restart
sudo systemctl restart zapchastbot
```

### Django admin ochilmayotgan bo'lsa
```bash
# Nginx va Django statusini tekshirish
sudo systemctl status nginx
sudo systemctl status zapchast-django

# Port tekshirish
sudo netstat -tulpn | grep 8000

# Restart
sudo systemctl restart zapchast-django nginx
```

### Redis muammolari
```bash
# Status
sudo systemctl status redis

# Restart
sudo systemctl restart redis

# Test
redis-cli ping
```

## Monitoring

### htop o'rnatish
```bash
sudo apt install htop
htop
```

### Disk space
```bash
df -h
```

### Memory usage
```bash
free -m
```

## Server xususiyatlari

**Minimal talablar:**
- RAM: 1 GB (2 GB tavsiya etiladi)
- Disk: 10 GB
- CPU: 1 core
- Ubuntu 20.04 LTS yoki yangi

**Portlar:**
- 22: SSH
- 80: HTTP (Nginx)
- 8000: Django (internal)
- 6379: Redis (internal)

## Muhim fayllar

- `/home/partsbot/` - Asosiy loyiha
- `/home/partsbot/.env` - Environment o'zgaruvchilari
- `/home/partsbot/db.sqlite3` - Database
- `/home/partsbot/logs/` - Log fayllar
- `/etc/systemd/system/zapchastbot.service` - Bot service
- `/etc/systemd/system/zapchast-django.service` - Django service
- `/etc/nginx/sites-available/zapchast-admin` - Nginx config
