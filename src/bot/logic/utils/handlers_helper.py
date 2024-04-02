from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from src.bot.logic.fsm import News

from src.bot.logic.keyboards import callback_choose


async def search_one(parser, message: Message, state: FSMContext):
    text = parser(message.text)

    if "Ваша ссылка недействительна" in text:
        await state.clear()
        return await message.answer(text=text)
    else:
        await state.set_state(News.choosing_callback)
        return await message.reply(text=text, reply_markup=callback_choose)
