from aiogram.fsm.state import StatesGroup, State


class News(StatesGroup):
    choosing_mode = State()

    choosing_mode_one = State()
    choosing_mode_many = State()

    choosing_rt_one = State()
    choosing_chinadaily_one = State()
    choosing_nyp_one = State()

    choosing_rt_many = State()
    choosing_chinadaily_many = State()
    choosing_nyp_many = State()

    choosing_callback = State()

    stop = State()
