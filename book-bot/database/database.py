import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.joinpath("..")))

import asyncio
from typing import NamedTuple

import aiosqlite

from config_data import logger
from config_data import SQLITE_DB_FILE, SQLITE_SCRIPT
from services import get_book_data


class BookData(NamedTuple):
    page_number: int
    page_text: str
    book_length: int


class DataBase:
    def __init__(self, db_path: Path) -> None:
        self.db_path = db_path


    def __get_db_script(self) -> str:
        with open(SQLITE_SCRIPT, encoding="utf-8") as file:
            return file.read()


    async def init_db(self):
        """Inits database on startup with sql script execution"""
        async with aiosqlite.connect(self.db_path) as con:
            await con.executescript(self.__get_db_script())
            await con.commit()
            logger.info("Database has been inited")


    async def init_book(self, book_id: int, path_to_book: Path) -> None:
        """
        Inits book's data in database. It's used to add it's content
        in database only
        """
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
        """Inits not existing user when /start"""
        async with aiosqlite.connect(self.db_path) as con:
            if not await self._check_user_in_db(tg_uid, con):
                await con.execute("insert into users(tg_uid, book_pages_id) values "
                                  "(?, (select book_pages_id from book_pages where "
                                  "book_id = ? and page_number = ?))", (tg_uid, 1, 1))
                await con.commit()
                logger.info("User has been inited")


    async def _fetch_last_page(self, tg_uid: int,
                               con: aiosqlite.Connection) -> BookData:
        """Fetches user's last page, it's text and amount of pages"""
        # rewrite, count column
        res = await con.execute("select page_number, page_text, (select "
                                "count(page_number) from book_pages) from users "
                                "join book_pages using(book_pages_id) "
                                "where tg_uid = ?", (tg_uid,))
        row = await res.fetchone()
        return BookData(*row)  # pyright: ignore


    async def __move_begin(self, tg_uid: int, con: aiosqlite.Connection) -> None:
        await con.execute("update users set book_pages_id = "
                          "(select book_pages_id from book_pages where "
                          "page_number=? and book_id=(select book_id from "
                          "book_pages join users using(book_pages_id) where "
                          "tg_uid = ?)) where tg_uid = ?", (1, tg_uid, tg_uid))


    async def __move_page(self, tg_uid: int, con: aiosqlite.Connection, move: int) -> None:
        await con.execute("update users set book_pages_id = "
                          "(select book_pages_id from book_pages where "
                          "page_number=(select page_number from users join "
                          "book_pages using(book_pages_id) where "
                          "tg_uid = ?)+?) where tg_uid=?", (tg_uid, move, tg_uid))


    async def update_page(self, tg_uid: int, move: int = -1, *,
is_begin: bool | None = None, is_continue: bool | None = None) -> BookData:
        """Handles users's pages depending on command"""
        async with aiosqlite.connect(SQLITE_DB_FILE) as con:
            if not is_continue:
                if not is_begin:
                    await self.__move_page(tg_uid, con, move)
                else:
                    await self.__move_begin(tg_uid, con)
                await con.commit()
            return await self._fetch_last_page(tg_uid, con)

    async def _show_bookmarks(self, tg_uid: int) -> None:
        pass

async def main() -> None:
    db = DataBase(SQLITE_DB_FILE)
    print(await db.update_page(333, 1, is_begin=True, is_continue=False))


if __name__ == "__main__":
    asyncio.run(main())
