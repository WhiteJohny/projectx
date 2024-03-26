from aiogram.fsm.state import StatesGroup, State


class News(StatesGroup):
    choosing_mode = State()

    choosing_mode_one = State()
    choosing_mode_many = State()

    choosing_rt_one = State()
    choosing_nn_one = State()
    choosing_nyp_one = State()

    choosing_rt_many = State()
    choosing_nn_many = State()
    choosing_nyp_many = State()
