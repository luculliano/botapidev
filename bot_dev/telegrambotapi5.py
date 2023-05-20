import asyncio
import logging
import os
import sys
from typing import Any

import aiohttp

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s; %(levelname)s; %(funcName)s",
    stream=sys.stdout,
    datefmt="%d.%m.%Y, %H:%M:%S",
)


class PictureBot:
    """bot that sends pictures"""

    def __init__(self) -> None:
        self.__TOKEN = os.getenv("TOKEN_BOT")
        self.offset = -2

    async def _get_photo(self) -> str | None:
        """get picture from third-party api"""

        url = "https://api.thecatapi.com/v1/images/search"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                logging.info("")
                # content type=None to avoid aiohttp.client_exceptions.ContentTypeError
                try:
                    result = await response.json()
                    return result[0]["url"]
                except Exception:
                    pass

    async def getUpdates(self, session: aiohttp.ClientSession) -> list[Any]:
        """check queries/updates from telegram server to bot as long pooling"""

        url = f"https://api.telegram.org/bot{self.__TOKEN}/getUpdates"
        params = {"offset": self.offset + 1, "timeout": 60}
        async with session.get(url, params=params) as response:
            logging.info("")
            updates = await response.json()
            return updates["result"]

    async def _parseUpdates(self, result: dict[Any, Any]) -> tuple[int, int]:
        """export offset and chat_id from updates"""

        offset = result["update_id"]
        chat_id = result["message"]["from"]["id"]
        return offset, chat_id

    async def sendPhoto(self, chat_id: int, session: aiohttp.ClientSession) -> None:
        """reply as picture from queries to bot"""

        url = f"https://api.telegram.org/bot{self.__TOKEN}/sendPhoto"
        photo_link = await self._get_photo()
        if photo_link is None:
            await self.sendMessage(chat_id, session)
        else:
            params = {"chat_id": chat_id, "photo": photo_link}
            logging.info("")
            await session.get(url, params=params)

    async def sendMessage(self, chat_id: int, session: aiohttp.ClientSession) -> None:
        """reply as text from queries to bot if no picture"""

        url = f"https://api.telegram.org/bot{self.__TOKEN}/sendMessage"
        params = {"chat_id": chat_id, "text": "Error picture"}
        logging.info("")
        await session.get(url, params=params)

    async def main(self) -> None:
        while True:
            async with aiohttp.ClientSession() as session:
                updates = await self.getUpdates(session)
                if updates:
                    self.offset, chat_id = await self._parseUpdates(updates[0])
                    await self.sendPhoto(chat_id, session)


if __name__ == "__main__":
    bot = PictureBot()
    asyncio.run(bot.main())
