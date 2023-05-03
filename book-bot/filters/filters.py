import re
from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery


class IsNewBookmark(BaseFilter):
    def __call__(self, callback: CallbackQuery) -> bool:
        data = callback.data
        match = re.fullmatch(r"^(\d+)/\d+$", data if data is not None else "")
        return match.group(1).isdigit() if match else False
