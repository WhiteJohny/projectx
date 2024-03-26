from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext


from src.bot.logic.utils.commands import set_commands
from src.bot.logic.settings import bot
from src.bot.logic.views import bot_start_msg, bot_stop_msg
from src.bot.logic.settings import Secrets
from src.bot.logic.keyboards import news_choose
from src.bot.logic.fsm import News


async def bot_start():
    await set_commands(bot)
    return await bot.send_message(chat_id=Secrets.admin_id, text=bot_start_msg())


async def bot_stop():
    return await bot.send_message(chat_id=Secrets.admin_id, text=bot_stop_msg())


async def mode_choosing(callback: CallbackQuery, state: FSMContext):
    mode = callback.data.split("_")[1]

    await callback.message.delete()

    if mode == "one":
        await state.set_state(News.choosing_mode_one)
    else:
        await state.set_state(News.choosing_mode_many)

    return await callback.message.answer(text="Выберите новостной сайт", reply_markup=news_choose)


async def news_choosing_one(callback: CallbackQuery, state: FSMContext):
    news = callback.data.split("_")[1]

    await callback.message.delete()

    if news == 'rt':
        await state.set_state(News.choosing_rt_one)
    elif news == 'nn':
        await state.set_state(News.choosing_nn_one)
    elif news == 'nyp':
        await state.set_state(News.choosing_nyp_one)

    return await callback.message.answer(text='Отправьте ссылку на вашу новость')


async def news_choosing_many(callback: CallbackQuery, state: FSMContext):
    news = callback.data.split("_")[1]

    await callback.message.delete()

    if news == 'rt':
        await state.set_state(News.choosing_rt_many)
    elif news == 'nn':
        await state.set_state(News.choosing_nn_many)
    elif news == 'nyp':
        await state.set_state(News.choosing_nyp_many)

    return await callback.message.answer(text='Введите ключевое слово(а)')
