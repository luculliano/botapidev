from itertools import zip_longest

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from vocabulary import VOCABULARY_RU


def create_inline_kb(width: int = 3, *args, **kwargs) -> InlineKeyboardMarkup:
    """Generates specific width inline keyboard on the fly"""
    keyboard = []
    buttons = (InlineKeyboardButton(text=VOCABULARY_RU[button_data]
                            if button_data in VOCABULARY_RU else button_data,
                            callback_data=button_data) for button_data in args)
    for tpl in zip_longest(*(iter(buttons),)*width):
        keyboard.append(list(filter(None, tpl)))

    buttons = (InlineKeyboardButton(text=button_text, callback_data=button_data)
                                for button_data, button_text in kwargs.items())
    for tpl in zip_longest(*(iter(buttons),)*width):
        keyboard.append(list(filter(None, tpl)))

    return InlineKeyboardMarkup(inline_keyboard=keyboard)
