from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types.message import Message

from vocabulary import VOCABULARY_EN
from filters import AdminFIlter

router = Router()  # module level router

# router.message.filter(AdminFIlter())  # for all handlers

@router.message(CommandStart())
async def proceed_start(message: Message) -> None:
    await message.reply(VOCABULARY_EN["start"])


@router.message(Command("help"))
async def proceed_help(message: Message) -> None:
    await message.reply(VOCABULARY_EN["help"])

@router.message(Command("admin"), AdminFIlter())
async def proceed_admin(message: Message) -> None:
    await message.reply("admin")

@router.message()
async def proceed_other(message: Message) -> None:
    try:
        await message.send_copy(message.chat.id, reply_to_message_id=message.message_id)
    except TypeError:
        await message.reply(VOCABULARY_EN["no-echo"])
