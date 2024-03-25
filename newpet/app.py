import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
import logging
from data import config  # Assuming `config.py` contains database connection details
from handlers.users import get_start, get_register  # Assuming these modules handle user interactions
from utils.db_api.db_gino import db  # Assuming `db_gino.py` provides database interaction functions
from handlers.users.get_register import init_db

async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    bot = Bot(token=config.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    dp = Dispatcher()
    dp.include_routers(get_start.router, get_register.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await init_db()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
    print("run")
