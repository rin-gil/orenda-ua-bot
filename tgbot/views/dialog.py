"""Показ діалогів у програмі"""

from operator import itemgetter

from aiogram.types import ContentType
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button, Column, Select, SwitchTo, Url
from aiogram_dialog.widgets.media import StaticMedia
from aiogram_dialog.widgets.text import Case, Const, Format

from tgbot.config import BOT_LOGO
from tgbot.controllers.dialog_handlers import (
    any_other_messages,
    not_choosing_district,
    on_close,
    on_start,
    reset_search,
    save_can_with_animals,
    save_city_name,
    save_district_name,
    save_from_owners_only,
    save_max_price,
    save_min_price,
    save_selected_city,
    save_selected_district,
    save_selected_rooms,
    save_user_search_settings,
)
from tgbot.misc.states import SearchSetup
from tgbot.misc.data_getters import (
    get_can_with_animals,
    get_found_cities,
    get_found_districts,
    get_from_owners_only,
    get_number_of_rooms,
    get_search_results,
)


search_setup_dialog: Dialog = Dialog(
    Window(
        Const(text="🌇 Введи назву міста, в якому шукаємо квартиру:"),
        StaticMedia(path=BOT_LOGO, type=ContentType.PHOTO),
        MessageInput(func=save_city_name, content_types=[ContentType.ANY]),
        state=SearchSetup.input_city_name,
    ),
    Window(
        Case(
            texts={
                True: Const(text="👉 Обери потрібне місто, або введи іншу назву:"),
                False: Const(text="❌ Я не знайшов жодного міста, спробуй змінити назву:"),
            },
            selector="cities_found",
        ),
        StaticMedia(path=BOT_LOGO, type=ContentType.PHOTO),
        MessageInput(func=save_city_name, content_types=[ContentType.ANY]),
        Column(
            Select(
                text=Format(text="{item[0]}"),
                id="w_city",
                item_id_getter=itemgetter(1),
                items="cities",
                on_click=save_selected_city,
            )
        ),
        state=SearchSetup.select_city,
        getter=get_found_cities,
    ),
    Window(
        Const(text="🌇 Введи назву району міста:"),
        StaticMedia(path=BOT_LOGO, type=ContentType.PHOTO),
        MessageInput(func=save_district_name, content_types=[ContentType.ANY]),
        Column(
            SwitchTo(text=Const(text="◀️ Повернутися"), id="b_another_city", state=SearchSetup.select_city),
            SwitchTo(
                text=Const(text="▶️ Шукати по всьому місту"),
                id="b_all_city",
                state=SearchSetup.select_number_of_rooms,
                on_click=not_choosing_district,
            ),
        ),
        state=SearchSetup.input_district_name,
    ),
    Window(
        Case(
            texts={
                True: Const(text="👉 Обери потрібний район, або введи іншу назву:"),
                False: Const(text="❌ Я не знайшов жодного району, спробуй змінити назву:"),
            },
            selector="districts_found",
        ),
        StaticMedia(path=BOT_LOGO, type=ContentType.PHOTO),
        MessageInput(func=save_district_name, content_types=[ContentType.ANY]),
        Column(
            Select(
                text=Format(text="{item[0]}"),
                id="w_district",
                item_id_getter=itemgetter(1),
                items="districts",
                on_click=save_selected_district,
            ),
            SwitchTo(text=Const(text="◀️ Повернутися"), id="b_another_city", state=SearchSetup.select_city),
        ),
        state=SearchSetup.select_district,
        getter=get_found_districts,
    ),
    Window(
        Const(text="🏘 Вибери кількість кімнат:"),
        StaticMedia(path=BOT_LOGO, type=ContentType.PHOTO),
        MessageInput(func=any_other_messages, content_types=[ContentType.ANY]),
        Select(
            text=Format(text="{item[0]}"),
            id="w_room",
            item_id_getter=itemgetter(1),
            items="rooms",
            on_click=save_selected_rooms,
        ),
        SwitchTo(text=Const(text="◀️ Повернутися"), id="b_another_city", state=SearchSetup.select_city),
        state=SearchSetup.select_number_of_rooms,
        getter=get_number_of_rooms,
    ),
    Window(
        Const(text="💵 На яку мінімальну ціну (у гривнях) на місяць ти розраховуєш?\n\nВводь лише цифри:"),
        StaticMedia(path=BOT_LOGO, type=ContentType.PHOTO),
        MessageInput(func=save_min_price, content_types=[ContentType.ANY]),
        SwitchTo(text=Const(text="◀️ Повернутися"), id="b_number_of_rooms", state=SearchSetup.select_number_of_rooms),
        state=SearchSetup.set_min_price,
    ),
    Window(
        Const(text="💵 На яку максимальну ціну (у гривнях) на місяць ти розраховуєш?\n\nВводь лише цифри:"),
        StaticMedia(path=BOT_LOGO, type=ContentType.PHOTO),
        MessageInput(func=save_max_price, content_types=[ContentType.ANY]),
        SwitchTo(text=Const(text="◀️ Повернутися"), id="b_min_price", state=SearchSetup.set_min_price),
        state=SearchSetup.set_max_price,
    ),
    Window(
        Const(text="🐶 У тебе є домашні тварини?"),
        StaticMedia(path=BOT_LOGO, type=ContentType.PHOTO),
        MessageInput(func=any_other_messages, content_types=[ContentType.ANY]),
        Select(
            text=Format(text="{item[0]}"),
            id="w_animals",
            item_id_getter=itemgetter(1),
            items="animals",
            on_click=save_can_with_animals,
        ),
        SwitchTo(text=Const(text="◀️ Повернутися"), id="b_max_price", state=SearchSetup.set_max_price),
        state=SearchSetup.select_can_with_animals,
        getter=get_can_with_animals,
    ),
    Window(
        Const(text="📃 Показувати оголошення лише від власників квартир?"),
        StaticMedia(path=BOT_LOGO, type=ContentType.PHOTO),
        MessageInput(func=any_other_messages, content_types=[ContentType.ANY]),
        Select(
            text=Format(text="{item[0]}"),
            id="w_owners",
            item_id_getter=itemgetter(1),
            items="owners",
            on_click=save_from_owners_only,
        ),
        SwitchTo(text=Const(text="◀️ Повернутися"), id="b_can_with_animals", state=SearchSetup.select_can_with_animals),
        state=SearchSetup.select_from_owners_only,
        getter=get_from_owners_only,
    ),
    Window(
        Case(
            texts={
                True: Format(text="✔ Пошук завершено.\n\nЩо будемо робити далі?"),
                False: Const(text="❌ За вказаними параметрами нічого не знайдено!\n\nСпробуй змінити умови пошуку."),
            },
            selector="if_ads_found",
        ),
        StaticMedia(path=BOT_LOGO, type=ContentType.PHOTO),
        MessageInput(func=any_other_messages, content_types=[ContentType.ANY]),
        Column(
            Url(
                text=Const(text="↗ Переглянути на сайті"),
                url=Format(text="{show_ads_url}"),
                id="b_show_ads",
                when="if_ads_found",
            ),
            Button(
                text=Const(text="🆗 Підписатися на пошук"),
                id="b_subscribe",
                on_click=save_user_search_settings,
                when="if_ads_found",
            ),
            Button(text=Const(text="🔍 Новий пошук"), id="b_reset_search", on_click=reset_search),
        ),
        state=SearchSetup.show_search_result,
        getter=get_search_results,
    ),
    on_start=on_start,
    on_close=on_close,
)
