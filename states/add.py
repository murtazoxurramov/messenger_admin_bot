from aiogram.dispatcher.filters.state import StatesGroup, State

class AddState(StatesGroup):
    user_id = State()
    chan_id = State()
    group_id = State()
    