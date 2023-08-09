"""Налаштування конфігурації для бота"""

import logging
import sys

from os.path import join, normpath
from pathlib import Path
from typing import NamedTuple

from environs import Env


class DbConfig(NamedTuple):
    """Database configuration"""

    host: str
    port: str
    database: str
    user: str
    password: str


class RedisConfig(NamedTuple):
    """Redis database configuration"""

    host: str
    port: int
    database_index: int
    password: str


class WebhookCredentials(NamedTuple):
    """Represents credentials to use webhook"""

    wh_host: str
    wh_path: str
    wh_token: str
    app_host: str
    app_port: int


class TgBot(NamedTuple):
    """Дані бота"""

    token: str


class Config(NamedTuple):
    """Конфігурація бота"""

    tg_bot: TgBot
    db: DbConfig
    redis: RedisConfig | None
    webhook: WebhookCredentials | None


# Change USE_WEBHOOK to True to use a webhook instead of long polling
USE_WEBHOOK: bool = False

# Change USE_REDIS to True to use redis storage for FSM instead of memory
USE_REDIS: bool = False

_BASE_DIR: Path = Path(__file__).resolve().parent.parent
_LOG_FILE: str = join(_BASE_DIR, "orenda-ua-bot.log")
BOT_LOGO: str = normpath(join(_BASE_DIR, "tgbot/assets/img/bot_logo.png"))

sys.tracebacklimit = 0

logger: logging.Logger = logging.getLogger(__name__)
logging.basicConfig(
    filename=_LOG_FILE,
    level=logging.ERROR,
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
            host=env.str("PG_HOST"),
            port=env.str("PG_PORT"),
            database=env.str("PG_DB_NAME"),
            user=env.str("PG_DB_USER"),
            password=env.str("PG_DB_PASS"),
        ),
        redis=RedisConfig(
            host=env.str("REDIS_HOST"),
            port=env.int("REDIS_PORT"),
            database_index=env.int("REDIS_DB_INDEX"),
            password=env.str("REDIS_DB_PASS"),
        )
        if USE_REDIS
        else None,
        webhook=WebhookCredentials(
            wh_host=env.str("WEBHOOK_HOST"),
            wh_path=env.str("WEBHOOK_PATH"),
            wh_token=env.str("WEBHOOK_TOKEN"),
            app_host=env.str("WEBAPP_HOST"),
            app_port=env.int("WEBAPP_PORT"),
        )
        if USE_WEBHOOK
        else None,
    )
