"""Запускає бота"""

from asyncio import run

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from aiogram_dialog import DialogRegistry

from tgbot.config import Config, load_config, logger
from tgbot.controllers.dialog_handlers import register_dialog_handlers
from tgbot.controllers.other_handlers import register_other_handlers
from tgbot.misc.sheduler import schedule
from tgbot.services.database import Database
from tgbot.views.dialog import search_setup_dialog


def register_all_handlers(dp: Dispatcher) -> None:
    """Реєструє обробники"""
    register_dialog_handlers(dp)
    register_other_handlers(dp)


def register_dialog(dp: Dispatcher) -> None:
    """Реєструє діалог"""
    registry = DialogRegistry(dp)
    registry.register(search_setup_dialog)


async def main() -> None:
    """Запускає бота"""

    config: Config = load_config()
    bot: Bot = Bot(token=config.tg_bot.token)
    dp: Dispatcher = Dispatcher(bot=bot, storage=MemoryStorage())
    database: Database = Database(db_config=config.db)
    bot["db"] = database

    register_all_handlers(dp)
    register_dialog(dp)

    try:  # On starting bot
        await database.init()
        await schedule(dp)
        await dp.skip_updates()
        await dp.start_polling(bot)
    finally:  # On stopping bot
        await dp.storage.close()
        await dp.storage.wait_closed()
        session = await bot.get_session()
        await session.close()


if __name__ == "__main__":
    logger.info("Starting bot")
    try:
        run(main())
    except (KeyboardInterrupt, SystemExit):
        pass
    except Exception as ex:
        logger.critical("Unknown error: %s", ex)
    logger.info("Bot stopped!")
