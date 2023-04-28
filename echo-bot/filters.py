from aiogram.filters import BaseFilter
from aiogram.types.message import Message

from config import ADMINS


class AdminFIlter(BaseFilter):
    """Filter to determine admin by id"""

    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in map(  # pyright: ignore
            int, filter(lambda x: x.isdigit(), ADMINS.split(","))
        )
