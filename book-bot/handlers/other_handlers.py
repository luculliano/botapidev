from aiogram import Router
from aiogram.types.message import Message

router = Router()


@router.message()
async def proceed_other(message: Message) -> None:
    await message.send_copy(message.chat.id, reply_to_message_id=message.message_id)
