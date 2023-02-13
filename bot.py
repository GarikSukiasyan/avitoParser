# -*- coding: utf-8 -*-

import logging
import threading
from aiogram import Bot, Dispatcher, executor, types
from tg_bot.config.config import bot, dp
from tg_bot.handlers.users import *
from parser.pasrer import pars




async def scheduled(wait_for):
    while True:
        await asyncio.sleep(wait_for)

        await pars()



# lis = db.get_all_id_user()
# print(lis)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(scheduled(120))  # поставим 10 секунд, в качестве теста
    executor.start_polling(dp, skip_updates=True)