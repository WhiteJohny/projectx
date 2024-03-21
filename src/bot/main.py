import asyncio

from aiogram import Dispatcher, F

from aiogram.filters import Command, StateFilter
from aiogram.methods import DeleteWebhook

from src.bot.logic.handlers.simple import start_command, help_command, fox_search_many_handler, garbage_handler,\
    news_command, n2_search_many_handler, n2_search_one_handler, n3_search_many_handler, fox_search_one_handler, \
    n3_search_one_handler
from src.bot.logic.handlers.events import bot_start, bot_stop, mode_choosing, news_choosing_one, news_choosing_many
from src.bot.logic.settings import bot
from src.bot.logic.fsm import News


async def start():
    dp = Dispatcher()

    dp.startup.register(bot_start)
    dp.shutdown.register(bot_stop)

    dp.message.register(start_command, Command(commands='start'))
    dp.message.register(help_command, Command(commands='help'))
    dp.message.register(news_command, Command(commands='news'))

    dp.message.register(fox_search_many_handler, F.text, StateFilter(News.choosing_fox_many))
    dp.message.register(fox_search_one_handler, F.text, StateFilter(News.choosing_fox_one))
    dp.message.register(n2_search_many_handler, F.text, StateFilter(News.choosing_2_many))
    dp.message.register(n2_search_one_handler, F.text, StateFilter(News.choosing_2_one))
    dp.message.register(n3_search_many_handler, F.text, StateFilter(News.choosing_3_many))
    dp.message.register(n3_search_one_handler, F.text, StateFilter(News.choosing_3_one))
    dp.message.register(garbage_handler)

    dp.callback_query.register(mode_choosing, F.data.startswith("mode_"), StateFilter(News.choosing_mode))
    dp.callback_query.register(news_choosing_many, F.data.startswith("news_"), StateFilter(News.choosing_mode_many))
    dp.callback_query.register(news_choosing_one, F.data.startswith("news_"), StateFilter(News.choosing_mode_one))

    try:
        await bot(DeleteWebhook(drop_pending_updates=True))
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(start())
