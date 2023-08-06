"""Описує стан для FSM (кінцевого автомата)"""

from aiogram.dispatcher.filters.state import State, StatesGroup


class SearchSetup(StatesGroup):
    """Описує кроки діалогового вікна налаштування пошуку"""

    input_city_name = State()
    select_city = State()
    input_district_name = State()
    select_district = State()
    select_number_of_rooms = State()
    set_min_price = State()
    set_max_price = State()
    select_can_with_animals = State()
    select_from_owners_only = State()
    show_search_result = State()
