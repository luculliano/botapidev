import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.joinpath("..")))

import aiosqlite
from config_data import logger
from config_data import SQLITE_DB_FILE, SQLITE_SCRIPT
import asyncio


__all__ = ["init_db", "init_user",
           "update_page", "fetch_last_page"]


async def get_db() -> aiosqlite.Connection:
    if not hasattr(get_db, "con"):
        get_db.con = await aiosqlite.connect(SQLITE_DB_FILE)
    return get_db.con


def _get_script(path_to_script: Path) -> str:
    with open(path_to_script, encoding="utf-8") as file:
        return file.read()


async def init_db() -> None:
    """Inits database on startup"""
    con = await get_db()
    await con.executescript(_get_script(SQLITE_SCRIPT))
    await con.commit()
    logger.info("Database has been inited")
    await con.close()


async def _check_user_in_db(tg_uid: int,
                            con: aiosqlite.Connection) -> None | aiosqlite.Row:
    res = await con.execute("select * from users where tg_uid = ?", (tg_uid,))
    return await res.fetchone()


async def init_user(tg_uid: int) -> tuple[int, None] | None:
    """Init not existing user in database when /start"""
    con = await get_db()
    if await _check_user_in_db(tg_uid, con) is not None:
        return 1, await con.close()
    await con.execute("insert into users(tg_uid, cur_page) values (?, ?)",
                      (tg_uid, 1))
    await con.commit()
    logger.info("User has been inited")
    await con.close()


async def update_page(tg_uid: int, move: int, is_begin: bool = False) -> None:
    """Saves last user's page when forward and backward buttons in use"""
    con = await get_db()
    try:
        if is_begin:
            await con.execute("update users set cur_page = ? where tg_uid = ?",
                              (1, tg_uid))
            logger.info("Beginning page has been returned")
        else:
            await con.execute("update users set cur_page = cur_page + ? "
                              "where tg_uid = ?", (move, tg_uid))
        await con.commit()
    except aiosqlite.IntegrityError:
        pass
    await con.close()


async def fetch_last_page(tg_uid: int) -> int:
    """Fetches user's last page when /continue"""
    async with aiosqlite.connect(SQLITE_DB_FILE) as con:
        res = await con.execute("select cur_page from users where tg_uid = ?",
                                (tg_uid,))
        logger.info("Last page has been returned")
        fetch_page = await res.fetchone()
        return fetch_page[0]  # pyright: ignore


async def main() -> None:
    print(await init_user(777))


asyncio.run(main())
