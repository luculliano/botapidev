import asyncio
import logging
from os import getenv
from aiogram import F
from aiogram import Bot, Dispatcher
from aiogram.filters import Command, Text
from aiogram.types import (
    ContentType,
    KeyboardButton,
    KeyboardButtonPollType,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)
from aiogram.types import WebAppInfo
from aiogram.types.message import Message
from dotenv import load_dotenv

from vocabulary import TEXT1, TEXT2

load_dotenv()

logging.basicConfig(level=logging.INFO)

bot = Bot(getenv("TELEGRAM_BOT_TOKEN", ""))
dp = Dispatcher()


button_1: KeyboardButton = KeyboardButton(text="YES")
button_2: KeyboardButton = KeyboardButton(text="NO")
button_3: KeyboardButton = KeyboardButton(text="🤷")
keyboard: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
    keyboard=[[button_1, button_2], [button_3]],
    resize_keyboard=True,  # to make normal size
    one_time_keyboard=True,  # to hide after answer and Remove is not needed.
)

# keyboard = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=f"button {j * 3 + i}") for i in range(1, 4)] for j in range(3)])
# button_4 = [KeyboardButton(text=f"button #{i}") for i in range(1, 5)]
# button_5 = [KeyboardButton(text=f"button #{i}") for i in range(5, 9)]
# keyboard = ReplyKeyboardMarkup(keyboard=[button_4, button_5], resize_keyboard=True, one_time_keyboard=True)

# button_6 = [KeyboardButton(text=f"button #{i}") for i in range(1, 15)]
# keyboard = ReplyKeyboardMarkup(keyboard=[button_6[:3], button_6[4:8]], resize_keyboard=True, one_time_keyboard=True)


@dp.message(Command("question"))
async def proceed_question(message: Message) -> None:
    await message.answer("Are you ready?", reply_markup=keyboard)


@dp.message(Text(text=("YES", "NO")))
async def proceed_answer(message: Message) -> None:
    await message.answer(
        "Got you!", reply_markup=ReplyKeyboardRemove(remove_keyboard=True)
    )


@dp.message(Text(text="🤷"))
async def proceed_3(message: Message) -> None:
    await message.answer("NONONONONONO!")
    await message.answer("Are you ready?", reply_markup=keyboard)


@dp.message(Command("html"))
async def proceed_html(message: Message) -> None:
    await message.answer(TEXT1, parse_mode="HTML")


@dp.message(Command("md"))
async def proceed_md(message: Message) -> None:
    await message.answer(TEXT2, parse_mode="MarkdownV2")


web_app_btn: KeyboardButton = KeyboardButton(  # allows to run apps in tellegram
    text="Start Web App", web_app=WebAppInfo(url="https://luculliano.ru/")
)

# Создаем объект клавиатуры
web_app_keyboard: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
    keyboard=[[web_app_btn]], resize_keyboard=True
)


@dp.message(Command("webapp"))
async def proceed_webapp(message: Message) -> None:
    await message.answer("Launch webapp", reply_markup=web_app_keyboard)


geo_btn: KeyboardButton = KeyboardButton(text="Share location", request_location=True)
loc_keyboard = ReplyKeyboardMarkup(keyboard=[[geo_btn]])


@dp.message(Command("loc"))
async def proceed_loc(message: Message) -> None:
    await message.answer("Location", reply_markup=loc_keyboard)


# type='quiz' - викторина
# type='regular' - опрос
poll_btn: KeyboardButton = KeyboardButton(
    text="Создать опрос/викторину", request_poll=KeyboardButtonPollType(type="quiz")
)

kb = ReplyKeyboardMarkup(
    keyboard=[[poll_btn]], resize_keyboard=True, one_time_keyboard=True
)


@dp.message(Command("quz"))
async def proceed_quiz(message: Message) -> None:
    await message.answer("quzzz", reply_markup=kb)


mob_btn = KeyboardButton(text="share phone", request_contact=True)
mob_keyboard = ReplyKeyboardMarkup(
    keyboard=[[mob_btn]], resize_keyboard=True, one_time_keyboard=True
)


@dp.message(Command("reg"))
async def proceed_phone(message: Message) -> None:
    await message.answer("Register bellow", reply_markup=mob_keyboard)


@dp.message(F.content_type == ContentType.CONTACT)
async def proceed_contact(message: Message) -> None:
    logging.info(f"got the data: {message.contact}")


async def main() -> None:
    await bot.delete_my_commands()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
