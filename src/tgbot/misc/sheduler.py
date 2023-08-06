"""Виконання задач за розкладом"""

from aiogram import Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from tgbot.services.distribution import check_for_new_ads


async def schedule(dp: Dispatcher) -> None:
    """Створює завдання розсилки нових оголошень в планувальнику"""
    scheduler: AsyncIOScheduler = AsyncIOScheduler()
    scheduler.add_job(func=check_for_new_ads, trigger="cron", hour="*", minute="*/15", args=(dp,), timezone="UTC")
    scheduler.start()
