import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.joinpath("..")))

import asyncio
from typing import Iterable, NamedTuple

import aiosqlite

from config_data import logger
from config_data import SQLITE_SCRIPT
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


    async def __fetch_last_page(self, tg_uid: int,
                               con: aiosqlite.Connection) -> BookData:
        """Fetches user's last page, it's text and amount of pages"""
        res = await con.execute("select page_number, page_text, page_amount "
                                "from users join book_pages using(book_pages_id)"
                                "join book using(book_id) "
                                "where tg_uid = ?", (tg_uid,))
        row = await res.fetchone()
        return BookData(*row)  # pyright: ignore


    async def __fetch_bookmark(self, tg_uid: int,
                        con: aiosqlite.Connection,  page_number: int) -> BookData:
            res = await con.execute("select page_number, page_text, page_amount "
                                    "from bookmarks join book_pages using(book_pages_id)"
                                    "join book using(book_id) join users using(users_id) "
                                    "where tg_uid = ? and page_number = ?",
                                    (tg_uid, page_number))
            row = await res.fetchone()
            book_data = BookData(*row)  # pyright: ignore
            await con.execute("update users set book_pages_id = (select book_pages_id "
                              "from book_pages where page_number=? and book_id=?) "
                              "where tg_uid=?", (book_data.page_number, 1, tg_uid))
            await con.commit()
            return book_data


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
is_begin: bool | None = None, is_continue: bool | None = None,
is_bookmark: bool | None = None, page_number: int | None = None) -> BookData:
        """Handles users's pages depending on command"""
        async with aiosqlite.connect(self.db_path) as con:
            if not is_continue:
                if not is_begin:
                    await self.__move_page(tg_uid, con, move)
                else:
                    await self.__move_begin(tg_uid, con)
                await con.commit()
            return await (self.__fetch_bookmark(tg_uid, con, page_number) if \
        is_bookmark and page_number else self.__fetch_last_page(tg_uid, con))


    async def __delete_bookmark(self, tg_uid: int, con: aiosqlite.Connection,
                              page_number: int) -> None:
            await con.execute("delete from bookmarks where users_id=(select "
                              "users_id from users where tg_uid = ?) and "
                              "book_pages_id = (select book_pages_id from "
                              "book_pages where page_number = ?)",
                              (tg_uid, page_number))
            await con.commit()
            logger.info("Bookmark has been deleted")


    async def show_bookmarks(self, tg_uid: int, *, is_del: bool = False,
                             page_number: int | None = None) -> Iterable[aiosqlite.Row]:
        async with aiosqlite.connect(self.db_path) as con:
            if is_del and page_number:
                await self.__delete_bookmark(tg_uid, con, page_number)
            res = await con.execute("select page_number, page_text from "
                                    "book_pages join bookmarks using"
                                    "(book_pages_id) join users using(users_id) "
                                    "where tg_uid = ?", (tg_uid,))
            return await res.fetchall()


    async def add_bookmark(self, tg_uid: int) -> None:
        async with aiosqlite.connect(self.db_path) as con:
            await con.execute("insert into bookmarks(book_pages_id, users_id) "
                              "select book_pages_id, users_id from users "
                              "where tg_uid = ?", (tg_uid,))
            await con.commit()
            logger.info("Bookmark has been added")


async def main() -> None:
    pass


if __name__ == "__main__":
    asyncio.run(main())
