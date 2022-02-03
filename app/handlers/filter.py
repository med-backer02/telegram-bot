from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from app import dp

class NoArgs(BoundFilter):
    key = "no_args"

    def __init__(self, no_args):
        self.no_args = no_args

    async def check(self, message: types.Message):
        if not len(message.text.split(" ")) > 1:
            return True

class OnlyPM(BoundFilter):
    key = "only_pm"

    def __init__(self, only_pm):
        self.only_pm = only_pm

    async def check(self, message: types.Message):
        if message.from_user.id == message.chat.id:
            return True

dp.filters_factory.bind(OnlyPM)
dp.filters_factory.bind(NoArgs)