import logging

from aiogram import Dispatcher

from data.config import CREATOR


async def on_startup_notify(dp: Dispatcher):
    try:
        await dp.bot.send_message(CREATOR, "Bot ishga tushdi")

    except Exception as err:
        logging.exception(err)
