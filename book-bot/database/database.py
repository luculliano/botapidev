import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.joinpath("..")))

import aiosqlite
from config_data import logger
from config_data import SQLITE_DB_FILE, SQLITE_SCRIPT, HAM_ON_RYE_JSON
from services import get_book_data
import asyncio


class DataBase:
    def __init__(self, db_path: Path) -> None:
        self.db_path = db_path


    def _get_db_script(self) -> str:
        with open(SQLITE_SCRIPT, encoding="utf-8") as file:
            return file.read()


    async def init_db(self):
        """Inits database on startup with sql script execution"""
        async with aiosqlite.connect(self.db_path) as con:
            await con.executescript(self._get_db_script())
            await con.commit()
            logger.info("Database has been inited")


    async def init_book(self, book_id: int, path_to_book: Path) -> None:
        """Inits book's data in database"""
        async with aiosqlite.connect(self.db_path) as con:
            values = ((page_number, page_text, book_id) for page_number, page_text
                      in get_book_data(path_to_book).items())
            await con.executemany("insert into book_pages(page_number, "
                                  "page_text, book_id) values (?, ?, ?)", values)
            await con.commit()
            logger.info("Book's data has been inited")


    async def _check_user_in_db(self, tg_uid: int, con: aiosqlite.Connection) -> bool:
        res = await con.execute("select exists "
                                "(select 1 from users where tg_uid = ?)", (tg_uid,))
        is_user = await res.fetchone()
        return is_user[0]  # pyright: ignore


    async def init_user(self, tg_uid: int) -> tuple[int, None] | None:
        """Inits not existing user in database when /start"""
        async with aiosqlite.connect(self.db_path) as con:
            if not await self._check_user_in_db(tg_uid, con):
                await con.execute("insert into users(tg_uid, book_pages_id) values "
                                  "(?, (select book_pages_id from book_pages where "
                                  "book_id = ? and page_number = ?))", (tg_uid, 1, 1))
                await con.commit()
                logger.info("User has been inited")


    async def _fetch_last_page(self, tg_uid: int,
                               con: aiosqlite.Connection) -> None | aiosqlite.Row:
        """Fetches user's last page and it's text"""
        res = await con.execute("select page_number, page_text from users join "
                                "book_pages using(book_pages_id) "
                                "where tg_uid = ?", (tg_uid,))
        logger.info("Last page has been returned")
        return await res.fetchone()


    async def update_page(self, tg_uid: int, move: int, *, is_begin: bool, is_continue: bool):
        """Handles users's pages depending on command"""
        async with aiosqlite.connect(SQLITE_DB_FILE) as con:
            return await self._fetch_last_page(tg_uid, con)
            # try:
            #     if not is_continue:
            #         if not is_begin:
            #             await con.execute(
            #                 "update users set cur_page = cur_page + ? " "where tg_uid = ?",
            #                 (move, tg_uid),
            #             )
            #         else:
            #             await con.execute(
            #                 "update users set cur_page = ? where tg_uid = ?", (1, tg_uid)
            #             )
            #         await con.commit()
            #         logger.info("Page has been updated")
            #     # return await _fetch_last_page(tg_uid, con)
            # except aiosqlite.IntegrityError:
            #     return False


async def main() -> None:
    db = DataBase(SQLITE_DB_FILE)
    print(await db.update_page(444, 1, is_begin=True, is_continue=True))


asyncio.run(main())
