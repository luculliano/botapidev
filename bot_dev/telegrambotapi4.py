"""bot that sends pictures"""
from typing import Any
import aiohttp
import asyncio
import os
import logging
import sys

TOKEN = os.getenv("TOKEN_BOT")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    stream=sys.stdout,
    datefmt="%d.%m.%Y, %H:%M:%S",
)


async def get_picture() -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(
            "https://api.thecatapi.com/v1/images/search"
        ) as response:
            response_json = await response.json()
            logging.info("get picture")
            return response_json[0]["url"]


async def getUpdates(offset: int) -> dict[Any, Any] | None:
    url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
    params = {"offset": offset + 1}
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            updates = await response.json()
            logging.info("get updates")
            try:
                return updates["result"][0]
            except IndexError:
                return None


async def parseUpdates(result: dict[Any, Any]) -> tuple[int, int]:
    offset = result["update_id"]
    chat_id = result["message"]["from"]["id"]
    return offset, chat_id


async def sendPhoto(chat_id: int, photo_link: str) -> None:
    url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"
    params = {"chat_id": chat_id, "photo": photo_link}
    async with aiohttp.ClientSession() as session:
        await session.get(url, params=params)
        logging.info("send photo")


async def main() -> None:
    # await get_picture()
    offset = -2
    while True:
        updates = await getUpdates(offset)
        if updates is not None:
            offset, chat_id = await parseUpdates(updates)
            photo = await get_picture()
            await sendPhoto(chat_id, photo)
        await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(main())
