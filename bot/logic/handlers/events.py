from bot.logic.utils.commands import set_commands
from bot.logic.settings import bot
from bot.logic.views import bot_start_msg, bot_stop_msg
from bot.logic.settings import Secrets


async def bot_start():
    await set_commands(bot)
    await bot.send_message(chat_id=Secrets.admin_id, text=bot_start_msg())


async def bot_stop():
    await bot.send_message(chat_id=Secrets.admin_id, text=bot_stop_msg())
