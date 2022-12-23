"""Розсилка нових оголошень користувачам"""

from asyncio import sleep
from datetime import date, timedelta

from aiogram import Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.exceptions import BotBlocked, RetryAfter, UserDeactivated

from tgbot.models.database import database
from tgbot.models.dataclasses import AdShortInfo
from tgbot.models.search import search


async def check_for_new_ads(dp: Dispatcher) -> None:
    """Перевіряє наявність нових оголошень і надсилає їх користувачам"""
    async for user in database.get_users():
        _: tuple = user.search_url.partition("date_from=")
        new_search_url: str = f"{_[0]}date_from={date.today() - timedelta(days=60)}&date_to={date.today()}{_[2][29:]}"
        new_ads: set = set(await search.get_ads_ids(search_url=new_search_url))
        ads_to_send: set = new_ads.difference(user.ads_ids)
        for ad_id in ads_to_send:
            ad_info: AdShortInfo | None = await search.get_ad_by_id(ad_id=ad_id)
            if ad_info:
                try:
                    await dp.bot.send_message(
                        chat_id=user.id,
                        text=ad_info.description,
                        parse_mode="HTML",
                        reply_markup=InlineKeyboardMarkup(
                            inline_keyboard=[[InlineKeyboardButton(text="↗ Переглянути на сайті", url=ad_info.ad_url)]]
                        ),
                    )
                except (BotBlocked, UserDeactivated):
                    await database.delete_user(user_id=user.id)
                except RetryAfter as ex:
                    await sleep(ex.timeout)
                    await dp.bot.send_message(
                        chat_id=user.id,
                        text=ad_info.description,
                        parse_mode="HTML",
                        reply_markup=InlineKeyboardMarkup(
                            inline_keyboard=[[InlineKeyboardButton(text="↗ Переглянути на сайті", url=ad_info.ad_url)]]
                        ),
                    )
        await database.update_user_data(
            user_id=user.id,
            new_search_url=new_search_url,
            ads_to_delete=user.ads_ids.difference(new_ads),
            ads_to_save=ads_to_send,
        )
