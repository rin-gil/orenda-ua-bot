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
    <a href="https://github.com/rin-gil/OrendaUAbot/blob/master/README.md">Read English</a>
</p>

## OrendaUA bot

Бот для розсилки оголошень з сайту [DOM.RIA](https://dom.ria.com/uk/). Робоча версія доступна за посиланням [https://t.me/OrendaUAbot](https://t.me/OrendaUAbot)

### Можливості

* Налаштування фільтра для пошуку оголошень.
* Підписка на нові оголошення, згідно з заданим фільтром.

### Установка

```
git clone https://github.com/rin-gil/OrendaUAbot.git
cd OrendaUAbot
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
mv .env.dist .env
```

### Налаштування та запуск

* Зареєструйте нового бота у [BotFather](https://t.me/BotFather) і скопіюйте отриманий токен
* Вставте токен бота у файл .env
* Запуск бота через файл bot.py `python bot.py`

### Обмеження
* Бот шукає тільки оголошення про оренду квартир, пошук квартир на продаж та інші категорії оголошень з сайту [DOM.RIA](https://dom.ria.com/uk/) не доступні.
* Перегляд знайдених об'яв з бота недоступний. Замість цього ви отримуватимете повідомлення з фотографією і коротким описом квартири, що здається.
Переглянути повне оголошення та зв'язатися з автором оголошення ви можете, перейшовши на сайт за посиланням.

### Розробники

* [Ringil](https://github.com/rin-gil)

### License

Проєкт OrendaUA bot поширюється за ліцензією [MIT](https://github.com/rin-gil/OrendaUAbot/blob/master/LICENCE)
