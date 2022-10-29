import asyncio

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor

from tgbot import load_config
from tgbot.handlers import register_commands, register_callbacks, register_messages
from tgbot.models import db_init
from tgbot.services.sheduler import schedule

config = load_config()
bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
dp = Dispatcher(bot, storage=MemoryStorage())
bot['config'] = config


async def on_startup(_):
    await db_init()
    register_commands(dp)
    register_callbacks(dp)
    register_messages(dp)
    asyncio.create_task(schedule())


async def on_shutdown(_):
    await dp.storage.close()
    await dp.storage.wait_closed()
    await bot.session.close()


def main():
    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown, skip_updates=True)


if __name__ == '__main__':
    main()
