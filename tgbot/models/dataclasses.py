"""Класи даних, які використовуються у програмі"""

from typing import NamedTuple


class User(NamedTuple):
    """Інформація про користувача"""

    id: int
    search_url: str
    ads_ids: set[int]


class AdShortInfo(NamedTuple):
    """Інформація про оголошення"""

    ad_url: str
    description: str


class AdDetailedInfo(NamedTuple):
    """Детальна інформація про оголошення"""

    ad_url: str
    rooms_count: int
    realty_type_name: str
    street_name: str
    floor: str
    price: str
    area_total: int | None
    area_living: int | None
    area_kitchen: int | None
    description: str
