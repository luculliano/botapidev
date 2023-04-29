import asyncio
import logging
from os import getenv

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

import handlers

load_dotenv()

logging.basicConfig(level=logging.INFO)


async def main() -> None:
    bot = Bot(getenv("TELEGRAM_BOT_TOKEN", ""))
    dp = Dispatcher()

    dp.include_router(handlers.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
