from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

import pytest


from src.tests.test_bot.mocked_bot import MockedBot


@pytest.fixture()
async def memory_storage():
    storage = MemoryStorage()
    try:
        yield storage
    finally:
        await storage.close()


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
