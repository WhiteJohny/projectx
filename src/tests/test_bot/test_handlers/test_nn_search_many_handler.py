# from unittest.mock import AsyncMock
#
# import pytest
#
# from src.bot.logic.handlers.simple import nn_search_many_handler
# from src.parser.parsers.ready.nn_parser import nn_many_parser
#
#
# @pytest.mark.asyncio
# async def test_nn_search_many_handler():
#     state = AsyncMock()
#     message = AsyncMock()
#     await nn_search_many_handler(message, state)
#     message.answer.assert_called_with(text=nn_many_parser(message))
