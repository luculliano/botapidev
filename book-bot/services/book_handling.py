"""
This module has functions to split txt file by pages to use it as pagination.
It also has get_book_data function to extract json text with pages's numbers
to insert it in database
"""
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.joinpath("..")))

import json
import re

PAGE_SIZE = 320


def _get_cropped_text(text: str) -> str:
    """Removes useless \n strings from text of txt file"""
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


def make_book(txt_path: Path, json_path: Path) -> None:
    """Makes book in json format as page and it's text"""
    with open(txt_path, encoding="utf-8") as file:
        book = _split_text(_get_cropped_text(file.read()), PAGE_SIZE)
    with open(json_path, "w", encoding="utf-8") as file:
        json.dump(book, file, indent=3, ensure_ascii=False)


def get_book_data(path: Path) -> dict[str, str]:
    with open(path, encoding="utf-8") as file:
        return json.load(file)
