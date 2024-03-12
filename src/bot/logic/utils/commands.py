from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_commands(bot: Bot):
    bot_commands = [
        BotCommand(
            command='start',
            description='Начало работы, приветствие'
        ),
        BotCommand(
            command='help',
            description='Помощь по функционалу'
        ),
    ]

    await bot.set_my_commands(bot_commands, BotCommandScopeDefault())
