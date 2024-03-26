from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from src.parser.parsers.for_bot.multy_parser import fox_many_parser, fox_one_parser
from src.bot.logic.views import garbage_msg, start_msg, help_msg, news_command_message
from src.bot.logic.keyboards import mode_choose
from src.bot.logic.fsm import News


async def fox_search_many_handler(message: Message, state: FSMContext):
    await state.clear()
    return await message.answer(text=fox_many_parser(message.text))


async def fox_search_one_handler(message: Message, state: FSMContext):
    await state.clear()
    return await message.answer(text=fox_one_parser(message.text))


async def n2_search_many_handler(message: Message, state: FSMContext):
    await state.clear()
    return await message.answer(text='К сожалению, этот сайт пока недоступен')


async def n2_search_one_handler(message: Message, state: FSMContext):
    await state.clear()
    return await message.answer(text='К сожалению, этот сайт пока недоступен')


async def n3_search_many_handler(message: Message, state: FSMContext):
    await state.clear()
    return await message.answer(text='К сожалению, этот сайт пока недоступен')


async def n3_search_one_handler(message: Message, state: FSMContext):
    await state.clear()
    return await message.answer(text='К сожалению, этот сайт пока недоступен')


async def garbage_handler(message: Message):
    return await message.answer(garbage_msg())


async def start_command(message: Message):
    return await message.answer(start_msg(message.from_user.full_name))


async def news_command(message: Message, state: FSMContext):
    await state.set_state(News.choosing_mode)
    return await message.answer(text=news_command_message(), reply_markup=mode_choose)


async def help_command(message: Message):
    return await message.answer(help_msg())
