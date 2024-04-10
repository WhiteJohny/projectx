"""
from unittest.mock import AsyncMock

import pytest

from src.bot.logic.settings import Secrets
from src.bot.logic.handlers.events import bot_start
from src.bot.logic.views import bot_start_msg


@pytest.mark.asyncio
async def test_bot_start(bot):
    await bot_start()
    text = bot_start_msg()
    assert bot.send_message(chat_id=Secrets.admin_id, text=text)
"""