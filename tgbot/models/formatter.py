"""Форматує різні дані в потрібну форму"""

from datetime import date, timedelta

from tgbot.models.dataclasses import AdDetailedInfo, AdShortInfo


class Formatter:
    """Форматує різні дані в потрібну форму"""

    _FIND_CITY_URL: str = "https://dom.ria.com/node/api/autocompleteCities"
    _FIND_DISTRICT_URL: str = "https://dom.ria.com/node/api/autocompleteLocations"
    _FIND_ADS_URL: str = "https://dom.ria.com/node/searchEngine/v2/"
    _AD_URL: str = "https://dom.ria.com/node/searchEngine/v2/view/realty/"

    @staticmethod
    async def _correct_user_input(user_input: str) -> str:
        """Видаляє з user_input все, крім букв і пробілів"""
        processed_input: str = ""
        for char in user_input[:26]:
            if char.isalpha():
                processed_input += char
            elif char.isspace() and (not processed_input or not processed_input[-1].isspace()):
                processed_input += char
        return processed_input

    async def gen_city_search_link(self, city_name: str) -> str:
        """Генерує посилання для пошуку міст на dom.ria.com"""
        return (
            f"{self._FIND_CITY_URL}"
            f"?labelName=output"
            f"&lang_id=4"
            f"&text={await self._correct_user_input(user_input=city_name)}"
        )

    async def gen_district_search_link(self, city_id: str, district_name: str) -> str:
        """Генерує посилання для пошуку районів на сайті dom.ria.com"""
        return (
            f"{self._FIND_DISTRICT_URL}"
            f"?type=simple"
            f"&labelName=name"
            f"&lang_id=4"
            f"&cityId={city_id}"
            f"&text={await self._correct_user_input(user_input=district_name)}"
        )

    async def gen_ads_search_link(self, dialog_data: dict) -> str:
        """Генерує посилання для пошуку оголошень на сайті dom.ria.com"""
        return (
            f"{self._FIND_ADS_URL}"
            f"?category=1"
            f"&realty_type=2"
            f"&operation=3"
            f"&sort=created_at"
            f"&photos_count_from=1"
            f"&limit=50"
            f"&state_id={dialog_data['state_id']}"
            f"&city_id={dialog_data['city_id']}"
            f"&d_id={dialog_data['district_id'] if dialog_data.get('district_id') else '0'}"
            f"&date_from={date.today() - timedelta(days=60)}"
            f"&date_to={date.today()}"
            f"&ch={dialog_data['rooms']}"
            f"%2C235_f_{dialog_data['min_price']}"
            f"%2C235_t_{dialog_data['max_price']}"
            f"{dialog_data['animals']}"
            f"{dialog_data['owners']}"
        )

    async def gen_ad_link(self, ad_id: int) -> str:
        """Генерує посилання на оголошення з сайту dom.ria.com"""
        return f"{self._AD_URL}{ad_id}?lang_id=4"

    @staticmethod
    async def gen_ad_info(ad_info: AdDetailedInfo) -> AdShortInfo:
        """Повертає коротку інформацію про оголошення"""
        title: str = f"{ad_info.rooms_count}к {ad_info.realty_type_name} на {ad_info.street_name}"
        area_total: str = f"Загальна площа {ad_info.area_total}м²" if ad_info.area_total else ""
        area_living: str = f", житлова {ad_info.area_living}м²" if ad_info.area_living else ""
        area_kitchen: str = f", кухня {ad_info.area_kitchen}м²" if ad_info.area_kitchen else ""
        description: str = (
            f'🏠 <b><a href="{ad_info.ad_url}">{title}</a>\n\n'
            f"{ad_info.price} грн.\n"
            f"{ad_info.floor}\n"
            f"{area_total}{area_living}{area_kitchen}\n\n</b>"
            f"{ad_info.description}"
        )
        return AdShortInfo(
            ad_url=ad_info.ad_url,
            description=description if len(description) < 1021 else f"{description[:1021]}...",
        )
