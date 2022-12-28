"""Клас для роботи з базою даних"""

from sqlite3 import OperationalError
from sys import exit as sys_exit
from typing import AsyncIterator

from aiosqlite import connect

from tgbot.config import DB_FILE, logger
from tgbot.models.dataclasses import User


class Database:
    """Клас для роботи з базою даних"""

    def __init__(self, path: str) -> None:
        """Визначає шлях до файлу бази даних"""
        self._db_path = path

    async def init(self) -> None:
        """Створює файл бази даних і таблиці в ній"""
        try:
            async with connect(database=self._db_path) as db:
                await db.execute(
                    """
                    CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY,
                        search_url VARCHAR(300) NOT NULL
                    );
                    """
                )
                await db.execute(
                    """
                    CREATE TABLE IF NOT EXISTS ads (
                        user_id INTEGER NOT NULL,
                        ad_id INTEGER NOT NULL
                    );
                    """
                )
        except OperationalError as ex:
            logger.critical("Database connection error: %s", ex)
            sys_exit()

    async def add_user(self, user_id: int, search_url: str, ads_ids: list) -> None:
        """Додає нового користувача в базу даних"""
        async with connect(database=self._db_path) as db:
            await db.execute("""INSERT INTO users (id, search_url) VALUES (?, ?);""", (user_id, search_url))
            values: list[tuple] = []
            for ad_id in ads_ids:
                values.append((user_id, ad_id))
            await db.executemany("""INSERT INTO ads (user_id, ad_id) VALUES (?, ?);""", values)
            await db.commit()

    async def delete_user(self, user_id: int) -> None:
        """Видаляє з бази даних всі записи про користувача і знайдені для нього оголошення"""
        async with connect(database=self._db_path) as db:
            await db.execute("""DELETE FROM users WHERE id=?;""", (user_id,))
            await db.execute("""DELETE FROM ads WHERE user_id=?;""", (user_id,))
            await db.commit()

    async def check_if_user_exists(self, user_id: int) -> bool:
        """Перевіряє, чи є користувач із зазначеним id у базі даних"""
        async with connect(database=self._db_path) as db:
            async with db.execute("""SELECT id FROM users WHERE id=?;""", (user_id,)) as cursor:
                async for row in cursor:
                    return bool(row[0])
        return False

    async def get_users(self) -> AsyncIterator[User]:
        """Повертає інформацію про користувачів з бази даних"""
        async with connect(database=self._db_path) as db:
            async with db.execute("""SELECT id, search_url FROM users;""") as cursor_users:
                async for row_users in cursor_users:
                    async with db.execute("""SELECT ad_id FROM ads WHERE user_id=?;""", (row_users[0],)) as cursor_ads:
                        ads_list: list[int] = []
                        async for row_ads in cursor_ads:
                            ads_list.append(row_ads[0])
                        yield User(id=row_users[0], search_url=row_users[1], ads_ids=set(ads_list))

    async def update_user_data(self, user_id: int, ads_to_save: set[int], ads_to_delete: set[int]) -> None:
        """Оновлює дані користувача в базі даних"""
        async with connect(database=self._db_path) as db:
            values: list = []
            for ad_id in ads_to_delete:
                values.append((user_id, ad_id))
            await db.executemany("""DELETE FROM ads WHERE user_id=? AND ad_id=?;""", values)
            values.clear()
            for ad_id in ads_to_save:
                values.append((user_id, ad_id))
            await db.executemany("""INSERT INTO ads(user_id, ad_id) VALUES (?, ?);""", values)
            await db.commit()


database: Database = Database(path=DB_FILE)
