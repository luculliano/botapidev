import asyncio
import logging
import os

import aiohttp
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types.message import Message
from aiogram.enums.dice_emoji import DiceEmoji

TOKEN = os.getenv("BOT_TOKEN", "")


bot = Bot(TOKEN)

dp = Dispatcher()

logging.basicConfig(level=logging.INFO)


@dp.message(Command(commands=["start"]))
async def handle_start_command(message: Message) -> None:
    # answer is an alias istead of:
    # await bot.send_message(message.chat.id, message.text)
    await message.answer(f"Welcome!\nI'm EchoBot. Powered by luculliano.")


@dp.message(Command(commands=["help"]))
async def handle_help_command(message: Message) -> None:
    await message.answer(f"Write me something and I will send you a cat.")


async def get_catgif() -> str:
    """get cat images from third-party API"""

    url = "https://cataas.com/cat/gif"
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params={"json": "true"}) as response:
            catlink = await response.json()
            return f"{url[:-8]}{catlink['url']}"


@dp.message(Command("cat"))
async def send_catgif(message: Message) -> None:
    cat = await get_catgif()
    await message.reply_video(cat, caption="Cats are here 😺")


@dp.message(Command("dice"))
async def send_dice(message: Message, bot: Bot) -> None:
    """send dice in other chat
       here i specify needed bot and its methods
    """
    await bot.send_dice(chat_id=-1001913796543, emoji=DiceEmoji.DICE)

# @dp.message()  # if not args - no filters, so all messages.
async def echo_message(message: Message) -> None:
    await message.reply(message.text)


async def main() -> None:
    # insted of syntax sugar use TelegramEventObserer class decorator with method:
    # register
    dp.message.register(echo_message)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
    # dp.run_polling(bot)  # is like asyncio.run, it takes bots and start longpooling
