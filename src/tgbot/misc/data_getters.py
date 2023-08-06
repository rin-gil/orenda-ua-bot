"""Функції, які повертають дані для показу в діалозі"""

from typing import Any

from aiogram_dialog import DialogManager

from tgbot.services.search import search


async def get_found_cities(dialog_manager: DialogManager, **kwargs: Any) -> dict:
    """Список міст"""
    found_cities: list[tuple] = await search.get_list_cities(
        city_name=dialog_manager.current_context().dialog_data["city_name"],
    )
    return {"cities": found_cities, "cities_found": bool(found_cities)}


async def get_found_districts(dialog_manager: DialogManager, **kwargs: Any) -> dict:
    """Список районів"""
    found_districts: list[tuple] = await search.get_list_districts(
        city_id=dialog_manager.current_context().dialog_data["city_id"],
        district_name=dialog_manager.current_context().dialog_data["district_name"],
    )
    return {"districts": found_districts, "districts_found": bool(found_districts)}


async def get_number_of_rooms(**kwargs: Any) -> dict:
    """Кількість кімнат"""
    rooms: tuple[tuple[str, str], ...] = (
        ("1", "209_f_1%2C209_t_1"),
        ("1-2", "209_f_1%2C209_t_2"),
        ("2", "209_f_2%2C209_t_2"),
        ("2-3", "209_f_2%2C209_t_3"),
        ("3", "209_f_3%2C209_t_3"),
        ("4+", "209_f_4"),
    )
    return {"rooms": rooms}


async def get_can_with_animals(**kwargs: Any) -> dict:
    """Наявність тварин"""
    animals: tuple[tuple[str, str], ...] = (
        ("🟢 Так", "%2C1670_1670"),
        ("🔴 Ні", ""),
    )
    return {"animals": animals}


async def get_from_owners_only(**kwargs: Any) -> dict:
    """Тільки від власників"""
    owners: tuple[tuple[str, str], ...] = (
        ("🟢 Так", "%2C1437_1436%3A"),
        ("🔴 Ні", ""),
    )
    return {"owners": owners}


async def get_search_results(dialog_manager: DialogManager, **kwargs: Any) -> dict:
    """Генерує результати пошуку оголошень"""
    search_ads_url: str = await search.get_search_link(dialog_data=dialog_manager.current_context().dialog_data)
    dialog_manager.current_context().dialog_data["search_url"] = search_ads_url
    return {
        "show_ads_url": search_ads_url.replace("node/searchEngine/v2/", "uk/search"),
        "if_ads_found": await search.check_if_ads_found(search_url=search_ads_url),
    }
