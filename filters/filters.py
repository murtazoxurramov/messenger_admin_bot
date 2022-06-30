from aiogram import types
from aiogram.dispatcher.filters import BoundFilter


class IsChannel(BoundFilter):
    async def check(self, message: types.Message) -> bool:
        # return message.chat.type in (
        #     types.ChatType.CHANNEL,
        # )
        return message.chat.type in (
            types.ChatType.CHANNEL,
            types.ChatType.is_channel,
            
        )
        
class IsGroup(BoundFilter):
    async def check(self, message: types.Message) -> bool:
        return message.chat.type in (
            types.ChatType.GROUP,
            types.ChatType.SUPERGROUP,
        )