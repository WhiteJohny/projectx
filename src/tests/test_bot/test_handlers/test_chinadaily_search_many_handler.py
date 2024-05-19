from unittest.mock import AsyncMock

import pytest

from src.model import get_news_sentiment_many
from src.bot.logic.handlers.simple import chinadaily_search_many_handler
from src.parser.parsers.ready.chinadaily_parser import chinadaily_many_parser


@pytest.mark.asyncio
async def test_chinadaily_search_many_handler():
    state = AsyncMock()
    message = AsyncMock()
    await chinadaily_search_many_handler(message, state)
    message.answer.assert_called_with(text=get_news_sentiment_many(chinadaily_many_parser(message.text)))
