from itertools import zip_longest
import logging
from os import getenv

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types.message import Message
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO)

VOCABULARY_EN = {
    "/start": "This keyboard powered by "
              "<code>create_inline_kb</code> function"
}

VOCABULARY_BUTTONS_EN = {
    "Button's 1 data to filter when pressed": "Button 1",
    "Button's 2 data to filter when pressed": "Button 2",
    "Button's 3 data to filter when pressed": "Button 3",
    "Button's 4 data to filter when pressed": "Button 4",
    "Button's 5 data to filter when pressed": "Button 5",
}


def create_inline_kb(width: int, *args, **kwargs) -> InlineKeyboardMarkup:
    """Generates specific width inline keyboard on the fly"""
    keyboard = []
    buttons = (InlineKeyboardButton(text=VOCABULARY_BUTTONS_EN[button_data],
                            callback_data=button_data) for button_data in args)
    for tpl in zip_longest(*(iter(buttons),)*width):
        keyboard.append(list(filter(None, tpl)))

    buttons = (InlineKeyboardButton(text=button_text, callback_data=button_data)
                                for button_data, button_text in kwargs.items())
    for tpl in zip_longest(*(iter(buttons),)*width):
        keyboard.append(list(filter(None, tpl)))

    return InlineKeyboardMarkup(inline_keyboard=keyboard)

keyboard = create_inline_kb(2, *VOCABULARY_BUTTONS_EN)

bot = Bot(getenv("TELEGRAM_BOT_TOKEN", ""))
dp = Dispatcher()


@dp.message(Command("start"))
async def proceed_start(message: Message) -> None:
    await message.answer(VOCABULARY_EN["/start"],
                         parse_mode="HTML",
                         reply_markup=keyboard)


if __name__ == "__main__":
    dp.run_polling(bot)
