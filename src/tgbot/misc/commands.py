"""Sets commands for the bot"""

from aiogram import Dispatcher
from aiogram.types import BotCommand


async def set_default_commands(dp: Dispatcher) -> None:
    """Задає команди бота"""
    await dp.bot.set_my_commands(
        commands=[
            BotCommand(command="start", description="▶️ Налаштувати пошук оголошень"),
            BotCommand(command="stop", description="️⏹ Зупинити розсилку та видалити дані"),
        ],
    )
