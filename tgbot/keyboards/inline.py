from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Button under the initial dialog
kb_search_start = InlineKeyboardMarkup(row_width=3, inline_keyboard=[
    [InlineKeyboardButton(text='🔍 Розпочати', callback_data='search_start')]
])


async def generate_cities_kb(cities: set):
    """
    Generates dynamic buttons, depending on the list of found cities

    :param cities: List of cities
    :return: Keyboard with generated buttons
    """
    kb_cities = InlineKeyboardMarkup(row_width=1)
    for city in cities:
        kb_cities.insert(InlineKeyboardButton(text=city[2], callback_data=f'city_{city[0]}_{city[1]}'))
    return kb_cities


# Buttons for selecting the number of rooms
kb_select_number_of_rooms = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='1', callback_data='209_f_1%2C209_t_1'),
        InlineKeyboardButton(text='1-2', callback_data='209_f_1%2C209_t_2'),
        InlineKeyboardButton(text='2', callback_data='209_f_2%2C209_t_2')
    ],
    [
        InlineKeyboardButton(text='2-3', callback_data='209_f_2%2C209_t_3'),
        InlineKeyboardButton(text='3', callback_data='209_f_3%2C209_t_3'),
        InlineKeyboardButton(text='4+', callback_data='209_f_4')
    ]
])

# Can with animals selection dialog keys
kb_can_with_animals = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='🟢 Так', callback_data='animal_yes'),
        InlineKeyboardButton(text='🔴 Ні', callback_data='animal_no')
    ]
])

# Ads only from owner selection dialog keys
kb_only_from_owner = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='🟢 Так', callback_data='owner_yes'),
        InlineKeyboardButton(text='🔴 Ні', callback_data='owner_no')
    ]
])


async def generate_end_search_kb(ads: int, url: str):
    """
    Dialog buttons to end the search

    :param ads: Quantity of found ads
    :param url: Link to the page with found ads, according to the user's request
    :return: Keyboard with generated buttons
    """
    if ads != 0:
        kb_end_search = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='↗ Переглянути на сайті', url=url)],
            [InlineKeyboardButton(text='🆗 Підписатися на пошук', callback_data='subscribe')],
            [InlineKeyboardButton(text='↩ Скасувати та видалити', callback_data='stop')]
        ])
    else:
        kb_end_search = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='🔍 Новий пошук', callback_data='start_new_search')]
        ])
    return kb_end_search


async def link_to_ad(url: str):
    """
    Outputs a button with a link to the site under the ad.

    :param url: Link to ad
    :return: Generated keypad with button
    """
    return InlineKeyboardMarkup(row_width=3,
                                inline_keyboard=[[InlineKeyboardButton(text='↗ Переглянути на сайті', url=url)]])
