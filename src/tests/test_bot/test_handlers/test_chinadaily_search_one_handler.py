# from unittest.mock import AsyncMock
#
# import pytest
#
# from src.bot.logic.handlers.simple import chinadaily_search_one_handler
# from src.parser.parsers.ready.chinadaily_parser import chinadaily_one_parser
#
#
# @pytest.mark.asyncio
# async def test_chinadaily_search_one_handler():
#     state = AsyncMock()
#     message = AsyncMock()
#     await chinadaily_search_one_handler(message, state)
#     message.answer.assert_called_with(text=chinadaily_one_parser(message.text))
