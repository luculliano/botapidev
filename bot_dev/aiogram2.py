"""echo bot"""
import asyncio
from aiogram import Bot, Dispatcher
import os
import logging
from aiogram.types.message import Message
from aiogram.filters import Command
from aiogram.types import ContentType
from aiogram import F

TOKEN = os.getenv("BOT_TOKEN", "")

bot = Bot(TOKEN)

dp = Dispatcher()

logging.basicConfig(level=logging.INFO)


@dp.message(Command("start", "help"))
async def process_start_command(message: Message) -> None:
    text = """
        Welcome!
I'm EchoBot. Powered by luculliano.
I reply the same message as your send me.
    """
    await message.answer(text)


@dp.message(F.content_type == ContentType.PHOTO)
# F.contentType.in_((ContentType.PHOTO, ...))
async def process_photo(message: Message) -> None:
    """this hanle all photo type so to filter messages i need to use:
    F magic filter in construction F.content_type == ContentType.VOCIE/VIDEO...
    ContentType is the same as key in Message dict, i.e. if message is audio it
    has an audio attr if no => no audio key and it is None. I can do so too:
    F.content_type == "audio"
    """
    logging.info(message.json(indent=2, exclude_none=True))
    await message.reply_photo(message.photo[0].file_id)


@dp.message(F.content_type == ContentType.VOICE)
async def process_voice(message: Message) -> None:
    logging.info(message.json(indent=2, exclude_none=True))
    await message.reply_voice(message.voice.file_id)


@dp.message()
async def process_emoji(message: Message) -> None:
    """to easy handle all types of messages user send_copy method"""
    logging.info(message.json(indent=2, exclude_none=True))
    try:
        await message.send_copy(message.chat.id)
    except TypeError:
        await message.reply("This type is not supported!")


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
