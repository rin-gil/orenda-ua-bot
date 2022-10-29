import asyncio
from datetime import date, timedelta

import aioschedule

from tgbot.keyboards import link_to_ad
from tgbot.models import select_users, get_old_ads, del_user, add_user
from tgbot.services import get_ad_id, get_ad


async def check_for_new_ads() -> None:
    """
    Checks for new ads and shows them to users.

    :return: None
    """
    # Get an attached list of all users from the database.
    # Under user[0] we have the user id, under user[1] we have the search string.
    users: list = await select_users()
    for user in users:
        # Get a set of old ads that have already been shown to a certain user before.
        old_ads: set = await get_old_ads(id_user=user[0])
        # Get the old search string.
        old_search_string: str = user[1]
        # Form a new search string (change the date).
        string: tuple = old_search_string.partition('date_from=')
        new_search_string: str = f'{string[0]}date_from={str(date.today() - timedelta(days=60))}' \
                                 f'&date_to={str(date.today())}{string[2][29:]}'
        # Get a new list of ads.
        new_ads: set = set()
        new_ads_ids: list = await get_ad_id(url=new_search_string)
        for ads in new_ads_ids:
            new_ads.add(ads)
        # Form a list of ads to be shown to the user (the new list of ads minus what has already been shown before).
        ads_to_show: set = new_ads.difference(old_ads)
        # Save a new search string to the database for the user.
        await del_user(id_user=user[0])
        await add_user(id_user=user[0], search_string=new_search_string)
        # Send found new ads to the user.
        for ad in ads_to_show:
            ad_text: str = await get_ad(id_ad=ad)
            if len(ad_text) != 0:
                url: str = ad_text.partition('">')[0].replace('<b><a href="', '')
                try:
                    from bot import dp
                    await dp.bot.send_message(chat_id=user[0], text=ad_text, reply_markup=await link_to_ad(url=url))
                    await asyncio.sleep(1)
                except Exception as ex:
                    # If the message could not be sent (the user stopped the bot),
                    # then delete the user from the database.
                    await del_user(user[0])
                    print(ex)


async def schedule() -> None:
    """
    # Starts the function to check for new announcements on a schedule.

    :return: None
    """
    aioschedule.every(1).hour.do(check_for_new_ads)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)
