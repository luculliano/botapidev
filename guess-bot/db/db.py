import asyncio
from secrets import randbelow
from typing import NamedTuple

import aiohttp
import aiosqlite
from aiogram.types.message import Message

DB = "temp.db"


class CantGetUserStat(Exception):
    """Exception that raises when user isn't in DB database"""


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


async def get_game_stat(tg_uid: int) -> UserGameStat:
    async with aiosqlite.connect(DB) as con:
        query = await con.execute(
            "SELECT attempts, secret_number, state " "FROM users WHERE tg_uid = ?",
            (tg_uid,),
        )
        res = await query.fetchone()
        if res is None:
            raise CantGetUserStat
        return UserGameStat(*res)


async def _get_main_stat(tg_uid: int) -> UserMainStat:
    async with aiosqlite.connect(DB) as con:
        query = await con.execute(
            "SELECT * FROM ("
            "SELECT ROW_NUMBER() OVER (ORDER BY perc DESC, memes DESC) as rank, * "
            "FROM (SELECT tg_uid, tries, memes, "
            "ROUND(CAST(memes AS REAL) / tries * 100, 2) perc FROM users))"
            "WHERE tg_uid = ?",
            (tg_uid,),
        )
        res = await query.fetchone()
        if res is None:
            raise CantGetUserStat
        return UserMainStat(*res)


async def show_main_stat(tg_uid: int) -> str:
    """Function returns user's statistic from DB database"""
    user_stat = await _get_main_stat(tg_uid)
    return (
        "STATISTIC\n"
        f"UID: {user_stat.tg_uid}\n"
        f"Tries: {user_stat.tries}\n"
        f"Memes: {user_stat.memes} "
        f"({user_stat.perc if user_stat.perc is not None else 0}%) "
        f"#{user_stat.rank} by rating"
    )


async def create_table() -> None:
    """Function creates table for users data in DB database"""
    async with aiosqlite.connect(DB) as con:
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


async def _check_user_in_db(
    con: aiosqlite.Connection, tg_uid: int
) -> aiosqlite.Row | None:
    res = await con.execute("SELECT * FROM users WHERE tg_uid = ?", (tg_uid,))
    return await res.fetchone()


async def create_user(tg_uid: int) -> None:
    """Function enters not existing user in DB database when /start"""
    async with aiosqlite.connect(DB) as con:
        if await _check_user_in_db(con, tg_uid) is None:
            data = (tg_uid, 5, None, 0, 0, 0)
            await con.execute(
                "INSERT INTO users("
                "tg_uid, attempts, secret_number, tries, memes, state)"
                "VALUES(?, ?, ?, ?, ?, ?)",
                data,
            )
            await con.commit()


async def start_game(tg_uid: int) -> None:
    """Function modifies user data in DB database when /game"""
    async with aiosqlite.connect(DB) as con:
        data = (1, randbelow(100), 1, 1, tg_uid)
        await con.execute(
            "UPDATE users SET "
            "attempts = attempts - ?, secret_number = ?, "
            "tries = tries + ?, state = ? "
            "WHERE tg_uid = ?",
            data,
        )
        await con.commit()


async def finish_game(tg_uid: int, is_win: bool) -> None:
    """
    Function updates user's data in DB database
    when attempts = 0 or user guessed right
    """
    async with aiosqlite.connect(DB) as con:
        data = (5, None, is_win, 0, tg_uid)
        await con.execute(
            "UPDATE users SET "
            "attempts = ?, secret_number = ?, "
            "memes = memes + ?, state = ? "
            "WHERE tg_uid = ?",
            data,
        )
        await con.commit()


async def cancel_game(tg_uid: int) -> None:
    """Function resets previous user data in DB database when /cancel"""
    async with aiosqlite.connect(DB) as con:
        data = (5, None, 1, 0, tg_uid)
        await con.execute(
            "UPDATE users SET "
            "attempts = ?, secret_number = ?, "
            "tries = tries - ?, state = ? "
            "WHERE tg_uid = ?",
            data,
        )
        await con.commit()


async def _update_attempt(tg_uid: int) -> None:
    async with aiosqlite.connect(DB) as con:
        await con.execute(
            "UPDATE users SET attempts = attempts - ? " "WHERE tg_uid = ?",
            (1, tg_uid),
        )
        await con.commit()


async def _get_random_meme() -> str:
    """get random picture to send when user win"""
    async with aiohttp.ClientSession() as session:
        async with session.get("https://meme-api.com/gimme") as response:
            result = await response.json()
            return result["url"]


async def define_number(tg_uid: int, message: Message):
    """determine the user number in game mode"""
    msg = int(message.text)  # pyright: ignore
    data = await get_game_stat(tg_uid)
    if msg == data.secret_number:
        try:
            meme = await _get_random_meme()
            await message.answer_photo(
                meme, "Congratulations! Here's the meme for you."
            )
        except Exception:
            await message.answer("Congratulations! You're right. (No meme, sorry...)")
        await finish_game(tg_uid, True)

    elif msg > data.secret_number:
        attempts = data.attempts
        await _update_attempt(tg_uid)
        if attempts > 0:
            await message.reply(f"Too much. Try again [{attempts}].")
    elif msg < data.secret_number:
        attempts = data.attempts
        await _update_attempt(tg_uid)
        if attempts > 0:
            await message.reply(f"Too little. Try again [{attempts}].")
    if data.attempts <= 0:
        await message.answer(
            "No attempts have been left.\n" f"The answer is {data.secret_number}."
        )
        await finish_game(tg_uid, False)


async def main() -> None:
    await create_table()


if __name__ == "__main__":
    asyncio.run(main())
