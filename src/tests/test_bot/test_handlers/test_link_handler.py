from unittest.mock import AsyncMock

import pytest

from src.bot.logic.handlers.simple import link_handler
from src.bot.logic.views import bad_link_msg, good_link_msg


@pytest.mark.asyncio
async def test_link_handler():
    message = AsyncMock()
    await link_handler(message)
    b_text, g_text = bad_link_msg(), good_link_msg()
    message.answer.assert_called_with(b_text or g_text)
