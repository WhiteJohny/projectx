from unittest.mock import AsyncMock

import pytest

from src.bot.logic.handlers.simple import fox_search_many_handler
from src.parser.parsers.for_bot.multy_parser import fox_many_parser


@pytest.mark.asyncio
async def test_fox_search_many_handler():
    state = AsyncMock()
    message = AsyncMock()
    await fox_search_many_handler(message, state)
    message.answer.assert_called_with(text=fox_many_parser(message.text))
