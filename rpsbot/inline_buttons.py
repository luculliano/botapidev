import asyncio
import logging
from os import getenv

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.filters.text import Text
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types.callback_query import CallbackQuery
from aiogram.filters.callback_data import CallbackData
from aiogram.types.message import Message
from dotenv import load_dotenv
from aiogram import F

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


@dp.message(Command("start"))  # updates not supported
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


class BookCallbackData(CallbackData, prefix="book", sep="-"):
    book_id: int
    book_name: str
    book_pages: int

btn1 = InlineKeyboardButton(text="Book 1", callback_data=BookCallbackData(book_id=1, book_name="Women", book_pages=222).pack())
btn2 = InlineKeyboardButton(text="Book 2", callback_data=BookCallbackData(book_id=2, book_name="Men", book_pages=333).pack())
keyboard = InlineKeyboardMarkup(inline_keyboard=[[btn1], [btn2]])


@dp.message(Command("temp"))
async def proceed_temp(message: Message) -> None:
    await message.answer("That the test CallbackData", reply_markup=keyboard)


@dp.callback_query(BookCallbackData.filter(F.book_id == 1))
async def proceed_book(callback: CallbackQuery, callback_data: BookCallbackData) -> None:
    await callback.message.answer(f"Book number {callback_data.book_id} has name {callback_data.book_name}")
    await callback.answer()


async def main() -> None:
    # print(btn1.callback_data)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
