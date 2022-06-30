from aiogram import Dispatcher

from loader import dp
from .channel import IsChannel


if __name__ == "filters":
    dp.filters_factory.bind(IsChannel)
