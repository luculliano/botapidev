import asyncio
import logging
import re

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types.message import Message

from config import TELEGRAM_BOT_TOKEN
from db import (
    CantGetUserStat,
    cancel_game,
    create_table,
    create_user,
    define_number,
    get_game_stat,
    show_main_stat,
    start_game,
)

bot = Bot(TELEGRAM_BOT_TOKEN)

dp = Dispatcher()

logging.basicConfig(level=logging.INFO)


@dp.message(Command("start"))
async def proceed_start(message: Message) -> None:
    await message.answer(
        "Welcome!\nIt's a guess-bot powered by luculliano.\n"
        "To get the rules of the game and a list of available "
        "commands use /help."
    )

    cur_uid = message.from_user.id  # pyright: ignore
    await create_user(cur_uid)


@dp.message(Command("help"))
async def proceed_help(message: Message) -> None:
    await message.answer(
        "I pick a number from 0 to 100.\n"
        "If you guess the number for 5 attempts "
        "I'll send you fun meme.\n\n"
        "Available commands:\n"
        "/game - to start playing\n"
        "/cancel - to cancel game\n"
        "/stat - to show stat\n"
        "/help - to show this message\n\n"
    )


@dp.message(Command("game"))
async def proceed_game(message: Message) -> None:
    cur_uid = message.from_user.id  # pyright: ignore
    try:
        data = await get_game_stat(cur_uid)
        if data.state == 1:
            await message.answer("Command /game not available in game mode.")
        else:
            await message.answer("The number is picked. You have 5 attempts.")
            await start_game(cur_uid)
            logging.info(data)
    except CantGetUserStat:
        await message.answer(f"User {cur_uid} doesn't exist. Use /start to log in.")


@dp.message(Command("cancel"))
async def proceed_cancel(message: Message) -> None:
    cur_uid = message.from_user.id  # pyright: ignore
    try:
        data = await get_game_stat(cur_uid)
        if data.state == 1:
            await cancel_game(cur_uid)
            await message.answer("The game has been stopped.")
        else:
            await message.answer("Command /cancel is available in game mode only.")
    except CantGetUserStat:
        await message.answer(f"User {cur_uid} doesn't exist. Use /start to log in.")


@dp.message(Command("stat"))
async def proceed_stat(message: Message) -> None:
    cur_uid = message.from_user.id  # pyright: ignore
    try:
        await message.answer(await show_main_stat(cur_uid))
    except CantGetUserStat:
        await message.answer(f"User {cur_uid} doesn't exist. Use /start to log in.")


@dp.message(lambda msg: msg.text and re.fullmatch(r"\d|\d\d|100", msg.text))
async def proceed_numbers(message: Message) -> None:
    cur_uid = message.from_user.id  # pyright: ignore

    try:
        data = await get_game_stat(cur_uid)
        if data.state == 0:
            await message.answer("Please, use numbers in game mode only.")
            return
        await define_number(cur_uid, message)
    except CantGetUserStat:
        await message.answer(f"User {cur_uid} doesn't exist. Use /start to log in.")


@dp.message()
async def proceed_other(message: Message) -> None:
    await message.answer("Not supported! Use /help for help.")


async def main() -> None:
    await create_table()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
