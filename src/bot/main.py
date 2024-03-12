import asyncio

from aiogram import Dispatcher, F
from aiogram.filters import Command

from src.bot.logic.handlers.simple import start_command, help_command, link_handler, garbage_handler
from src.bot.logic.handlers.events import bot_start, bot_stop
from src.bot.logic.settings import bot


async def start():
    dp = Dispatcher()

    dp.startup.register(bot_start)
    dp.shutdown.register(bot_stop)

    dp.message.register(start_command, Command(commands='start'))
    dp.message.register(help_command, Command(commands='help'))

    dp.message.register(link_handler, F.text)
    dp.message.register(garbage_handler)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(start())
