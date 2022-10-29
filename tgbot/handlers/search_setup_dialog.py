from datetime import date, timedelta

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery

from tgbot import BANNED_CONTENT
from tgbot.keyboards import kb_search_start, generate_cities_kb, kb_select_number_of_rooms, kb_can_with_animals, \
    kb_only_from_owner, generate_end_search_kb
from tgbot.misc import Search
from tgbot.models import del_user, add_user
from tgbot.services import find_city, get_quantity_ads


async def commands(message: Message, state: FSMContext) -> None:
    """
    Handles commands from the user

    :param message: Message from the user
    :param state: State from FSM
    :return: None
    """
    if message.text == '/start':
        await Search.Start.set()
        async with state.proxy() as data:
            data['id_user']: int = message.from_user.id
            await message.bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
            await message.answer(text='🏘 Давай налаштуємо пошук:', reply_markup=kb_search_start)
    elif message.text == '/help':
        await message.bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        await message.answer(text='Вітаю! ✋\n\n'
                                  'Я допоможу тобі знайти оголошення про оренду квартир, '
                                  'а також можу надсилати тобі нові оголошення, які тебе зацікавлять.\n\n'
                                  'Для початку роботи, натисни /start\n\n'
                                  'Щоб зупинити розсилку оголошень та видалити всі свої дані, натисни /stop')
    else:
        await state.reset_state()
        await del_user(id_user=message.chat.id)
        async with state.proxy() as data:
            data.clear()
        await message.bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        await message.answer(text='❌ Усі твої дані видалені.\n\nЩоб налаштувати новий пошук, натисни /start')


async def search_start(call: CallbackQuery, state: FSMContext) -> None:
    """
    Ask the user the name of the city

    :param call: CallbackQuery
    :param state: State from FSM
    :return: None
    """
    await call.answer(cache_time=1)
    await Search.SelectCity.set()
    async with state.proxy() as data:
        data['message_id']: int = call.message.message_id
        await call.bot.edit_message_text(text='🌇 Введи назву міста, в якому шукаємо квартиру, можна перші три літери:',
                                         chat_id=call.message.chat.id, message_id=call.message.message_id)


async def select_city(message: Message, state: FSMContext) -> None:
    """
    Check if there are cities on the user's request and display a list of cities

    :param message: Message from the user
    :param state: State from FSM
    :return: None
    """
    async with state.proxy() as data:
        cities: set = await find_city(city=message.text)
        await message.bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        if len(cities) != 0:
            kb_cities = await generate_cities_kb(cities=cities)
            await message.bot.edit_message_text(text=f'🔍 Я знайшов <b>{len(cities)}</b> міст, '
                                                     f'вибери одне, або введи іншу назву:',
                                                chat_id=data['id_user'], message_id=data['message_id'],
                                                reply_markup=kb_cities)
        else:
            await message.bot.edit_message_text(text='❌ Я не знайшов жодного міста, спробуй змінити назву:',
                                                chat_id=data['id_user'], message_id=data['message_id'])


async def select_number_of_rooms(call: CallbackQuery, state: FSMContext) -> None:
    """
    Save the selected city and show the dialogue to select the number of rooms.

    :param call: CallbackQuery
    :param state: State from FSM
    :return: None
    """
    await call.answer(cache_time=1)
    await Search.SelectNumberOfRooms.set()
    city: list = call.data.split('_')
    async with state.proxy() as data:
        data['city_id']: str = city[1]
        data['state_id']: str = city[2]
        await call.bot.edit_message_text(text='🏘 Вибери кількість кімнат:',
                                         chat_id=call.message.chat.id, message_id=call.message.message_id,
                                         reply_markup=kb_select_number_of_rooms)


async def set_min_price(call: CallbackQuery, state: FSMContext) -> None:
    """
    Save the selected number of rooms, display a message about entering the minimum price.

    :param call: CallbackQuery
    :param state: State from FSM
    :return: None
    """
    await call.answer(cache_time=1)
    await Search.SetMinPrice.set()
    async with state.proxy() as data:
        data['rooms']: str = call.data
        await call.bot.edit_message_text(text='💵 На яку мінімальну ціну (у гривнях) на місяць ти розраховуєш?',
                                         chat_id=call.message.chat.id, message_id=call.message.message_id)


async def min_price_is_invalid(message: Message, state: FSMContext) -> None:
    """
    Check the entered price, only numbers should be entered.

    :param message: Message from the user
    :param state: State from FSM
    :return: None
    """
    async with state.proxy() as data:
        await message.bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        try:
            await message.bot.edit_message_text(text='❌ Вводь лише цифри, будь ласка!\n\n'
                                                     '💵 На яку <b>мінімальну</b> ціну (у гривнях) '
                                                     'на місяць ти розраховуєш?',
                                                chat_id=data['id_user'], message_id=data['message_id'])
        finally:
            pass


async def set_max_price(message: Message, state: FSMContext) -> None:
    """
    Save the entered minimum price, display a message about entering the maximum price.

    :param message: Message from the user
    :param state: State from FSM
    :return: None
    """
    await Search.SetMaxPrice.set()
    async with state.proxy() as data:
        data['min_price']: int = int(message.text)
        await message.bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        await message.bot.edit_message_text(text='💵 На яку <b>максимальну</b> ціну (у гривнях) '
                                                 'на місяць ти розраховуєш?',
                                            chat_id=data['id_user'], message_id=data['message_id'])


async def max_price_is_invalid(message: Message, state: FSMContext) -> None:
    """
    Check the entered price, only numbers should be entered.

    :param message: Message from the user
    :param state: State from FSM
    :return: None
    """
    async with state.proxy() as data:
        await message.bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        try:
            await message.bot.edit_message_text(text='❌ Вводь лише цифри, будь ласка!\n\n'
                                                     '💵 На яку <b>максимальну</b> ціну (у гривнях) '
                                                     'на місяць ти розраховуєш?',
                                                chat_id=data['id_user'], message_id=data['message_id'])
        finally:
            pass


async def select_can_with_animals(message: Message, state: FSMContext) -> None:
    """
    Save the entered maximum price, display a message about whether you have pets.

    :param message: Message from the user
    :param state: State from FSM
    :return: None
    """
    await Search.CanWithAnimals.set()
    async with state.proxy() as data:
        data['max_price']: int = int(message.text)

        # Check if the user entered a higher price first, then a lower one,
        # then swap them so that the search is displayed correctly.
        min_price: int = min(data['min_price'], data['max_price'])
        max_price: int = max(data['min_price'], data['max_price'])
        data['min_price']: int = min_price
        data['max_price']: int = max_price

        await message.bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        await message.bot.edit_message_text(text='🐶 У тебе є домашні тварини?',
                                            chat_id=data['id_user'], message_id=data['message_id'],
                                            reply_markup=kb_can_with_animals)


async def select_ads_only_from_owner(call: CallbackQuery, state: FSMContext) -> None:
    """
    Save the user's answer about having pets, and display a dialog about whether to show ads only from apartment owners.

    :param call: CallbackQuery
    :param state: State from FSM
    :return: None
    """
    await call.answer(cache_time=1)
    await Search.OnlyFromOwner.set()
    animals: str = call.data
    async with state.proxy() as data:
        if animals == 'animal_yes':
            data['animals']: str = '%2C1670_1670'
        else:
            data['animals']: str = ''
        await call.bot.edit_message_text(text='📃 Показувати оголошення лише від власників квартир?',
                                         chat_id=call.message.chat.id, message_id=call.message.message_id,
                                         reply_markup=kb_only_from_owner)


async def generating_search_string(call: CallbackQuery, state: FSMContext) -> None:
    """
    Generate a search string.

    :param call: CallbackQuery
    :param state: State from FSM
    :return: None
    """
    await call.answer(cache_time=1)
    await Search.End.set()
    owner: str = call.data
    async with state.proxy() as data:
        if owner == 'owner_yes':
            data['owner']: str = '%2C1437_1436%3A'
        else:
            data['owner']: str = ''
        search_string: str = f'https://dom.ria.com/node/searchEngine/v2/?category=1&realty_type=2&operation=3' \
                             f'&state_id=0&city_id={data["city_id"]}&in_radius=0&with_newbuilds=0&price_cur=1' \
                             f'&wo_dupl=1&inspected=0&sort=inspected_sort&period=0&date_from=' \
                             f'{str(date.today() - timedelta(days=60))}&date_to={str(date.today())}&notFirstFloor=0' \
                             f'&notLastFloor=0&with_map=0&photos_count_from=0&firstInteraction=false' \
                             f'&state_id{data["state_id"]}=&type=list&client=searchV2&limit=50&page=0' \
                             f'&operation_type=3&ch={data["rooms"]}%2C235_f_{data["min_price"]}' \
                             f'%2C235_t_{data["max_price"]}%2C246_244{data["owner"]}{data["animals"]}'
        data['search_string']: str = search_string
        quantity_ads = await get_quantity_ads(url=search_string)
        kb_end_search = generate_end_search_kb(ads=quantity_ads,
                                               url=search_string.replace('node/searchEngine/v2/', 'uk/search'))
        if quantity_ads != 0:
            await call.bot.edit_message_text(text=f'✔ За вказаними параметрами я знайшов '
                                                  f'<b>{quantity_ads}</b> оголошень.\n\n'
                                                  f'Що будемо робити далі?',
                                             chat_id=call.message.chat.id, message_id=call.message.message_id,
                                             reply_markup=await kb_end_search)
        else:
            await call.bot.edit_message_text(text=f'❌ За вказаними параметрами нічого не знайдено.\n\n'
                                                  f'Спробуй змінити пошуковий запит.',
                                             chat_id=call.message.chat.id, message_id=call.message.message_id,
                                             reply_markup=await kb_end_search)


async def restart_search(call: CallbackQuery, state: FSMContext) -> None:
    """
    If the user's query did not find anything, restart the creation of the search query.

    :param call: CallbackQuery
    :param state: State from FSM
    :return: None
    """
    await call.answer(cache_time=1)
    async with state.proxy() as data:
        data.clear()
        data['id_user']: int = call.from_user.id
    await Search.Start.set()
    await call.bot.edit_message_text(text='🏘 Давай налаштуємо пошук:',
                                     chat_id=call.message.chat.id, message_id=call.message.message_id,
                                     reply_markup=kb_search_start)


async def search_subscription(call: CallbackQuery, state: FSMContext) -> None:
    """
    Save the search query to the database

    :param call: CallbackQuery
    :param state: State from FSM
    :return: None
    """
    await call.answer(cache_time=1)
    async with state.proxy() as data:
        await del_user(id_user=data['id_user'])
        await add_user(id_user=data['id_user'], search_string=data['search_string'])
        data.clear()
        await state.reset_state()
        await call.bot.edit_message_text(text='✔ Підписку оформлено!\n\nЯ надсилатиму тобі нові оголошення в міру їх '
                                              'появи. Щоб скасувати підписку, введи команду /stop',
                                         chat_id=call.message.chat.id, message_id=call.message.message_id)


async def delete_search(call: CallbackQuery, state: FSMContext) -> None:
    """
    Deleting a user and his data from the database.

    :param call: CallbackQuery
    :param state: State from FSM
    :return: None
    """
    await call.answer(cache_time=1)
    await del_user(id_user=call.message.chat.id)
    await state.reset_state()
    async with state.proxy() as data:
        data.clear()
    await call.bot.edit_message_text(text='❌ Усі твої дані видалені.\n\nЩоб налаштувати новий пошук, натисни /start',
                                     chat_id=call.message.chat.id, message_id=call.message.message_id)


async def unknown_message(message: Message) -> None:
    """
    Delete all the user's messages that are not responses to bot questions.

    :param message: Message from the user
    :return: None
    """
    await message.bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)


async def unknown_content(message: Message) -> None:
    """
    Deletes a message if the user has sent anything other than text.

    :param message: Message from the user
    :return: None
    """
    await message.bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)


def register_commands(dp: Dispatcher) -> None:
    """
    Registers the handling of commands from the user in the Dispatcher.

    :param dp: Dispatcher
    :return: None
    """
    dp.register_message_handler(commands, commands=['start', 'help', 'stop'], state='*')


def register_callbacks(dp: Dispatcher) -> None:
    """
    Registers the processing of inline keyboard key presses in the dispatcher

    :param dp: Dispatcher
    :return: None
    """
    dp.register_callback_query_handler(search_start, text='search_start', state=Search.Start)
    dp.register_callback_query_handler(select_number_of_rooms, text_contains='city_', state=Search.SelectCity)
    dp.register_callback_query_handler(set_min_price, text_contains='209_', state=Search.SelectNumberOfRooms)
    dp.register_callback_query_handler(select_ads_only_from_owner, text_contains='animal_', state=Search.CanWithAnimals)
    dp.register_callback_query_handler(generating_search_string, text_contains='owner_', state=Search.OnlyFromOwner)
    dp.register_callback_query_handler(restart_search, text='start_new_search', state=Search.End)
    dp.register_callback_query_handler(search_subscription, text='subscribe', state=Search.End)
    dp.register_callback_query_handler(delete_search, text='stop', state=Search.End)


def register_messages(dp: Dispatcher) -> None:
    """
    Registers the handling of messages from the user in the Dispatcher.

    :param dp: Dispatcher
    :return: None
    """
    dp.register_message_handler(select_city, state=Search.SelectCity)
    dp.register_message_handler(min_price_is_invalid, lambda message: not message.text.isdigit(),
                                state=Search.SetMinPrice)
    dp.register_message_handler(set_max_price, lambda message: message.text.isdigit(),
                                state=Search.SetMinPrice)
    dp.register_message_handler(max_price_is_invalid, lambda message: not message.text.isdigit(),
                                state=Search.SetMaxPrice)
    dp.register_message_handler(select_can_with_animals, state=Search.SetMaxPrice)
    dp.register_message_handler(unknown_message, state=None)
    dp.register_message_handler(unknown_message, state='*')
    dp.register_message_handler(unknown_content, content_types=BANNED_CONTENT, state=None)
    dp.register_message_handler(unknown_content, content_types=BANNED_CONTENT, state='*')
