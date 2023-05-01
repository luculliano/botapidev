import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.joinpath("..")))

import json
from string import punctuation

import aiofiles

from config_data.config import HAM_ON_RYE_JSON, HAM_ON_RYE_TXT

PAGE_SIZE = 266


def _make_page(text: str, start: int, size: int) -> tuple[str, int]:
    page = text[start : start + size]
    if page[-1] in punctuation and page[-2] not in punctuation:
        return page, len(page)
    if page[-1] in punctuation and page[-2] in punctuation:
        return _make_page(page[:-2], start, size - 1)
    return _make_page(text, start, size - 1)


def _split_text(text: str) -> dict[int, str]:
    book: dict[int, str] = {}
    start, page_number = 0, 1
    while True:
        try:
            page_text, page_size = _make_page(text, start, PAGE_SIZE)
            book.setdefault(page_number, page_text.lstrip())
            page_number += 1
            start += page_size
        except IndexError:
            return book


def make_book() -> None:
    """Makes book in json format as page and it's text"""
    with open(HAM_ON_RYE_TXT, encoding="utf-8") as file:
        text = file.read()
        book = _split_text(text)
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
