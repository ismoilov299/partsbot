"""
Main bot initialization and configuration
"""
import os
import sys
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from dotenv import load_dotenv
import redis.asyncio as redis

# Add project root to path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, os.path.join(PROJECT_ROOT, 'src'))

# Load environment variables from project root
env_path = os.path.join(PROJECT_ROOT, '.env')
load_dotenv(dotenv_path=env_path)

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_app.settings')
import django
django.setup()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Bot token from environment
BOT_TOKEN = os.getenv('BOT_TOKEN')
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN is not set in .env file")

# Redis configuration
REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.getenv('REDIS_PORT', '6379'))
REDIS_DB = int(os.getenv('REDIS_DB', '0'))


async def get_redis_storage():
    """Create Redis storage for FSM"""
    redis_client = redis.Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        db=REDIS_DB,
        decode_responses=False
    )
    return RedisStorage(redis_client)


async def create_bot():
    """Create and configure bot instance"""
    bot = Bot(token=BOT_TOKEN)
    storage = await get_redis_storage()
    dp = Dispatcher(storage=storage)
    
    # Import and register routers
    from bot.handlers import start, search, shop_add, request, admin
    
    # Register routers in priority order (specific handlers first, catch-all last)
    dp.include_router(admin.router)
    dp.include_router(search.router)
    dp.include_router(shop_add.router)
    dp.include_router(request.router)
    dp.include_router(start.router)  # Must be last - has catch-all handler
    
    return bot, dp


async def on_startup(bot: Bot):
    """Actions on bot startup"""
    logger.info("Bot started successfully!")


async def on_shutdown(bot: Bot):
    """Actions on bot shutdown"""
    logger.info("Bot shutting down...")