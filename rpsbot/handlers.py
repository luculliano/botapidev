from secrets import choice

from aiogram import Router
from aiogram.filters import Command
from aiogram.filters.text import Text
from aiogram.types.message import Message

from keyboards import keyboard1, keyboard2

router = Router()


@router.message(Command("start"))
async def proceed_start(message: Message) -> None:
    await message.answer(
        "<b>Welcome!</b>\nI'm the bot powered by luculliano.\n"
        "Let's play Rock, Paper, Scissors?\n"
        "Use /help for more information.\n"
        "Wanna play?",
        parse_mode="HTML",
        reply_markup=keyboard1,
    )


@router.message(Command("help"))
async def proceed_help(message: Message) -> None:
    await message.answer(
        "<u>Rules:</u>\nI choose one of the Rock, Paper, Scissors "
        "along with you.\nYou have to choose one of them too.\n"
        "Let's play Rock, Paper, Scissors?\n",
        parse_mode="HTML",
        reply_markup=keyboard1,
    )


@router.message(Text("Let's go!"))
async def proceed_yes(message: Message) -> None:
    await message.answer("Great! You choose...", reply_markup=keyboard2)


@router.message(Text(text=("Rock 🗿", "Paper 📜", "Scissors ✂")))
async def proceed_choose(message: Message) -> None:
    src = "Rock", "Paper", "Scissors"
    bot_choice = choice(src)
    user_choice = message.text[:-2]  # pyright: ignore
    if bot_choice == user_choice:
        await message.answer(
            f"That's the draw!. Wanna play again?",
            reply_markup=keyboard1,
        )
    elif (
        src.index(bot_choice) - src.index(user_choice) == 1
        or src.index(bot_choice) - src.index(user_choice) == -2
    ):
        await message.answer(
            f"You loose! {bot_choice} beats {user_choice}. Wanna play again?",
            reply_markup=keyboard1,
        )
    else:
        await message.answer(
            f"You win! {user_choice} beats {bot_choice}. Wanna play again?",
            reply_markup=keyboard1,
        )


@router.message(Text("Not today!"))
async def proceed_no(message: Message) -> None:
    await message.answer('Got you. If you wanna play - press "Let\'s go" button.')


@router.message()
async def proceed_other(message: Message) -> None:
    await message.answer("Not supported. Use /help for help.")
