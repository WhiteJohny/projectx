import asyncio

from aiogram import Dispatcher, F

from aiogram.filters import Command, StateFilter
from aiogram.methods import DeleteWebhook

from src.bot.logic.handlers.simple import start_command, help_command, garbage_handler, news_command,\
    rt_search_many_handler, rt_search_one_handler, nyp_search_many_handler, nyp_search_one_handler,\
    chinadaily_search_many_handler, chinadaily_search_one_handler, show_command

from src.bot.logic.handlers.events import bot_start, stop_command, mode_choosing, news_choosing_one, news_choosing_many,\
    callback_choosing, model_check, bot_stop, news_next

from src.bot.logic.settings import bot
from src.bot.logic.fsm import News

from src.model import model_init


async def start():
    dp = Dispatcher()

    dp.startup.register(bot_start)
    dp.shutdown.register(bot_stop)

    dp.message.register(start_command, Command(commands='start'))
    dp.message.register(help_command, Command(commands='help'))
    dp.message.register(news_command, Command(commands='news'))
    dp.message.register(stop_command, Command(commands='stop'))
    dp.message.register(show_command, Command(commands='show'))

    dp.message.register(rt_search_many_handler, F.text, StateFilter(News.choosing_rt_many))
    dp.message.register(rt_search_one_handler, F.text, StateFilter(News.choosing_rt_one))
    dp.message.register(chinadaily_search_many_handler, F.text, StateFilter(News.choosing_chinadaily_many))
    dp.message.register(chinadaily_search_one_handler, F.text, StateFilter(News.choosing_chinadaily_one))
    dp.message.register(nyp_search_many_handler, F.text, StateFilter(News.choosing_nyp_many))
    dp.message.register(nyp_search_one_handler, F.text, StateFilter(News.choosing_nyp_one))
    dp.message.register(garbage_handler)

    dp.callback_query.register(mode_choosing, F.data.startswith("mode_"), StateFilter(News.choosing_mode))
    dp.callback_query.register(news_choosing_many, F.data.startswith("news_"), StateFilter(News.choosing_mode_many))
    dp.callback_query.register(news_choosing_one, F.data.startswith("news_"), StateFilter(News.choosing_mode_one))
    dp.callback_query.register(callback_choosing, F.data.startswith("callback_"), StateFilter(News.choosing_callback))
    dp.callback_query.register(model_check, F.data.startswith("valid_"))
    dp.callback_query.register(news_next, F.data == "next")

    try:
        await bot(DeleteWebhook(drop_pending_updates=True))
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    model_init()
    asyncio.run(start())
