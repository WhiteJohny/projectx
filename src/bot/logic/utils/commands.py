from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault, BotCommandScopeChat

from src.bot.logic.settings import Secrets


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
        BotCommand(
            command='news',
            description='Выбор новостного сайта'
        ),
    ]
    bot_admin_commands = [
        BotCommand(
            command='stop',
            description='Прекращение работы бота'
        ),
        BotCommand(
            command='show',
            description='Взять новость в обработку'
        )
    ]
    bot_admin_commands.extend(bot_commands)

    await bot.set_my_commands(bot_commands, BotCommandScopeDefault())

    for admin in Secrets.admins_id.split(" "):
        await bot.set_my_commands(bot_admin_commands, BotCommandScopeChat(chat_id=int(admin)))
