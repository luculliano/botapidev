"""longpooling"""

import os
from asyncio import run
from time import monotonic

import aiohttp

TOKEN = os.getenv("TOKEN_BOT")


async def do_something() -> None:
    print("Updated")


async def main() -> None:
    offset = -2
    while True:
        start = monotonic()
        async with aiohttp.ClientSession() as session:
            params = {"offset": offset + 1, "timeout": 60}
            async with session.get(
                f"https://api.telegram.org/bot{TOKEN}/getUpdates", params=params
            ) as response:
                updates = await response.json()
                if updates["result"]:
                    await do_something()
                    offset = updates["result"][0]["update_id"]
        print(f"Session uptime with Telegram server = {monotonic() - start} sec")


run(main())
