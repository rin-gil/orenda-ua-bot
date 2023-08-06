"""Клас для роботи з базою даних"""

from typing import AsyncIterator

from asyncpg import create_pool, Pool

from tgbot.config import DbConfig
from tgbot.services.dataclasses import User


class Database:
    """Клас для роботи з базою даних"""

    def __init__(self, db_config: DbConfig) -> None:
        """Визначає параметри підключення до бази даних"""
        self._db_dsn: str = (
            f"postgresql://{db_config.user}:{db_config.password}@{db_config.host}:{db_config.port}/{db_config.database}"
        )
        self._pool: Pool | None = None

    async def _get_pool(self) -> Pool:
        """Створює та повертає пул підключень до бази даних"""
        if not self._pool:
            self._pool = await create_pool(dsn=self._db_dsn)
        return self._pool

    async def init(self) -> None:
        """Створює файл бази даних і таблиці в ній"""
        pool: Pool = await self._get_pool()
        await pool.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                user_id BIGINT PRIMARY KEY,
                search_url VARCHAR(300) NOT NULL
            );
            """
        )
        await pool.execute(
            """
            CREATE TABLE IF NOT EXISTS ads (
                user_id BIGINT REFERENCES users(user_id) ON DELETE CASCADE,
                ad_id INTEGER NOT NULL
            );
            """
        )

    async def add_user(self, user_id: int, search_url: str, ads_ids: list) -> None:
        """Додає нового користувача в базу даних"""
        pool: Pool = await self._get_pool()
        values: list[tuple[str, int]] = [(str(user_id), ad_id) for ad_id in ads_ids]
        await pool.execute("""INSERT INTO users (user_id, search_url) VALUES ($1, $2);""", user_id, search_url)
        await pool.executemany("""INSERT INTO ads (user_id, ad_id) VALUES (CAST($1 AS TEXT)::BIGINT, $2);""", values)

    async def delete_user(self, user_id: int) -> None:
        """Видаляє з бази даних всі записи про користувача і знайдені для нього оголошення"""
        pool: Pool = await self._get_pool()
        await pool.execute("""DELETE FROM users WHERE user_id=$1;""", user_id)

    async def check_if_user_exists(self, user_id: int) -> bool:
        """Перевіряє, чи є користувач із зазначеним id у базі даних"""
        pool: Pool = await self._get_pool()
        for row in await pool.fetch("""SELECT user_id FROM users WHERE user_id=$1;""", user_id):
            return bool(row[0])
        return False

    async def get_users(self) -> AsyncIterator[User]:
        """Повертає інформацію про користувачів з бази даних"""
        pool: Pool = await self._get_pool()
        for user in await pool.fetch("""SELECT user_id, search_url FROM users;"""):
            ads_list: list[int] = []
            for ad in await pool.fetch("""SELECT ad_id FROM ads WHERE user_id=$1;""", user[0]):
                ads_list.append(ad[0])
            yield User(id=user[0], search_url=user[1], ads_ids=set(ads_list))

    async def update_user_data(self, user_id: int, ads_to_save: set[int], ads_to_delete: set[int]) -> None:
        """Оновлює дані користувача в базі даних"""
        pool: Pool = await self._get_pool()
        values: list[tuple[int | str, int]] = []
        for ad_id in ads_to_delete:
            values.append((user_id, ad_id))
        await pool.executemany("""DELETE FROM ads WHERE user_id=$1 AND ad_id=$2;""", values)
        values.clear()
        for ad_id in ads_to_save:
            values.append((str(user_id), ad_id))
        await pool.executemany("""INSERT INTO ads (user_id, ad_id) VALUES (CAST($1 AS TEXT)::BIGINT, $2);""", values)

    async def close(self) -> None:
        """Закриває пул підключень до бази даних"""
        if self._pool:
            await self._pool.close()
            self._pool = None
