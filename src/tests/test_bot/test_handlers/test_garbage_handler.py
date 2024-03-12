from unittest.mock import AsyncMock

import pytest

from src.bot.logic.handlers.simple import garbage_handler
from src.bot.logic.views import garbage_msg


@pytest.mark.asyncio
async def test_garbage_handler():
    message = AsyncMock()
    await garbage_handler(message)
    text = garbage_msg()
    message.answer.assert_called_with(text)
