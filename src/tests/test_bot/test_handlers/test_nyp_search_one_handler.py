# from unittest.mock import AsyncMock
#
# import pytest
#
# from src.model import get_news_sentiment_one
# from src.bot.logic.handlers.simple import nyp_search_one_handler
# from src.parser.parsers.ready.nyp_parser import nyp_one_parser
#
#
# @pytest.mark.asyncio
# async def test_nyp_search_one_handler():
#     state = AsyncMock()
#     message = AsyncMock()
#     await nyp_search_one_handler(message, state)
#     message.answer.assert_called_with(text=get_news_sentiment_one(nyp_one_parser(message.text)))
