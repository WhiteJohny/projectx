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
            text='Foxnews',
            callback_data='news_fox'
        ),
        InlineKeyboardButton(
            text='news2',
            callback_data='news_2'
        ),
        InlineKeyboardButton(
            text='newsw3',
            callback_data='news_3'
        )
    ]
])
