from unittest.mock import AsyncMock

import pytest

from src.bot.logic.handlers.simple import rt_search_many_handler
from src.parser.parsers.ready.rt_parser import rt_many_parser


@pytest.mark.asyncio
async def test_rt_search_many_handler():
    state = AsyncMock()
    message = AsyncMock()
    await rt_search_many_handler(message, state)
    message.answer.assert_called_with(text=rt_many_parser(message.text))
