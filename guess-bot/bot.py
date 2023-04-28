import asyncio

from aiogram import Bot, Dispatcher

from config import TELEGRAM_BOT_TOKEN
import handlers
from keyboards import set_main_menu
from settings import logger
from database import init_db


async def main() -> None:
    logger.info("Start pooling.")

    await init_db()

    bot = Bot(TELEGRAM_BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(handlers.router)

    await set_main_menu(bot)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
