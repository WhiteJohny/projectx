"""
import pytest

from src.tests.test_bot.confitest import bot
from src.bot.logic.settings import Secrets
from src.bot.logic.handlers.events import bot_start
from src.bot.logic.views import bot_start_msg


@pytest.mark.asyncio
async def test_bot_start(bot):
    await bot_start()
    text = bot_start_msg()
    bot.send_message.assert_called_with(chat_id=Secrets.admin_id, text=text)
"""