import logging
from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware

from data.config import CHAT_ID
from keyboards.inline.addchan import AddChan
from utils.misc.subscribtion import check
from loader import bot


class BigBrother(BaseMiddleware):
    async def on_pre_process_update(self, update: types.Update, data: dict):
        if update.message:
            user = update.message.from_user.id
        elif update.callback_query:
            user = update.callback_query.from_user.id
        else:
            return
        logging.info(user)
        final_status = True
        for channel in CHAT_ID:
            result = await check(user_id=user, channel=channel)

        final_status *= result

        if not final_status:
            text = f"Assalomu alaykum {update.message.from_user.full_name}!\n" \
                   f"Kanalga obuna bo'lmagansiz shu sababli habar yoza olmaysiz\n" \
                   f"Iltimos\n                     <b>Obuna bo'ling👇</b>"
            await update.message.reply(text=text, reply_markup=AddChan, disable_web_page_preview=True)
            raise CancelHandler()