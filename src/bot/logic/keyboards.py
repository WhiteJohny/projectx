from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


mode_choose = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='Анализ новости',
            callback_data='mode_one'
        ),
        InlineKeyboardButton(
            text='Анализ за 7 дней',
            callback_data='mode_many'
        )
    ]
])

news_choose = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='RT',
            callback_data='news_rt'
        ),
        InlineKeyboardButton(
            text='NN',
            callback_data='news_nn'
        ),
        InlineKeyboardButton(
            text='NYP',
            callback_data='news_nyp'
        )
    ]
])
