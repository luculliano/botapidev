import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.joinpath("..")))
import re
import json

import aiofiles

from config_data.config import HAM_ON_RYE_JSON, HAM_ON_RYE_TXT

PAGE_SIZE = 320


def _get_cropped_text(text: str) -> str:
    cropped_text = re.sub(r"\n\s{1,}\n", "\n", text)
    return cropped_text


def _get_page_text(text: str, start: int, size: int) -> str:
    return text[start : start + size]


def _split_text(text: str, size: int) -> dict[int, str]:
    content = {}
    start, page_number = 0, 1
    while start < len(text):
        content.setdefault(page_number, _get_page_text(text, start, size))
        page_number += 1
        start += PAGE_SIZE
    return content


def make_book() -> None:
    """Makes book in json format as page and it's text"""
    with open(HAM_ON_RYE_TXT, encoding="utf-8") as file:
        book = _split_text(_get_cropped_text(file.read()), PAGE_SIZE)
    with open(HAM_ON_RYE_JSON, "w", encoding="utf-8") as file:
        json.dump(book, file, indent=3, ensure_ascii=False)


async def get_text_of_page(page_number: str) -> str:
    """Returns text by page number"""
    async with aiofiles.open(HAM_ON_RYE_JSON, encoding="utf-8") as file:
        content = await file.read()
        return json.loads(content)[page_number]


async def get_book_length() -> int:
    """Returns text by page number"""
    async with aiofiles.open(HAM_ON_RYE_JSON, encoding="utf-8") as file:
        content = await file.read()
        return len(json.loads(content))


if __name__ == "__main__":
    make_book()
