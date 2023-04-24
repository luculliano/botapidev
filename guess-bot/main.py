import asyncio
import logging
import re
from secrets import randbelow

import aiohttp
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types.message import Message

from config import TELEGRAM_BOT_TOKEN

bot = Bot(TELEGRAM_BOT_TOKEN)

dp = Dispatcher()

logging.basicConfig(level=logging.INFO)

users_db = {}


def _create_user(uid: int) -> None:
    users_db[uid] = {
        "state": 0,
        "tries": 0,
        "wins": 0,
        "secret_number": None,
        "attempts": 5,
    }


def _start_game(uid: int) -> None:
    users_db[uid]["state"] = 1
    users_db[uid]["tries"] += 1
    users_db[uid]["secret_number"] = randbelow(100)
    users_db[uid]["attempts"] -= 1
    print(users_db)


def _finish_game(uid: int, is_win: bool) -> None:
    users_db[uid]["state"] = 0
    users_db[uid]["attempts"] = 5
    if is_win:
        users_db[uid]["wins"] += 1


def _cancel_game(uid: int) -> None:
    users_db[uid]["state"] = 0
    users_db[uid]["tries"] -= 1
    users_db[uid]["attempts"] = 5


def _rate_user(uid: int) -> str:
    rating = {key: value["wins"] for key, value in users_db.items()}
    sorted_users = sorted(rating, key=lambda key: rating[key], reverse=True)
    return f"#{sorted_users.index(uid) + 1} by rating"


def _show_stat(uid: int) -> str:
    return (
        f"STATISTIC\n\n"
        f"UID: {uid}\n"
        f"Tries: {users_db[uid]['tries']}\n"
        f"Memes: {users_db[uid]['wins']} {_rate_user(uid)}"
    )


async def _define_number(uid: int, message: Message) -> None:
    """determine the user number in game mode"""
    msg = int(message.text)  # pyright: ignore

    if msg == users_db[uid]["secret_number"]:
        try:
            meme = await _get_random_meme()
            await message.answer_photo(
                meme, "Congratulations! Here's the meme for you."
            )
        except Exception:
            await message.answer("Congratulations! You're right. (No meme, sorry...)")
        _finish_game(uid, is_win=True)
    elif msg > users_db[uid]["secret_number"]:
        attempts = users_db[uid]["attempts"]
        users_db[uid]["attempts"] -= 1
        if attempts > 0:
            await message.reply(f"Too much. Try again [{attempts}].")
    elif msg < users_db[uid]["secret_number"]:
        attempts = users_db[uid]["attempts"]
        users_db[uid]["attempts"] -= 1
        if attempts > 0:
            await message.reply(f"Too low. Try again [{attempts}].")


async def _get_random_meme() -> str:
    """get random picture to send when user win"""
    async with aiohttp.ClientSession() as session:
        async with session.get("https://meme-api.com/gimme") as response:
            result = await response.json()
            return result["url"]


@dp.message(Command("start"))
async def proceed_start(message: Message) -> None:
    await message.answer(
        "Welcome!\nIt's a guess-bot powered by luculliano.\n"
        "To get the rules of the game and a list of available "
        "commands use /help."
    )

    cur_uid = message.from_user.id  # pyright: ignore
    if cur_uid not in users_db:
        _create_user(cur_uid)


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
async def proceed_play(message: Message) -> None:
    cur_uid = message.from_user.id  # pyright: ignore
    try:
        if users_db[cur_uid]["state"] == 1:
            await message.answer("Command /play not available in game mode.")
        else:
            await message.answer("The number is picked. You have 5 attempts.")
            _start_game(cur_uid)
        logging.info(users_db[cur_uid])
    except Exception:
        await message.answer(f"User {cur_uid} doesn't exist. Use /start to log in.")


@dp.message(Command("cancel"))
async def proceed_cancel(message: Message) -> None:
    cur_uid = message.from_user.id  # pyright: ignore
    try:
        if users_db[cur_uid]["state"] == 1:
            await message.answer("The game has been stopped.")
            _cancel_game(cur_uid)
        else:
            await message.answer("Command /cancel is available in game mode only.")
    except KeyError:
        await message.answer(f"User {cur_uid} doesn't exist. Use /start to log in.")


@dp.message(Command("stat"))
async def proceed_stat(message: Message) -> None:
    cur_uid = message.from_user.id  # pyright: ignore
    try:
        await message.answer(_show_stat(cur_uid))
    except KeyError:
        await message.answer(f"User {cur_uid} doesn't exist. Use /start to log in.")


@dp.message(lambda msg: msg.text and re.fullmatch(r"\d|\d\d|100", msg.text))
async def proceed_numbers(message: Message) -> None:
    cur_uid = message.from_user.id  # pyright: ignore

    if users_db[cur_uid]["state"] == 0:
        await message.answer("Please, use numbers in game mode only.")
        return

    await _define_number(cur_uid, message)

    if users_db[cur_uid]["attempts"] < 0:
        await message.answer(
            "No attempts have been left.\n"
            f"The answer is {users_db[cur_uid]['secret_number']}."
        )
        _finish_game(cur_uid, is_win=False)
        return


@dp.message()
async def proceed_other(message: Message) -> None:
    await message.answer("Not supported! Use /help for help.")


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
