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
    <a href="https://pypi.org/project/aiosqlite/0.18.0/">
        <img src="https://img.shields.io/badge/aiosqlite-v0.18.0-informational" alt="aiosqlite version">
    </a>
    <a href="https://pypi.org/project/APScheduler/3.10.1/">
        <img src="https://img.shields.io/badge/APScheduler-v3.10.1-informational" alt="APScheduler version">
    </a>
    <a href="https://pypi.org/project/environs/9.5.0/">
        <img src="https://img.shields.io/badge/environs-v9.5.0-informational" alt="environs version">
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

### Установлення

```
git clone https://github.com/rin-gil/orenda-ua-bot.git
cd orenda-ua-bot
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
mv .env.example .env
```

### Налаштування та запуск

* Зареєструйте нового бота у [@BotFather](https://t.me/BotFather) і скопіюйте отриманий токен
* Вставте токен бота у файл .env
* Запуск бота через файл bot.py `python bot.py`

### Розробники

* [Ringil](https://github.com/rin-gil)

### Ліцензії

Проєкт OrendaUA bot поширюється за ліцензією [MIT](https://github.com/rin-gil/orenda-ua-bot/blob/master/LICENCE.md)
