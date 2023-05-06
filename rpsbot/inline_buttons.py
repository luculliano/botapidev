import asyncio
import logging
from os import getenv

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.filters.text import Text
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types.callback_query import CallbackQuery
from aiogram.types.message import Message
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)

bot = Bot(getenv("TELEGRAM_BOT_TOKEN", ""))
dp = Dispatcher()

btn_url = [
    [InlineKeyboardButton(text="Outer link", url="https://google.com")],
    [InlineKeyboardButton(text="Inner link", url="tg://resolve?domain=t0digital")],
    [InlineKeyboardButton(text="Callback button 1", callback_data="Callback button 1 pressed")],
    [InlineKeyboardButton(text="Callback button 2", callback_data="Callback button 2 pressed")],
]


keyboard = InlineKeyboardMarkup(inline_keyboard=btn_url[2:])


@dp.message(Command("start"))  # udates not supported
async def proceed_url(message: Message) -> None:
    await message.answer("Some inline buttons bellow", reply_markup=keyboard)



@dp.callback_query(Text("Callback button 1 pressed"))
async def proceed_callback1(callback: CallbackQuery) -> None:
    if callback.message.text != "11111111111111111":  # pyright: ignore
        await callback.message.edit_text("11111111111111111", reply_markup=callback.message.reply_markup)  # pyright: ignore
    await callback.answer(text="ЯХАААА 1")

@dp.callback_query(Text("Callback button 2 pressed"))
async def proceed_callback2(callback: CallbackQuery) -> None:
    if callback.message.text != "22222222222222222":  # pyright: ignore
        await callback.message.edit_text("22222222222222222", reply_markup=callback.message.reply_markup)  # pyright: ignore
    await callback.answer(text="ЯХАААА 2 (с задержкой)", show_alert=True)


async def main() -> None:
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
