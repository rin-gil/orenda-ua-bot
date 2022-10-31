<p align="center">
    <img src="https://repository-images.githubusercontent.com/559275297/4c8d91b7-c55c-4c70-8903-2f45ebcdab3f" alt="OrendaUA Bot" width="640">
</p>

<p align="center">
    <a href="https://www.python.org/downloads/release/python-3108/"><img src="https://img.shields.io/badge/python-v3.10-informational" alt="python version"></a>
    <a href="https://pypi.org/project/aiogram/2.22.1/"><img src="https://img.shields.io/badge/aiogram-v2.22.1-informational" alt="aiogram version"></a>
    <a href="https://pypi.org/project/aiohttp/3.8.1/"><img src="https://img.shields.io/badge/aiohttp-v3.8.1-informational" alt="aiohttp version"></a>
    <a href="https://pypi.org/project/aioschedule/0.5.2/"><img src="https://img.shields.io/badge/aioschedule-v0.5.2-informational" alt="aioschedule version"></a>
    <a href="https://pypi.org/project/aiosqlite/0.17.0/"><img src="https://img.shields.io/badge/aiosqlite-v0.17.0-informational" alt="aiosqlite version"></a>
    <a href="https://pypi.org/project/environs/9.5.0/"><img src="https://img.shields.io/badge/environs-v9.5.0-informational" alt="environs version"></a>
    <a href="https://github.com/rin-gil/OrendaUAbot/blob/master/LICENCE"><img src="https://img.shields.io/badge/licence-MIT-success" alt="MIT licence"></a>
</p>

<p align="right">
    <a href="https://github.com/rin-gil/OrendaUAbot/blob/master/README.ua.md">Читати українською</a>
</p>

## OrendaUA bot

Bot for sending ads from the site [DOM.RIA](https://dom.ria.com/uk/). The working version is available at [https://t.me/OrendaUAbot](https://t.me/OrendaUAbot)

### Features

* Setting up a filter for searching ads.
* Subscription to new ads, according to the specified filter.

### Installation

```
git clone https://github.com/rin-gil/OrendaUAbot.git
cd OrendaUAbot
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
mv .env.dist .env
```

### Setup and launch

* Register a new bot with [BotFather](https://t.me/BotFather) and copy the obtained token
* Insert the bot token into the .env file
* Running the bot through the bot.py file `python bot.py`

### Обмеження
* The bot only searches for apartment rental ads, search for apartments for sale and other categories of ads from the site [DOM.RIA](https://dom.ria.com/uk/) are not available.
* Viewing found ads from the bot is not available. Instead, you will receive a message with a photo and a brief description of the apartment for rent.
You can view the full ad and contact the author of the ad by clicking on the link.

### Developers

* [Ringil](https://github.com/rin-gil)

### License

OrendaUA bot is licensed under [MIT](https://github.com/rin-gil/OrendaUAbot/blob/master/LICENCE)
