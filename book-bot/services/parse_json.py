import re

from aiogram.types import InlineKeyboardMarkup

def parse_page_number(reply_markup: InlineKeyboardMarkup) -> tuple[int, int]:
    page_number = reply_markup.dict()["inline_keyboard"][0][1]["text"]
    match = re.fullmatch(r"(\d+)/(\d+)", page_number)
    return tuple(map(int, match.groups()))
