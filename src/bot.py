"""Запускає бота"""

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils.executor import start_polling, start_webhook

from aiogram_dialog import DialogRegistry
from aiohttp import ClientSession

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


async def on_startup(dp: Dispatcher) -> None:
    """The functions that runs when the bot starts"""
    database: Database = dp.bot.get("db")
    config: Config = dp.bot.get("config")
    await database.init()
    await schedule(dp)
    # await set_default_commands(dp)
    if config.webhook:
        await dp.bot.set_webhook(
            url=f"{config.webhook.wh_host}/{config.webhook.wh_path}",
            drop_pending_updates=False,
            secret_token=config.webhook.wh_token,
        )


async def on_shutdown(dp: Dispatcher) -> None:
    """The functions that runs when the bot is stopped"""
    database: Database = dp.bot.get("db")
    config: Config = dp.bot.get("config")
    await dp.storage.close()
    await dp.storage.wait_closed()
    await database.close()
    if config.webhook:
        await dp.bot.delete_webhook()
        session: ClientSession = await dp.bot.get_session()
        await session.close()


def start_bot() -> None:
    """Запускає бота"""

    config: Config = load_config()
    bot: Bot = Bot(token=config.tg_bot.token)
    dp: Dispatcher = Dispatcher(bot=bot, storage=MemoryStorage())
    database: Database = Database(db_config=config.db)
    bot["config"] = config
    bot["db"] = database

    register_all_handlers(dp)
    register_dialog(dp)

    if config.webhook:
        start_webhook(
            dispatcher=dp,
            webhook_path=f"/{config.webhook.wh_path}",
            on_startup=on_startup,
            on_shutdown=on_shutdown,
            host=config.webhook.app_host,
            port=config.webhook.app_port,
        )
    else:
        start_polling(
            dispatcher=dp,
            on_startup=on_startup,
            on_shutdown=on_shutdown,
        )


if __name__ == "__main__":
    logger.info("Starting bot")
    try:
        start_bot()
    except (KeyboardInterrupt, SystemExit):
        pass
    except Exception as ex:
        logger.critical("Unknown error: %s", ex)
    logger.info("Bot stopped!")
