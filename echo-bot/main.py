import asyncio
import logging

from aiogram import Bot, Dispatcher

from config import TELEGRAM_BOT_TOKEN
import handlers


async def main() -> None:
    logging.basicConfig(level=logging.INFO)

    bot = Bot(TELEGRAM_BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(handlers.router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
