from aiogram import Router
from aiogram.filters import Command
from aiogram.filters.text import Text
from aiogram.types import CallbackQuery
from aiogram.types.message import Message

from config_data import logger
from database import users_db
from keyboards import create_inline_kb
from services import get_book_length, get_text_of_page
from vocabulary import VOCABULARY_RU

router = Router()


@router.message(Command("start"))
async def proceed_start(message: Message) -> None:
    cur_uid = message.from_user.id  # pyright: ignore
    users_db[cur_uid] = 1
    answer = VOCABULARY_RU["/start"].format(
        greet="Здравствуйте", name=message.from_user.first_name  # pyright: ignore
    )
    await message.answer(answer)
    logger.info(f"/start from id={cur_uid} is handled")


@router.message(Command("help"))
async def proceed_help(message: Message) -> None:
    await message.answer(VOCABULARY_RU["/help"])
    logger.info(f"/help is handled")


@router.message(Command("beginning"))
async def proceed_beginning(message: Message) -> None:
    cur_uid = message.from_user.id  # pyright: ignore
    users_db[cur_uid] = 1
    text = await get_text_of_page("1")
    keyboard = create_inline_kb(
        3, "backward", f"1/{await get_book_length()}", "forward"
    )
    await message.answer(text, reply_markup=keyboard)


@router.callback_query(Text("backward"))
async def proceed_backward(callback: CallbackQuery) -> None | bool:
    cur_uid = callback.from_user.id  # pyright: ignore
    if users_db[cur_uid] == 1:
        return await callback.answer()
    users_db[cur_uid] -= 1
    text = await get_text_of_page(str(users_db[cur_uid]))
    keyboard = create_inline_kb(
        3, "backward", f"{users_db[cur_uid]}/{await get_book_length()}", "forward"
    )
    await callback.message.edit_text(text=text, reply_markup=keyboard)  # pyright: ignore


@router.callback_query(Text("forward"))
async def proceed_forward(callback: CallbackQuery) -> None | bool:
    cur_uid = callback.from_user.id  # pyright: ignore
    book_length = await get_book_length()
    if users_db[cur_uid] == await get_book_length():
        return await callback.answer()
    users_db[cur_uid] += 1
    text = await get_text_of_page(str(users_db[cur_uid]))
    keyboard = create_inline_kb(
        3, "backward", f"{users_db[cur_uid]}/{book_length}", "forward"
    )
    await callback.message.edit_text(text=text, reply_markup=keyboard)  # pyright: ignore
