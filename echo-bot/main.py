import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

from config import TELEGRAM_BOT_TOKEN

logging.basicConfig(level=logging.INFO)

bot = Bot(TELEGRAM_BOT_TOKEN)
dp = Dispatcher()


@dp.message(Command("start", "help"))
async def proceed_start(message: Message) -> None:
    await message.answer(
        "Welcome!\nI'm echo-bot powered by luculliano "
        "and reply the same as you send me."
    )  # pyright: ignore


@dp.message()
async def proceed_messages(message: Message) -> None:
    try:
        await message.send_copy(message.chat.id,
                                reply_to_message_id=message.message_id)
    except Exception:
        await message.reply("It's not supported to reply.")


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
