from aiogram.dispatcher.filters.state import StatesGroup, State

class MessageState(StatesGroup):
    msg = State()
    msg_id = State()
    time = State()
    user_id = State()
    chan_id = State()
    