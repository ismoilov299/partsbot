
"""
Main entry point for the bot
"""
import asyncio
import os
import sys
from dotenv import load_dotenv

# Load environment variables first
load_dotenv()

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from bot.bot import create_bot, on_startup, on_shutdown

async def main():
    """Main function to run the bot"""
    bot, dp = await create_bot()
    
    # Register startup and shutdown handlers
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    
    # Start polling
    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nBot stopped by user")
