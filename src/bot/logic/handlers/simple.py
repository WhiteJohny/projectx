from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from src.parser.parsers.ready.rt_parser import rt_one_parser, rt_many_parser
from src.parser.parsers.ready.chinadaily_parser import chinadaily_one_parser, chinadaily_many_parser
from src.parser.parsers.ready.nyp_parser import nyp_one_parser, nyp_many_parser

from src.bot.logic.utils.handlers_helper import search_one
from src.bot.logic.views import garbage_msg, start_msg, help_msg, news_command_message
from src.bot.logic.keyboards import mode_choose, news_validation
from src.bot.logic.fsm import News
from src.bot.logic.handlers.events import LINKS_QUEUE


"""
FOX
from src.parser.parsers.fox_parser import fox_many_parser, fox_one_parser


async def fox_search_many_handler(message: Message, state: FSMContext):
    await state.clear()
    return await message.answer(text=fox_many_parser(message.text))


async def fox_search_one_handler(message: Message, state: FSMContext):
    return await search_one(parser=fox_one_parser, message=message, state=state)
"""

"""
NN
from src.parser.parsers.ready.nn_parser import nn_one_parser, nn_many_parser


async def nn_search_many_handler(message: Message, state: FSMContext):
    await state.clear()
    return await message.answer(text=nn_many_parser(message.text))


async def nn_search_one_handler(message: Message, state: FSMContext):
    return await search_one(parser=nn_one_parser, message=message, state=state)
"""


async def rt_search_many_handler(message: Message, state: FSMContext):
    await state.clear()
    return await message.answer(text=rt_many_parser(message.text))


async def rt_search_one_handler(message: Message, state: FSMContext):
    return await search_one(parser=rt_one_parser, message=message, state=state)


async def chinadaily_search_many_handler(message: Message, state: FSMContext):
    await state.clear()
    return await message.answer(text=chinadaily_many_parser(message.text))


async def chinadaily_search_one_handler(message: Message, state: FSMContext):
    return await search_one(parser=chinadaily_one_parser, message=message, state=state)


async def nyp_search_many_handler(message: Message, state: FSMContext):
    await state.clear()
    return await message.answer(text=nyp_many_parser(message.text))


async def nyp_search_one_handler(message: Message, state: FSMContext):
    return await search_one(parser=nyp_one_parser, message=message, state=state)


async def garbage_handler(message: Message):
    return await message.answer(garbage_msg())


async def start_command(message: Message):
    return await message.answer(start_msg(message.from_user.full_name))


async def news_command(message: Message, state: FSMContext):
    await state.set_state(News.choosing_mode)
    return await message.answer(text=news_command_message(), reply_markup=mode_choose)


async def help_command(message: Message):
    return await message.answer(help_msg())


async def show_command(message: Message):
    text = LINKS_QUEUE.peek()

    if text is None:
        return await message.answer(text="На данный момент необработанных новостей нет")

    return await message.answer(text=text, reply_markup=news_validation)
