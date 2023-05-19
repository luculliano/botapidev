import asyncio
import logging
import sys

import asyncpg as pg
from sqlalchemy.ext.asyncio import create_async_engine

URL = "postgresql+asyncpg://www:mysecretpassword@localhost:5433/mydb"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    stream=sys.stdout,
    datefmt="%d.%m.%Y, %H:%M:%S",
)


async def connect_databse() -> None:
    engine = create_async_engine(URL, echo=True, future=True)
    async with engine.connect() as con:
        print(engine)


if __name__ == "__main__":
    asyncio.run(connect_databse())
