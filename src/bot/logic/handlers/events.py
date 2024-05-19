import sys

from aiogram.types import CallbackQuery, Message, FSInputFile
from aiogram.fsm.context import FSMContext

from src.bot.logic.utils import commands, queue
from src.bot.logic.settings import bot
from src.bot.logic.views import bot_start_msg, bot_stop_msg
from src.bot.logic.settings import Secrets
from src.bot.logic.keyboards import news_choose, news_validation, news_check
from src.bot.logic.fsm import News


ERROR_LINKS = []
LINKS_QUEUE = queue.LinksQueue()


async def bot_start():
    await commands.set_commands(bot)
    return await bot.send_message(chat_id=Secrets.admin_id, text=bot_start_msg())


async def bot_stop():
    with open(r"src/model/error_links.txt", "w") as f:
        for link in set(ERROR_LINKS):
            f.write(f'{link}\n')

    file = FSInputFile(r"src/model/error_links.txt", "error_links.txt")

    try:
        await bot.send_document(chat_id=Secrets.admin_id, document=file, caption=bot_stop_msg())
    except Exception:
        await bot.send_message(chat_id=Secrets.admin_id, text=bot_stop_msg())


async def stop_command(message: Message):
    await bot.session.close()
    await sys.exit()


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
    elif news == 'cd':
        await state.set_state(News.choosing_chinadaily_one)
    else:
        await state.set_state(News.choosing_nyp_one)

    return await callback.message.answer(text='Отправьте ссылку на вашу новость')


async def news_choosing_many(callback: CallbackQuery, state: FSMContext):
    news = callback.data.split("_")[1]

    await callback.message.delete()

    if news == 'rt':
        await state.set_state(News.choosing_rt_many)
    elif news == 'cd':
        await state.set_state(News.choosing_chinadaily_many)
    else:
        await state.set_state(News.choosing_nyp_many)

    return await callback.message.answer(text='Введите ключевое слово(а)')


async def callback_choosing(callback: CallbackQuery, state: FSMContext):
    cb = callback.data.split("_")[1]
    ans = "✅"
    await state.clear()

    if cb == 'no':
        ans = "❌"
        msg_to_admin = f'{callback.message.text}\n{callback.message.reply_to_message.text}'
        LINKS_QUEUE.insert(msg_to_admin)

    return await callback.message.edit_text(text=f'{callback.message.text}\n{ans}')


async def model_check(callback: CallbackQuery):
    cb = callback.data.split("_")[1]
    ans = "Модель дала верный ответ 😌"
    link = callback.message.text.split("\n")[1]

    if link == LINKS_QUEUE.peek().split("\n")[1]:
        LINKS_QUEUE.pop()

        if cb == "error":
            ans = "Отправлено на дообучение модели ✅"
            ERROR_LINKS.append(link)

    return await callback.message.edit_text(text=f'{ans}\n{link}', reply_markup=news_check)


async def news_next(callback: CallbackQuery):
    text = LINKS_QUEUE.peek()

    await callback.message.edit_text(text=callback.message.text)

    if text is None:
        return await callback.message.answer(text="На данный момент необработанных новостей нет")

    return await callback.message.answer(text=text, reply_markup=news_validation)
