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
            text='RussiaToday',
            callback_data='news_rt'
        )
    ],
    [
        InlineKeyboardButton(
            text='ChinaDaily',
            callback_data='news_cd'
        )
    ],
    [
        InlineKeyboardButton(
            text='NYP',
            callback_data='news_nyp'
        )
    ]
])

callback_choose = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='ДА',
            callback_data='callback_yes'
        ),
        InlineKeyboardButton(
            text='НЕТ',
            callback_data='callback_no'
        )
    ]
])

news_validation = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='Ошибка модели',
            callback_data='valid_error'
        ),
        InlineKeyboardButton(
            text='Модель верна',
            callback_data='valid_pass'
        )
    ]
])
