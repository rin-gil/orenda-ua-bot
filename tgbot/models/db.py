from aiosqlite import connect

from tgbot import DB_NAME
from tgbot.services import get_ad_id


async def db_init() -> None:
    """
    Creates a database file and the necessary tables in it.

    :return: None
    """
    async with connect(DB_NAME) as db:
        await db.execute(
            """CREATE TABLE IF NOT EXISTS users (
            id_user INTEGER PRIMARY KEY ON CONFLICT IGNORE NOT NULL, 
            search_string TEXT
            );"""
        )
        await db.execute(
            """CREATE TABLE IF NOT EXISTS searches (
            id_user INTEGER REFERENCES users (id_user) ON UPDATE CASCADE ON DELETE CASCADE, 
            id_ad INTEGER
            );"""
        )


async def del_user(id_user: int) -> None:
    """
    Deletes all records about the user and the ads found for him from the database.

    :param id_user: user id
    :return: None
    """
    async with connect(DB_NAME) as db:
        value: list = [id_user]
        await db.execute("""DELETE FROM users WHERE id_user=?;""", value)
        await db.execute("""DELETE FROM searches WHERE id_user=?;""", value)
        await db.commit()


async def add_user(id_user: int, search_string: str) -> None:
    """
    Adds the user, his ad search filter and the ads found by this filter to the database.

    :param id_user: User ID
    :param search_string: Ad search string
    :return: None
    """
    async with connect(DB_NAME) as db:
        values: list = [id_user, search_string]
        await db.execute("""INSERT INTO users (id_user, search_string) VALUES (?, ?);""", values)
        await db.commit()
        values.clear()
        ads: list = await get_ad_id(url=search_string)
        for id_ad in ads:
            values.append([id_user, id_ad])
        await db.executemany("""INSERT INTO searches(id_user, id_ad) VALUES (?, ?);""", values)
        await db.commit()


async def select_users() -> list:
    """
    Returns a nested list containing the user id and its search query for all users in the database.

    :return: A list of users subscribed to the list of ads.
    """
    users: list = []
    async with connect(DB_NAME) as db:
        async with db.execute("""SELECT * FROM users;""") as cursor:
            async for row in cursor:
                users.append([row[0], row[1]])
    return users


async def get_old_ads(id_user: int) -> set:
    """
    Returns a set that contains a list of ad id's that were previously shown to the user.

    :param id_user: User id
    :return: Set that contains a list of ad id's that were previously shown to the user.
    """
    old_ads: set = set()
    async with connect(DB_NAME) as db:
        value: list = [id_user]
        async with db.execute("""SELECT id_ad FROM searches WHERE id_user=?;""", value) as cursor:
            async for row in cursor:
                old_ads.add(row[0])
    return old_ads
