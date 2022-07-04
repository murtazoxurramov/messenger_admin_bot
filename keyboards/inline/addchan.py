from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

AddChan = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Kanalga Obuna', url='http://t.me/devboysbot?startchannel=new')
        ],
        [
            InlineKeyboardButton(text='Obuna', callback_data='http://t.me/devboysbot?startchannel=new')
        ]
    ]
)