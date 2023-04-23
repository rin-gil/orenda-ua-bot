"""Інші обробники"""

from aiogram import Dispatcher
from aiogram.types import Message, Update, ContentType
from aiogram.utils.exceptions import TelegramAPIError

from aiogram_dialog import DialogManager, StartMode
from aiogram_dialog.exceptions import UnknownIntent

from tgbot.config import logger
from tgbot.misc.states import SearchSetup
from tgbot.models.database import database


async def other_type_handler(message: Message, dialog_manager: DialogManager) -> None:
    """
    Видаляє всі введені користувачем дані, які не мають відношення до діалогу

    Якщо користувача немає в базі даних, запускає новий діалог
    """
    await message.delete()
    if not await database.check_if_user_exists(user_id=message.from_user.id):
        await dialog_manager.start(state=SearchSetup.input_city_name, mode=StartMode.RESET_STACK)


async def error_handler(update: Update, exception: TelegramAPIError, dialog_manager: DialogManager) -> bool:
    """Обробка помилки UnknownIntent та запуск нового діалогового вікна налаштування пошуку"""
    if isinstance(exception, UnknownIntent):
        await update.callback_query.answer(text="❌ Дані застаріли", cache_time=1)
        await update.callback_query.message.delete()
        await dialog_manager.start(state=SearchSetup.input_city_name, mode=StartMode.RESET_STACK)
    else:
        logger.error(
            "When processing the update with id=%s there was a unhandled error: %s", update.update_id, repr(exception)
        )
    return True


def register_other_handlers(dp: Dispatcher) -> None:
    """Реєструє інші обробники"""
    dp.register_message_handler(callback=other_type_handler, content_types=ContentType.ANY, state=None)
    dp.register_errors_handler(callback=error_handler)
