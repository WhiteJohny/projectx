from aiogram.types import Message

from bot.logic.utils.url_validation import url_validation
from bot.logic.views import good_link_msg, bad_link_msg, garbage_msg, start_msg, help_msg


async def link_handler(message: Message):
    if url_validation(message.text):
        await message.answer(good_link_msg())
    else:
        await message.answer(bad_link_msg())


async def garbage_handler(message: Message):
    await message.answer(garbage_msg())


async def start_command(message: Message):
    await message.answer(start_msg(message.from_user.full_name))


async def help_command(message: Message):
    await message.answer(help_msg())
