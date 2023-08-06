"""Налаштування конфігурації для бота"""

import logging

from os.path import join, normpath
from pathlib import Path
from typing import NamedTuple

from environs import Env


class DbConfig(NamedTuple):
    """Database configuration"""

    host: str
    port: str
    password: str
    user: str
    database: str


class TgBot(NamedTuple):
    """Дані бота"""

    token: str


class Config(NamedTuple):
    """Конфігурація бота"""

    tg_bot: TgBot
    db: DbConfig


# sys.tracebacklimit = 0

_BASE_DIR: Path = Path(__file__).resolve().parent.parent
_LOG_FILE: str = join(_BASE_DIR, "orenda-ua-bot.log")
BOT_LOGO: str = normpath(join(_BASE_DIR, "tgbot/assets/img/bot_logo.png"))


logger: logging.Logger = logging.getLogger(__name__)
logging.basicConfig(
    # filename=_LOG_FILE,
    level=logging.INFO,
    format="%(levelname)-8s %(filename)s:%(lineno)d [%(asctime)s] - %(name)s - %(message)s",
)


def load_config() -> Config:
    """Завантажує налаштування зі змінних оточення"""
    env: Env = Env()
    env.read_env()
    return Config(
        tg_bot=TgBot(
            token=env.str("BOT_TOKEN"),
        ),
        db=DbConfig(
            host=env.str("POSTGRES_DB_HOST"),
            port=env.str("POSTGRES_DB_PORT"),
            password=env.str("POSTGRES_DB_PASSWORD"),
            user=env.str("POSTGRES_DB_USER"),
            database=env.str("POSTGRES_DB_NAME"),
        ),
    )
