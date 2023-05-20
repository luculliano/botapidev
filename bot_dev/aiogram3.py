import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import Text
from aiogram.types.message import Message
from dotenv import load_dotenv
from aiogram.filters import BaseFilter
import os
import re
from aiogram import F
import logging

logging.basicConfig(level=logging.INFO)
load_dotenv()

bot = Bot(os.getenv("BOT_TOKEN", ""))

dp = Dispatcher()


class OnlyNums(BaseFilter):
    async def __call__(self, message: Message) -> dict[str, str] | bool:
        text = message.text if message.text is not None else ""
        match = re.findall(r"\d+", text)
        return {"numbers": ", ".join(match)} if match else False


# argument numbers - сисок чисел из фильтра, аргумент должен соответствовать ключу
# а также кол-во аргументов должно соответствоать возвращ. значению
# два фильтра
@dp.message(~F.photo)
async def handle_nums(message: Message) -> None:
    await message.reply("GOT")
    print(message.photo)


@dp.message(Text(startswith="find numbers", ignore_case=True))
async def handle_other(message: Message) -> None:
    await message.reply(f"No numbers found!")


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
