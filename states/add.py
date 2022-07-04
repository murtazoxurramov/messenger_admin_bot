from aiogram.dispatcher.filters.state import StatesGroup, State

class AddState(StatesGroup):
    user_id = State()
    chan_id = State()
    user_name = State()
    