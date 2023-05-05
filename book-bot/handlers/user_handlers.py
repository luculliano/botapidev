import re

from aiogram import Router
from aiogram.filters import Command
from aiogram.filters.text import Text
from aiogram.types import CallbackQuery
from aiogram.types.message import Message
from aiosqlite import IntegrityError

from config_data import SQLITE_DB_FILE
from database import DataBase
from keyboards import create_bookmarks_kb, create_edit_kb, create_inline_kb
from vocabulary import VOCABULARY_RU
from filters import IsBookmarkDelete

router = Router()
db = DataBase(SQLITE_DB_FILE)

@router.message(Command("start"))
async def proceed_start(message: Message) -> None:
    cur_uid = message.from_user.id  # pyright: ignore
    await db.init_user(cur_uid)
    answer = VOCABULARY_RU["/start"].format(name=message.from_user.first_name)  # pyright: ignore
    await message.answer(answer)


@router.message(Command("help"))
async def proceed_help(message: Message) -> None:
    await message.answer(VOCABULARY_RU["/help"])


@router.message(Command("beginning"))
async def proceed_beginning(message: Message) -> None:
    cur_uid = message.from_user.id  # pyright: ignore
    book_data = await db.update_page(cur_uid, -1, is_begin=True)
    keyboard = create_inline_kb(3, "backward",
                f"{book_data.page_number}/{book_data.book_length}", "forward")
    await message.answer(book_data.page_text, reply_markup=keyboard)


@router.message(Command("continue"))
async def proceed_continue(message: Message) -> None:
    cur_uid = message.from_user.id  # pyright: ignore
    book_data = await db.update_page(cur_uid, 1, is_continue=True)
    keyboard = create_inline_kb(3, "backward",
                f"{book_data.page_number}/{book_data.book_length}", "forward")
    await message.answer(book_data.page_text, reply_markup=keyboard)


@router.callback_query(Text("backward"))
async def proceed_backward(callback: CallbackQuery) -> None:
    cur_uid = callback.from_user.id  # pyright: ignore
    try:
        book_data = await db.update_page(cur_uid, -1)
        keyboard = create_inline_kb(3, "backward",
                    f"{book_data.page_number}/{book_data.book_length}", "forward")
        await callback.message.edit_text(text=book_data.page_text,  # pyright: ignore
                                         reply_markup=keyboard)
    except IntegrityError:
        await callback.answer()


@router.callback_query(Text("forward"))
async def proceed_forward(callback: CallbackQuery) -> None:
    cur_uid = callback.from_user.id  # pyright: ignore
    try:
        book_data = await db.update_page(cur_uid, 1)
        keyboard = create_inline_kb(3, "backward",
                    f"{book_data.page_number}/{book_data.book_length}", "forward")
        await callback.message.edit_text(text=book_data.page_text,  # pyright: ignore
                                         reply_markup=keyboard)
    except IntegrityError:
        await callback.answer()


@router.callback_query(lambda x: re.fullmatch(r"^(\d+)/\d+$", x.data))
async def proceed_bookmark(callback: CallbackQuery) -> None:
    cur_uid = callback.from_user.id  # pyright: ignore
    try:
        await db.add_bookmark(cur_uid)
        await callback.answer(text=VOCABULARY_RU["add_bookmark"])
    except IntegrityError:
        await callback.answer()


@router.message(Command("bookmarks"))
async def proceed_bookmarks(message: Message) -> None | Message:
    cur_uid = message.from_user.id  # pyright: ignore
    bookmarks = await db.show_bookmarks(cur_uid)
    if not bookmarks:
        return await message.answer(VOCABULARY_RU["no_bookmarks"])
    keyboard = create_bookmarks_kb(bookmarks)
    await message.answer(VOCABULARY_RU["/bookmarks"], reply_markup=keyboard)


@router.callback_query(Text("cancel"))
async def proceed_cancel(callback: CallbackQuery) -> None:
    await callback.message.edit_text(VOCABULARY_RU["continue"])  # pyright: ignore


@router.callback_query(Text("cancel_del"))
async def proceed_cancel_del(callback: CallbackQuery) -> None:
    cur_uid = callback.from_user.id  # pyright: ignore
    bookmarks = await db.show_bookmarks(cur_uid)
    keyboard = create_bookmarks_kb(bookmarks)
    await callback.message.edit_text(VOCABULARY_RU["/bookmarks"],  # pyright: ignore
                                     reply_markup=keyboard)


@router.callback_query(Text("edit_bookmarks"))
async def proceed_edit_bookmarks(callback: CallbackQuery) -> None | bool:
    cur_uid = callback.from_user.id  # pyright: ignore
    bookmarks = await db.show_bookmarks(cur_uid)
    if not bookmarks:
        return await callback.answer(VOCABULARY_RU["no_bookmarks"])
    keyboard = create_edit_kb(bookmarks)
    await callback.message.edit_text(VOCABULARY_RU["/bookmarks"],  # pyright: ignore
                                     reply_markup=keyboard)


@router.callback_query(IsBookmarkDelete())
async def proceed_bookmark_del(callback: CallbackQuery, page_number: int) -> None | bool:
    cur_uid = callback.from_user.id  # pyright: ignore
    bookmarks = await db.show_bookmarks(cur_uid, is_del=True, page_number=page_number)
    if not bookmarks:
        return await callback.message.edit_text(VOCABULARY_RU["no_bookmarks"])  # pyright: ignore
    keyboard = create_edit_kb(bookmarks)
    await callback.message.edit_text(VOCABULARY_RU["/bookmarks"],  # pyright: ignore
                                     reply_markup=keyboard)
