from aiogram import Bot
from aiogram.types import BotCommand
from vocabulary import VOCABULARY_COMMANDS_EN


async def set_main_menu(bot: Bot) -> None:
    """It creates BotCommands and uses setMyCommands method"""
    main_menu_commands = [
        BotCommand(command=command, description=description)
        for command, description in VOCABULARY_COMMANDS_EN.items()
    ]
    await bot.set_my_commands(commands=main_menu_commands)
