from aiogram import Router
from aiogram.filters import Command
from aiogram.types.message import Message

from config_data import logger
from vocabulary import VOCABULARY_RU

router = Router()


@router.message(Command("start"))
async def proceed_start(message: Message) -> None:
    cur_uid = message.from_user.id  # pyright: ignore
    answer = VOCABULARY_RU["/start"].format(
        greet="Здравствуйте", name=message.from_user.first_name  # pyright: ignore
    )
    await message.answer(answer)
    logger.info(f"/start from id={cur_uid} is handled")


@router.message(Command("help"))
async def proceed_help(message: Message) -> None:
    await message.answer(VOCABULARY_RU["/help"])
    logger.info(f"/help is handled")


@router.message()
async def proceed_other(message: Message) -> None:
    await message.send_copy(message.chat.id, reply_to_message_id=message.message_id)
