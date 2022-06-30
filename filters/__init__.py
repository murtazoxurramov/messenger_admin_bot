from aiogram import Dispatcher

from loader import dp
from filters.filters import IsChannel
from filters.filters import IsGroup


if __name__ == "filters":
    dp.filters_factory.bind(IsChannel)
    dp.filters_factory.bind(IsGroup)
