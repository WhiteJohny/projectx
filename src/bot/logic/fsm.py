from aiogram.fsm.state import StatesGroup, State


class News(StatesGroup):
    choosing_mode = State()

    choosing_mode_one = State()
    choosing_mode_many = State()

    choosing_fox_one = State()
    choosing_2_one = State()
    choosing_3_one = State()

    choosing_fox_many = State()
    choosing_2_many = State()
    choosing_3_many = State()
