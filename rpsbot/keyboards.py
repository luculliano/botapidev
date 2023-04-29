from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


buttons1: list[KeyboardButton] = [
    KeyboardButton(text="Let's go!"),
    KeyboardButton(text="Not today!"),
]

keyboard1: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
    keyboard=[buttons1], resize_keyboard=True, one_time_keyboard=True
)


buttons2: list[list[KeyboardButton]] = [
    [KeyboardButton(text="Rock 🗿")],
    [KeyboardButton(text="Paper 📜")],
    [KeyboardButton(text="Scissors ✂")],
]

keyboard2: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
    keyboard=buttons2, resize_keyboard=True, one_time_keyboard=True
)
