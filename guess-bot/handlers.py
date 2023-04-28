import re

from aiogram import Router
from aiogram.filters import Command
from aiogram.types.message import Message

from database import *
from settings import logger
from vocabulary import VOCABULARY_EN

router = Router()


@router.message(Command("start", "help"))
async def proceed_start(message: Message) -> None:
    cur_uid = message.from_user.id  # pyright: ignore
    greet = "Welcome back" if await init_user(cur_uid) else "Welcome"
    answer = VOCABULARY_EN["main"].format(
        greet=greet,
        name=message.from_user.first_name,  # pyright: ignore
    )
    await message.answer(answer)
    logger.info(f"/main from id={cur_uid} is handled.")


@router.message(Command("game"))
async def proceed_game(message: Message) -> None:
    cur_uid = message.from_user.id  # pyright: ignore
    data = await get_game_stat(cur_uid)
    if data.state == 1:
        await message.answer("Command /game not available in game mode.")
    else:
        await init_game(cur_uid)
        await message.answer("The number is picked. You have 5 attempts.")
    logger.info(f"/game from id={cur_uid} is handled.")


@router.message(Command("cancel"))
async def proceed_cancel(message: Message) -> None:
    cur_uid = message.from_user.id  # pyright: ignore
    data = await get_game_stat(cur_uid)
    if data.state == 0:
        await message.answer("Command /cancel is available in game mode only.")
    else:
        await cancel_game(cur_uid)
        await message.answer("The game has been stopped.")
    logger.info(f"/cancel from id={cur_uid} is handled.")


@router.message(Command("stat"))
async def proceed_stat(message: Message) -> None:
    cur_uid = message.from_user.id  # pyright: ignore
    await message.answer(await show_main_stat(cur_uid))
    logger.info(f"/stat from id={cur_uid} is handled.")


@router.message(lambda msg: msg.text and re.fullmatch(r"\d|\d\d|100", msg.text))
async def proceed_numbers(message: Message) -> None:
    cur_uid = message.from_user.id  # pyright: ignore
    data = await get_game_stat(cur_uid)
    if data.state == 1:
        return await define_number(cur_uid, message, data.attempts, data.secret_number)
    await message.answer("Please, use numbers in game mode only.")
    logger.info(f"number from id={cur_uid} is handled.")


@router.message()
async def proceed_other(message: Message) -> None:
    await message.answer(VOCABULARY_EN["other"])
