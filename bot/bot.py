import asyncio
import logging
import time
from aiogram import Bot, Dispatcher, Router, types, F
from aiogram.filters import Command

import secrets
import utills


bot = Bot(token=secrets.TG_API_KEY,
          parse_mode="HTML")

router = Router()


@router.message(Command(commands=["start"]))
async def start_command(message: types.Message):
    chat_id = message.chat.id
    await bot.send_message(text=f"Приветствую👋, {message.from_user.full_name}!", chat_id=chat_id)
    time.sleep(0.5)
    await bot.send_message(text="Чтобы узнать, что я умею - напиши /help", chat_id=chat_id)


@router.message(Command(commands=["help"]))
async def help_command(message: types.Message):
    chat_id = message.chat.id
    await bot.send_message(text=f"Скинь мне ссылку на сайт новостей, а я расскажу тебе - плохие они или хорошие!", chat_id=chat_id)


@router.message(F.text)
async def link_handler(message: types.Message):
    chat_id = message.chat.id
    if utills.url_validation(message.text):
        await bot.send_message(text="Ваша ссылка работает!", chat_id=chat_id)
    else:
        await bot.send_message(text="Ваша ссылка недействительна!", chat_id=chat_id)


@router.message()
async def garbage(message: types.Message):
    await bot.send_message(text="Чтобы узнать, что я умею - напиши /help", chat_id=message.chat.id)


async def main():
    dp = Dispatcher()
    dp.include_router(router=router)

    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    )
    asyncio.run(main())
