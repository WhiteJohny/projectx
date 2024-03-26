# from unittest.mock import AsyncMock
#
# import pytest
#
# from src.bot.logic.handlers.simple import fox_search_one_handler
# from src.parser.parsers.ready.fox_parser import fox_one_parser
#
#
# @pytest.mark.asyncio
# async def test_fox_search_one_handler():
#     state = AsyncMock()
#     message = AsyncMock()
#     await fox_search_one_handler(message, state)
#     message.answer.assert_called_with(text=fox_one_parser(message.text))
