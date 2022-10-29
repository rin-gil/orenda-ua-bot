from aiogram.dispatcher.filters.state import StatesGroup, State


class Search(StatesGroup):
    Start = State()
    SelectCity = State()
    SelectNumberOfRooms = State()
    SetMinPrice = State()
    SetMaxPrice = State()
    CanWithAnimals = State()
    OnlyFromOwner = State()
    End = State()
