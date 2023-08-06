"""Розсилка нових оголошень користувачам"""

from asyncio import sleep

from aiogram import Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.exceptions import BotBlocked, RetryAfter, UserDeactivated

from tgbot.services.database import Database
from tgbot.services.dataclasses import AdShortInfo
from tgbot.services.search import search


async def check_for_new_ads(dp: Dispatcher) -> None:
    """Перевіряє наявність нових оголошень і надсилає їх користувачам"""
    database: Database = dp.bot.get("db")
    async for user in database.get_users():
        new_ads: set = set(await search.get_ads_ids(search_url=user.search_url))
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
            ads_to_delete=user.ads_ids.difference(new_ads),
            ads_to_save=ads_to_send,
        )
