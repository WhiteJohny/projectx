from aiogram import Dispatcher

import pytest

from src.tests.test_bot.mocked_bot import MockedBot


@pytest.fixture()
def bot():
    return MockedBot()


@pytest.fixture()
async def dispatcher():
    dp = Dispatcher()
    await dp.emit_startup()
    try:
        yield dp
    finally:
        await dp.emit_shutdown()
