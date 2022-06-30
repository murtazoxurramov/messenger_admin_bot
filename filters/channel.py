from aiogram import types
from aiogram.dispatcher.filters import BoundFilter


class IsChannel(BoundFilter):
    async def check(self, message: types.Message) -> bool:
        return message.chat.type in (
            types.ChatType.CHANNEL,
        )