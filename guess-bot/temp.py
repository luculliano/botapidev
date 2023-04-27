import asyncio
from dataclasses import dataclass
from secrets import randbelow
from typing import NamedTuple

import aiosqlite

DB = "temp.db"
# user not found /start to sign up


class CantGetUserStat(Exception):
    """Exception that raises when user isn't in DB database"""


@dataclass
class UserMainStat:
    rank: int
    tg_uid: int
    tries: int
    memes: int
    perc: int

@dataclass
class UserGameStat:
    attempts: int
    secret_number: int
    state: int

@dataclass
class UserStat:
    tg_uid: int
    attempts: int
    secret_number: int
    tries: int
    memes: int
    state: int
    perc: int
    rank: int


async def _get_game_stat(con: aiosqlite.Connection, tg_uid: int) -> UserGameStat:
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
        f"Memes: {user_stat.memes} ({user_stat.perc}%) #{user_stat.rank} by rating"
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


async def create_user(tg_uid: int) -> None:
    """Function enters new user in DB database when /start"""
    async with aiosqlite.connect(DB) as con:
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
        data = await _get_game_stat(con, tg_uid)
        if data.state = 0:

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
    async with aiosqlite.connect(DB) as con:
        data = (5, None, 1, is_win, 0, tg_uid)
        await con.execute(
            "UPDATE users SET "
            "attempts = ?, secret_number = ?, tries = tries + ?, "
            "memes = memes + ?, state = ? "
            "WHERE tg_uid = ?",
            data,
        )
        await con.commit()


async def cancel_game(tg_uid: int) -> None:
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


async def main() -> None:
    await create_table()
    # await create_user(66)
    # await start_game(111)
    print(await show_stat(66))
    # await _get_user_game_stat(66)


if __name__ == "__main__":
    asyncio.run(main())
