"""This module contains functions for work with sqlite3"""

from secrets import randbelow
from typing import NamedTuple

from aiogram.types.message import Message
import aiohttp
import aiosqlite

from config import SQLITE_DB_FILE


__all__ = ["init_user",
           "init_game",
           "define_number",
           "show_main_stat",
           "cancel_game",
           "get_game_stat"]


class UserMainStat(NamedTuple):
    rank: int
    tg_uid: int
    tries: int
    memes: int
    perc: int


class UserGameStat(NamedTuple):
    attempts: int
    secret_number: int
    state: int


async def _check_user_in_db(con: aiosqlite.Connection,
                            tg_uid: int) -> aiosqlite.Row | None:
    res = await con.execute("SELECT * FROM users WHERE tg_uid = ?", (tg_uid,))
    return await res.fetchone()


async def _get_main_stat(tg_uid: int) -> UserMainStat:
    async with aiosqlite.connect(SQLITE_DB_FILE) as con:
        query = await con.execute(
            "SELECT * FROM ("
            "SELECT ROW_NUMBER() OVER (ORDER BY perc DESC, memes DESC) as rank, * "
            "FROM (SELECT tg_uid, tries, memes, "
            "ROUND(CAST(memes AS REAL) / tries * 100, 2) perc FROM users))"
            "WHERE tg_uid = ?",
            (tg_uid,),
        )
        res = await query.fetchone()
        return UserMainStat(*res)  # pyright: ignore


async def _update_attempt(tg_uid: int) -> None:
    async with aiosqlite.connect(SQLITE_DB_FILE) as con:
        await con.execute(
            "UPDATE users SET attempts = attempts - ? " "WHERE tg_uid = ?",
            (1, tg_uid),
        )
        await con.commit()


async def _get_random_meme() -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get("https://meme-api.com/gimme",
                               timeout=3) as response:
            result = await response.json()
            return result["url"]


async def _finish_game(tg_uid: int, is_win: bool) -> None:
    """Updates user's stat in database when game finishes"""
    async with aiosqlite.connect(SQLITE_DB_FILE) as con:
        data = (5, None, is_win, 0, tg_uid)
        await con.execute(
            "UPDATE users SET "
            "attempts = ?, secret_number = ?, "
            "memes = memes + ?, state = ? "
            "WHERE tg_uid = ?",
            data,
        )
        await con.commit()


async def init_db() -> None:
    """Inits database and creates table for users"""
    async with aiosqlite.connect(SQLITE_DB_FILE) as con:
        await con.execute(
            "CREATE TABLE IF NOT EXISTS users("
            "users_id INTEGER PRIMARY KEY AUTOINCREMENT,"
            "tg_uid INTEGER UNIQUE NOT NULL,"
            "attempts INTEGER,"
            "secret_number INTEGER,"
            "tries INTEGER,"
            "memes INTEGER,"
            "state INTEGER)"
        )
        await con.commit()


async def init_user(tg_uid: int) -> bool | None:
    """Inits user in database"""
    async with aiosqlite.connect(SQLITE_DB_FILE) as con:
        if await _check_user_in_db(con, tg_uid) is not None:
            return True
        data = (tg_uid, 5, None, 0, 0, 0)
        await con.execute(
            "INSERT INTO users("
            "tg_uid, attempts, secret_number, tries, memes, state)"
            "VALUES(?, ?, ?, ?, ?, ?)",
            data,
        )
        await con.commit()


async def init_game(tg_uid: int) -> None:
    """Modifies user's data in database when /game"""
    async with aiosqlite.connect(SQLITE_DB_FILE) as con:
        data = (1, randbelow(100), 1, 1, tg_uid)
        await con.execute(
            "UPDATE users SET "
            "attempts = attempts - ?, secret_number = ?, "
            "tries = tries + ?, state = ? "
            "WHERE tg_uid = ?",
            data,
        )
        await con.commit()


async def get_game_stat(tg_uid: int) -> UserGameStat:
    """Returns user's current game stat from database"""
    async with aiosqlite.connect(SQLITE_DB_FILE) as con:
        query = await con.execute(
            "SELECT attempts, secret_number, state " "FROM users WHERE tg_uid = ?",
            (tg_uid,),
        )
        res = await query.fetchone()
        return UserGameStat(*res)  # pyright: ignore


async def cancel_game(tg_uid: int) -> None:
    """Resets user's stat in database when /cancel"""
    async with aiosqlite.connect(SQLITE_DB_FILE) as con:
        data = (5, None, 1, 0, tg_uid)
        await con.execute(
            "UPDATE users SET "
            "attempts = ?, secret_number = ?, "
            "tries = tries - ?, state = ? "
            "WHERE tg_uid = ?",
            data,
        )
        await con.commit()


async def show_main_stat(tg_uid: int) -> str:
    """Returns user's stat from database"""
    user_stat = await _get_main_stat(tg_uid)
    return (
        "STATISTIC\n"
        f"UID: {user_stat.tg_uid}\n"
        f"Tries: {user_stat.tries}\n"
        f"Memes: {user_stat.memes} "
        f"({user_stat.perc if user_stat.perc is not None else 0}%) "
        f"#{user_stat.rank} by rating"
    )


async def _define_win(tg_uid: int, message: Message) -> None:
    try:
        await message.answer_photo(await _get_random_meme(),
                                "Congratulations! Here's the meme for you.")
    except Exception:
        await message.answer("Congratulations! You're right. (No meme, sorry...)")
    await _finish_game(tg_uid, True)


async def _define_attempts(attempts: int, tg_uid: int,
                           message: Message, secret_number: int, prompt: str) -> None:
    await _update_attempt(tg_uid)
    if attempts <= 0:
        await message.answer("No attempts have been left.\n"
                            f"The answer is {secret_number}.")
        await _finish_game(tg_uid, False)
    if attempts > 0:
        await message.reply(f"Too {prompt}. Try again [{attempts}].")


async def define_number(tg_uid: int, message: Message, attempts: int, secret_number: int):
    """Determines numbers in game mode"""
    msg = int(message.text)  # pyright: ignore
    if msg == secret_number:
        await _define_win(tg_uid, message)
    elif msg > secret_number:
        await _define_attempts(attempts, tg_uid, message, secret_number, "much")
    elif msg < secret_number:
        await _define_attempts(attempts, tg_uid, message, secret_number, "low")
