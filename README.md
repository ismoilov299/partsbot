# Zapchast Bot

Professional Telegram bot for auto parts shop management.

## Features

- 🌐 Multi-language support (Uzbek & Russian)
- 🔍 Search shops by car brand and city
- 🏪 Add and manage shops
- 📝 Leave requests for parts
- 💾 SQLite database
- ⚡ Redis for state management

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

3. Initialize database with cities and car brands:
```bash
python init_db.py
```

4. Create Django superuser (optional):
```bash
python manage.py createsuperuser
```

5. Make sure Redis is running on localhost:6379

## Configuration

All configuration is in `.env` file:
- `BOT_TOKEN` - Telegram bot token
- `DATABASE_URL` - SQLite database URL
- `REDIS_HOST`, `REDIS_PORT`, `REDIS_DB` - Redis configuration

## Running

Start the bot:
```bash
python run.py
```

Access Django admin panel:
```bash
python manage.py runserver
```
Then open http://localhost:8000/admin

## Project Structure

```
zapchastbot/
├── src/
│   ├── bot/
│   │   ├── handlers/      # Message and callback handlers
│   │   ├── keyboards/     # Inline and reply keyboards
│   │   ├── states/        # FSM states
│   │   ├── utils/         # Database utilities
│   │   └── bot.py        # Main bot configuration
│   └── django_app/
│       ├── models.py      # Database models
│       ├── admin.py       # Admin panel configuration
│       └── settings.py    # Django settings
├── manage.py             # Django management script
├── run.py               # Bot entry point
├── init_db.py           # Database initialization
└── requirements.txt     # Python dependencies
```

## Models

- **User** - Telegram users
- **City** - Cities where shops are located
- **CarBrand** - Car brands/models
- **Shop** - Auto parts shops
- **Request** - User requests for parts

## Usage

1. Start bot with `/start`
2. Choose language (first time only)
3. Select action:
   - 🔍 Search shops - find shops by brand and city
   - ➕ Add shop - register your shop (coming soon)
4. Follow bot instructions

## Technologies

- Python 3.11+
- Aiogram 3.x
- Django 5.x
- SQLite
- Redis
- asyncio
