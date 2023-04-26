import asyncio
from secrets import randbelow
import aiosqlite

DB = "temp.db"
# user not found /start to sign up
# select * from users where tg_uid=tg_uid; if res.fethone() is not None => ...

async def create_table() -> None:
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


async def show_stat(tg_uid: int) -> None:
    async with aiosqlite.connect(DB) as con:
        query = await con.execute(
            "SELECT * FROM ("
            "SELECT ROW_NUMBER() OVER (ORDER BY perc DESC, memes DESC) as row_number, * "
            "FROM (SELECT tg_uid, tries, memes, "
            "ROUND(CAST(memes AS REAL) / tries * 100, 2) perc FROM users))"
            "WHERE tg_uid = ?", (tg_uid,))
        res = await query.fetchone()
        print("STATISTIC\n"
             f"UID: {res[1]}\n"  # pyright: ignore
             f"Tries: {res[2]}\n"  # pyright: ignore
             f"Memes: {res[3]} ({res[4]}%) #{res[0]} by rating")  # pyright: ignore


async def main() -> None:
    await create_table()
    # await create_user(66)
    await start_game(111)


if __name__ == "__main__":
    asyncio.run(main())
