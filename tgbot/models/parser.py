"""Парсинг сирих даних з dom.ria.com"""

from tgbot.models.dataclasses import AdDetailedInfo


class Parser:
    """Парсинг сирих даних з dom.ria.com"""

    @staticmethod
    async def parse_city_data(data: dict) -> tuple | None:
        """Парсить дані про міста з відповіді dom.ria.com

        Повертає кортеж, де перший елемент - назва міста,
        другий - ідентифікатор міста та області, розділені символом &."""
        try:
            if not data["payload"].get("areaId"):
                return f"{data['text']}", f"{data['payload']['cityId']}&{data['payload']['stateId']}"
        except KeyError:
            return None
        else:
            return None

    @staticmethod
    async def parse_district_data(data: dict) -> tuple | None:
        """Парсить дані про райони з відповіді dom.ria.com

        Повертає кортеж, де перший елемент - назва району,
        другий - ідентифікатор району"""
        try:
            if data.get("areaId"):
                return f"{data['name']}", f"{data['areaId']}"
        except KeyError:
            return None
        else:
            return None

    @staticmethod
    async def parse_ads_count(data: dict) -> int | None:
        """Парсить кількість знайдених оголошень з dom.ria.com"""
        return data.get("count")

    @staticmethod
    async def parse_ads_ids(data: dict) -> list[int] | None:
        """Парсить ідентифікатори знайдених оголошень з dom.ria.com"""
        return data.get("items")

    @staticmethod
    async def parse_ad_data(data: dict) -> AdDetailedInfo | None:
        """Парсить дані про оголошення з dom.ria.com"""
        try:
            ad_url: str = f"https://dom.ria.com/uk/{data['beautiful_url']}"
            rooms_count: int = data["rooms_count"]
            realty_type_name: str = (
                data["realty_type_name_uk"] if data.get("realty_type_name_uk") else data["realty_type_name"]
            )
            street_name: str = data["street_name_uk"] if data.get("street_name_uk") else data["street_name"]
            floor: str = data["floor_info"]
            price: str = data["priceArr"]["3"]
            area_total: int | None = data["total_square_meters"] if data.get("total_square_meters") else None
            area_living: int | None = data["living_square_meters"] if data.get("living_square_meters") else None
            area_kitchen: int | None = data["kitchen_square_meters"] if data.get("kitchen_square_meters") else None
            description: str = data["description_uk"] if data.get("description_uk") else data["description"]
            return AdDetailedInfo(
                ad_url=ad_url,
                rooms_count=rooms_count,
                realty_type_name=realty_type_name.casefold(),
                street_name=street_name,
                floor=floor,
                price=price,
                area_total=area_total,
                area_living=area_living,
                area_kitchen=area_kitchen,
                description=" ".join(description.splitlines()),
            )
        except (KeyError, TypeError, ValueError):
            return None
