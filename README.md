<p align="center">
    <img src="https://repository-images.githubusercontent.com/559275297/4c8d91b7-c55c-4c70-8903-2f45ebcdab3f" alt="OrendaUA Bot" width="640">
</p>

<p align="center">
    <a href="https://www.python.org/downloads/release/python-3108/">
        <img src="https://img.shields.io/badge/python-v3.10-informational" alt="python version">
    </a>
    <a href="https://pypi.org/project/aiogram/2.25.1/">
        <img src="https://img.shields.io/badge/aiogram-v2.25.1-informational" alt="aiogram version">
    </a>
    <a href="https://pypi.org/project/aiogram-dialog/1.9.0/">
        <img src="https://img.shields.io/badge/aiogram_dialog-v1.9.0-informational" alt="aiogram version">
    </a>
    <a href="https://pypi.org/project/aiohttp/3.8.5/">
        <img src="https://img.shields.io/badge/aiohttp-v3.8.5-informational" alt="aiohttp version">
    </a>
    <a href="https://pypi.org/project/asyncpg/0.28.0/">
        <img src="https://img.shields.io/badge/asyncpg-v0.28.0-informational" alt="asyncpg version">
    </a>
    <a href="https://pypi.org/project/APScheduler/3.10.1/">
        <img src="https://img.shields.io/badge/APScheduler-v3.10.1-informational" alt="APScheduler version">
    </a>
    <a href="https://pypi.org/project/environs/9.5.0/">
        <img src="https://img.shields.io/badge/environs-v9.5.0-informational" alt="environs version">
    </a>
    <a href="https://pypi.org/project/redis/4.6.0/">
        <img src="https://img.shields.io/badge/redis-v4.6.0-informational" alt="redis version">
    </a>
</p>
<p align="center">
    <a href="https://github.com/psf/black">
        <img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-black.svg">
    </a>
    <a href="https://github.com/rin-gil/orenda-ua-bot/actions/workflows/tests.yml">
        <img src="https://github.com/rin-gil/orenda-ua-bot/actions/workflows/tests.yml/badge.svg" alt="Tests">
    </a>
    <a href="https://github.com/rin-gil/orenda-ua-bot/actions/workflows/codeql.yml">
        <img src="https://github.com/rin-gil/orenda-ua-bot/actions/workflows/codeql.yml/badge.svg" alt="CodeQL tests">
    </a>
    <a href="https://github.com/rin-gil/orenda-ua-bot/blob/master/LICENCE.md">
        <img src="https://img.shields.io/badge/licence-MIT-success" alt="MIT licence">
    </a>
</p>

## OrendaUA bot

Бот для розсилки оголошень з сайту [DOM.RIA](https://dom.ria.com/uk/).
Робоча версія доступна за посиланням [@OrendaUAbot](https://t.me/OrendaUAbot)

### Можливості

* Налаштування фільтра для пошуку оголошень.
* Підписка на нові оголошення, згідно з заданим фільтром.

### Інсталяція бота

Якщо вам потрібна проста версія бота, без використання бази даних Postgres і без роботи в режимі веб-хука, перейдіть до [цієї гілки](https://github.com/rin-gil/orenda-ua-bot/tree/simple-with-sqlite-no-webhook).

Встановіть бота за допомогою команди в терміналі:

```
wget https://raw.githubusercontent.com/rin-gil/orenda-ua-bot/master/infrastructure/deploy.sh && chmod +x deploy.sh && ./deploy.sh
```

### Встановлення та налаштування Postgres

Встановіть базу даних Postgres згідно з інструкцією з офіційного сайту: https://www.postgresql.org/download/

Робота бота протестована на Postgres версії 15

Створіть базу даних, користувача та налаштування, виконавши команди в терміналі:

```
sudo -u postgres psql
CREATE DATABASE db_name;
CREATE USER db_user WITH PASSWORD 'db_password';
\connect db_name;
CREATE SCHEMA db_name AUTHORIZATION db_user;
ALTER ROLE db_user SET client_encoding TO 'utf8';
ALTER ROLE db_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE db_user SET timezone TO 'UTC';
\q
```

Замініть _db_name_, _db_user_ і _db_password_ у цих командах своїми даними.

### Налаштування та запуск

* Зареєструйте нового бота у [@BotFather](https://t.me/BotFather) і скопіюйте отриманий токен
* Вставте токен бота та облікові дані до бази даних у файл .env
* Запуск бота через файл bot.py `python bot.py`

### Додаткова конфігурація

Приклади конфігурацій для запуску бота в режимі webhook або як systemd-сервіс можна знайти в теці [infrastructure](https://github.com/rin-gil/orenda-ua-bot/tree/master/infrastructure)

### Розробники

* [Ringil](https://github.com/rin-gil)

### Ліцензії

Проєкт OrendaUA bot поширюється за ліцензією [MIT](https://github.com/rin-gil/orenda-ua-bot/blob/master/LICENCE.md)
