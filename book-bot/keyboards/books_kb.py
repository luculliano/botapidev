from itertools import zip_longest
from typing import Iterable

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from database import BookInfo
from vocabulary import VOCABULARY_RU


def create_books_kb(books: Iterable[BookInfo], width: int = 1) -> InlineKeyboardMarkup:
    keyboard = []
    buttons = (InlineKeyboardButton(text=f"{book.book_name}, {book.release_date}",
            callback_data=f"{book.book_id}book") for book in books)
    for tpl in zip_longest(*(iter(buttons),)*width):
        keyboard.append(list(filter(None, tpl)))
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def create_book_kb(book_id, width: int = 2, *args) -> InlineKeyboardMarkup:
    keyboard = []
    buttons = (InlineKeyboardButton(text=VOCABULARY_RU[button_data]
                        if button_data in VOCABULARY_RU else button_data,
                        callback_data=f"{book_id}{button_data}") for button_data in args)
    for tpl in zip_longest(*(iter(buttons),)*width):
        keyboard.append(list(filter(None, tpl)))

    return InlineKeyboardMarkup(inline_keyboard=keyboard)
