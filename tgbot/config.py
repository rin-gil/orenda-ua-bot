"""Налаштування конфігурації для бота"""

import logging
import sys

from os.path import join, normpath
from pathlib import Path
from typing import NamedTuple

from environs import Env


sys.tracebacklimit = 0

BASE_DIR: Path = Path(__file__).resolve().parent.parent
BOT_LOGO: str = normpath(join(BASE_DIR, "tgbot/assets/img/bot_logo.png"))
DB_FILE: str = normpath(join(BASE_DIR, "tgbot/db.sqlite3"))
LOG_FILE: str = join(BASE_DIR, "log.log")


logger: logging.Logger = logging.getLogger(__name__)
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.WARNING,
    format="%(levelname)-8s %(filename)s:%(lineno)d [%(asctime)s] - %(name)s - %(message)s",
)


class TgBot(NamedTuple):
    """Дані бота"""

    token: str


class Config(NamedTuple):
    """Конфігурація бота"""

    tg_bot: TgBot


def load_config() -> Config:
    """Завантажує налаштування зі змінних оточення"""
    env = Env()
    env.read_env()
    return Config(tg_bot=TgBot(token=env.str("BOT_TOKEN")))
