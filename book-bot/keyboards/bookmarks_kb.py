from itertools import zip_longest
from typing import Iterable

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import aiosqlite

from vocabulary import VOCABULARY_RU


def create_bookmarks_kb(bookmarks: Iterable[aiosqlite.Row],
                        width: int = 1) -> InlineKeyboardMarkup | None:
    """Generates inline keyboard for bookmarks on the fly"""
    keyboard = []
    buttons = (InlineKeyboardButton(text=f"{bookmark_data[0]} - {bookmark_data[1]}",
            callback_data=f"{bookmark_data[0]}move") for bookmark_data in bookmarks)
    for tpl in zip_longest(*(iter(buttons),)*width):
        keyboard.append(list(filter(None, tpl)))
    keyboard.append([InlineKeyboardButton(text=VOCABULARY_RU["edit_bookmarks"],
                                         callback_data="edit_bookmarks"),
                    InlineKeyboardButton(text=VOCABULARY_RU["cancel"],
                                         callback_data="cancel")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def create_edit_kb(bookmarks: Iterable[aiosqlite.Row],
                   width: int = 1) -> InlineKeyboardMarkup | None:
    """Generates inline keyboard for editing bookmarks on the fly"""
    keyboard = []
    buttons = (InlineKeyboardButton(
        text=f"{VOCABULARY_RU['del']} {bookmark_data[0]} - {bookmark_data[1]}",
        callback_data=f"{bookmark_data[0]}del") for bookmark_data in bookmarks)
    for tpl in zip_longest(*(iter(buttons),)*width):
        keyboard.append(list(filter(None, tpl)))
    keyboard.append([InlineKeyboardButton(text=VOCABULARY_RU["cancel"],
                                         callback_data="cancel_del")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
