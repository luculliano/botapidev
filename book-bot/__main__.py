import asyncio

from aiogram import Bot, Dispatcher

from config_data import TELEGRAM_BOT_TOKEN, logger
from handlers import user_handlers
from keyboards import set_main_menu
from vocabulary import VOCABULARY_RU


async def main() -> None:
    logger.info("Start pooling.")

    bot = Bot(TELEGRAM_BOT_TOKEN, parse_mode="HTML")
    dp = Dispatcher()
    dp.include_routers(user_handlers.router)

    await set_main_menu(bot)
    await bot.set_my_description(VOCABULARY_RU["description"])
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
