from unittest.mock import AsyncMock

import pytest

from src.bot.logic.handlers.simple import nyp_search_many_handler, get_news_sentiment_many
from src.parser.parsers.ready.nyp_parser import nyp_many_parser


@pytest.mark.asyncio
async def test_nyp_search_many_handler():
    state = AsyncMock()
    message = AsyncMock()
    await nyp_search_many_handler(message, state)
    message.answer.assert_called_with(text=get_news_sentiment_many(nyp_many_parser(message.text)))
