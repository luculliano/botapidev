import re
from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery


class IsBookmarkDelete(BaseFilter):
    """
    Filter to detect callback to delete page and
    return page number in handler
    """
    async def __call__(self, callback: CallbackQuery) -> dict[str, int]:
        match = re.fullmatch(r"^(\d+)del+$", callback.data)  # pyright: ignore
        return {"page_number": int(match.group(1))}


class IsUsebookmark(BaseFilter):
    """
    Filter to detect callback to use specified bookmark
    in bookmarks, returns page number in handler
    """
    async def __call__(self, callback: CallbackQuery) -> dict[str, int]:
        match = re.fullmatch(r"^(\d+)move+$", callback.data)  # pyright: ignore
        return {"page_number": int(match.group(1))}
