from __future__ import annotations

import logging
import os

from aiogram import Bot
from dotenv import load_dotenv
from dataclasses import dataclass, field


logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter(
    "%(asctime)s - [%(levelname)s] -  %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s")

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)

file_handler = logging.FileHandler("logs.txt")
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)

logger.addHandler(console_handler)
logger.addHandler(file_handler)

load_dotenv()


@dataclass
class Secrets:
    bot_token: str = os.getenv("BOT_TOKEN")
    admins_id: str = os.getenv("ADMINS_ID")


bot = Bot(token=Secrets.bot_token, parse_mode='HTML')
