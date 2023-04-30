from aiogram import Bot
from aiogram.types import BotCommand

from vocabulary import VOCABULARY_COMMANDS_RU


async def set_main_menu(bot: Bot) -> None:
    """Creates BotCommands using setMyCommands method"""
    main_menu_commands = [
        BotCommand(command=command, description=description)
        for command, description in VOCABULARY_COMMANDS_RU.items()
    ]
    await bot.set_my_commands(commands=main_menu_commands)
