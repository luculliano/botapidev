from aiogram import Router
from aiogram.filters import Command
from aiogram.filters.text import Text
from aiogram.types import CallbackQuery
from aiogram.types.message import Message

from database import init_user, update_page
from keyboards import create_inline_kb
from services import get_book_length, get_text_of_page
from vocabulary import VOCABULARY_RU

router = Router()


@router.message(Command("start"))
async def proceed_start(message: Message) -> None:
    cur_uid = message.from_user.id  # pyright: ignore
    answer = VOCABULARY_RU["/start"].format(
        greet="С возвращением" if await init_user(cur_uid) else "Здравствуйте",
        name=message.from_user.first_name  # pyright: ignore
    )
    await message.answer(answer)


@router.message(Command("help"))
async def proceed_help(message: Message) -> None:
    await message.answer(VOCABULARY_RU["/help"])


@router.message(Command("beginning"))
async def proceed_beginning(message: Message) -> None:
    cur_uid = message.from_user.id  # pyright: ignore
    book_page = await update_page(cur_uid, -1, is_begin=True, is_continue=False)
    text = await get_text_of_page(str(book_page))
    keyboard = create_inline_kb(
        3, "backward", f"1/{await get_book_length()}", "forward"
    )
    await message.answer(text, reply_markup=keyboard)


@router.message(Command("continue"))
async def proceed_continue(message: Message) -> None | bool:
    cur_uid = message.from_user.id  # pyright: ignore
    book_page = await update_page(cur_uid, 1, is_begin=False, is_continue=True)
    text = await get_text_of_page(str(book_page))
    keyboard = create_inline_kb(
        3, "backward", f"{book_page}/{await get_book_length()}", "forward"
    )
    await message.answer(text, reply_markup=keyboard)  # pyright: ignore


@router.callback_query(Text("backward"))
async def proceed_backward(callback: CallbackQuery) -> None | bool:
    cur_uid = callback.from_user.id  # pyright: ignore
    book_page = await update_page(cur_uid, -1, is_begin=False, is_continue=False)
    if not book_page:
        return await callback.answer()
    text = await get_text_of_page(str(book_page))
    keyboard = create_inline_kb(
        3, "backward", f"{book_page}/{await get_book_length()}", "forward"
    )
    await callback.message.edit_text(text=text, reply_markup=keyboard)  # pyright: ignore


@router.callback_query(Text("forward"))
async def proceed_forward(callback: CallbackQuery) -> None | bool:
    cur_uid = callback.from_user.id  # pyright: ignore
    book_page = await update_page(cur_uid, 1, is_begin=False, is_continue=False)
    if not book_page:
        return await callback.answer()
    text = await get_text_of_page(str(book_page))
    keyboard = create_inline_kb(
        3, "backward", f"{book_page}/{await get_book_length()}", "forward"
    )
    await callback.message.edit_text(text=text, reply_markup=keyboard)  # pyright: ignore
