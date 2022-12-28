"""Описано основну бізнес-логіку роботи програми"""

from aiohttp import ClientError, ClientSession, ContentTypeError

from tgbot.models.dataclasses import AdShortInfo, AdDetailedInfo
from tgbot.models.formatter import Formatter
from tgbot.models.parser import Parser


class SearchADS:
    """Основна бізнес-логіка програми"""

    def __init__(self) -> None:
        self._formatter = Formatter()
        self._parser = Parser()

    @staticmethod
    async def _make_request(url: str) -> list[dict] | dict | None:
        """Виконує запит до сайту"""
        try:
            async with ClientSession() as session:
                async with session.get(url=url) as responce:
                    if responce.status == 200:
                        result: list[dict] | dict = await responce.json()
                        return result
        except (ClientError, ContentTypeError):
            return None
        else:
            return None

    async def get_list_cities(self, city_name: str) -> list[tuple]:
        """Повертає список знайдених міст з dom.ria.com за назвою міста"""
        url: str = await self._formatter.gen_city_search_link(city_name=city_name)
        raw_data: list[dict] | dict | None = await self._make_request(url=url)
        list_cities: list = []
        if raw_data and isinstance(raw_data, list):
            count: int = 0
            for raw_city_data in raw_data:
                parsed_city_data: tuple | None = await self._parser.parse_city_data(data=raw_city_data)
                if parsed_city_data:
                    list_cities.append(parsed_city_data)
                    count += 1
                    if count == 10:
                        break
        return list_cities

    async def get_list_districts(self, city_id: str, district_name: str) -> list[tuple]:
        """Повертає список знайдених районів з dom.ria.com за назвою району та ідентифікатором міста"""
        url: str = await self._formatter.gen_district_search_link(city_id=city_id, district_name=district_name)
        raw_data: list[dict] | dict | None = await self._make_request(url=url)
        list_districts: list = []
        if raw_data and isinstance(raw_data, list):
            count: int = 0
            for raw_district_data in raw_data:
                parsed_district_data: tuple | None = await self._parser.parse_district_data(data=raw_district_data)
                if parsed_district_data:
                    list_districts.append(parsed_district_data)
                    count += 1
                    if count == 10:
                        break
        return list_districts

    async def get_search_link(self, dialog_data: dict) -> str:
        """Повертає згенерований рядок пошуку оголошень"""
        return await self._formatter.gen_ads_search_link(dialog_data=dialog_data)

    async def check_if_ads_found(self, search_url: str) -> bool:
        """Перевіряє, чи існує хоча б одне оголошення за вказаними параметрами"""
        raw_data: list[dict] | dict | None = await self._make_request(url=search_url)
        if raw_data and isinstance(raw_data, dict):
            ads_count: int | None = await self._parser.parse_ads_count(data=raw_data)
            return bool(ads_count)
        return False

    async def get_ads_ids(self, search_url: str) -> list:
        """Повертає ідентифікатори знайдених оголошень"""
        raw_data: list[dict] | dict | None = await self._make_request(url=search_url)
        if raw_data and isinstance(raw_data, dict):
            ads_ids: list[int] | None = await self._parser.parse_ads_ids(data=raw_data)
            return ads_ids if ads_ids else []
        return []

    async def get_ad_by_id(self, ad_id: int) -> AdShortInfo | None:
        """Повертає інформацію про оголошення"""
        url: str = await self._formatter.gen_ad_link(ad_id=ad_id)
        raw_data: list[dict] | dict | None = await self._make_request(url=url)
        if raw_data and isinstance(raw_data, dict):
            parsed_data: AdDetailedInfo | None = await self._parser.parse_ad_data(data=raw_data)
            if parsed_data:
                return await self._formatter.gen_ad_info(ad_info=parsed_data)
        return None


search: SearchADS = SearchADS()
