# from unittest.mock import AsyncMock
#
# import pytest
#
# from src.bot.logic.handlers.simple import help_command
# from src.bot.logic.views import help_msg
#
#
# @pytest.mark.asyncio
# async def test_help_command():
#     message = AsyncMock()
#     await help_command(message)
#     text = help_msg()
#     message.answer.assert_called_with(text)
