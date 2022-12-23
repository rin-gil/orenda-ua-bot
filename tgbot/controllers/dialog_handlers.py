"""Обробники діалогів"""

from typing import Any

from aiogram import Dispatcher
from aiogram.types import CallbackQuery, Message, InputFile

from aiogram_dialog import DialogManager, StartMode, ShowMode
from aiogram_dialog.context.storage import StorageProxy
from aiogram_dialog.manager.protocols import ManagedDialogAdapterProto
from aiogram_dialog.widgets.kbd import Button

from tgbot.config import BOT_LOGO
from tgbot.misc.states import SearchSetup
from tgbot.models.database import database
from tgbot.models.search import search


async def on_start(start_data: Any, manager: DialogManager) -> None:
    """Встановлює початкові дані для діалогу"""
    proxy: StorageProxy = manager.data["aiogd_storage_proxy"]
    await proxy.storage.set_state(user=proxy.user_id, chat=proxy.chat_id, state="dialog")
    await database.delete_user(user_id=proxy.user_id)


async def on_close(result: Any, manager: DialogManager) -> None:
    """Вмикає обробник other_type_handler після завершення діалогу"""
    await manager.data["state"].reset_state()


async def start(message: Message, dialog_manager: DialogManager) -> None:
    """Запуск діалогового вікна налаштування пошуку оголошень"""
    await message.delete()
    await dialog_manager.start(state=SearchSetup.input_city_name, mode=StartMode.RESET_STACK)


async def stop(message: Message, dialog_manager: DialogManager) -> None:
    """Скидає стан діалогу і видаляє користувача з бази даних"""
    await message.delete()
    await dialog_manager.reset_stack()
    await dialog_manager.data["state"].reset_state()
    await database.delete_user(user_id=message.from_user.id)
    await message.answer_photo(
        photo=InputFile(path_or_bytesio=BOT_LOGO),
        caption="❌ Усі твої дані видалені.\n\nЩоб налаштувати новий пошук, натисни /start",
    )


async def save_city_name(message: Message, dialog: ManagedDialogAdapterProto, manager: DialogManager) -> None:
    """Зберігає назву обраного міста"""
    await message.delete()
    manager.show_mode = ShowMode.EDIT
    if message.content_type == "text":
        manager.current_context().dialog_data["city_name"] = message.text
        await dialog.switch_to(state=SearchSetup.select_city)


async def save_selected_city(callback: CallbackQuery, select: Any, manager: DialogManager, item_id: str) -> None:
    """Зберігає обраний ідентифікатор міста та області"""
    (
        manager.current_context().dialog_data["city_id"],
        manager.current_context().dialog_data["state_id"],
    ) = item_id.split("&")
    await manager.switch_to(state=SearchSetup.input_district_name)


async def not_choosing_district(callback: CallbackQuery, button: Button, manager: DialogManager) -> None:
    """Видаляє значення, якщо користувач вирішив не вибирати район міста"""
    manager.current_context().dialog_data.pop("district_name", None)
    manager.current_context().dialog_data.pop("district_id", None)


async def save_district_name(message: Message, dialog: ManagedDialogAdapterProto, manager: DialogManager) -> None:
    """Зберігає назву вибраного району"""
    await message.delete()
    manager.show_mode = ShowMode.EDIT
    if message.content_type == "text":
        manager.current_context().dialog_data["district_name"] = message.text
        await dialog.switch_to(state=SearchSetup.select_district)


async def save_selected_district(callback: CallbackQuery, select: Any, manager: DialogManager, item_id: str) -> None:
    """Зберігає ідентифікатор вибраного району"""
    manager.current_context().dialog_data["district_id"] = item_id
    await manager.switch_to(state=SearchSetup.select_number_of_rooms)


async def save_selected_rooms(callback: CallbackQuery, select: Any, manager: DialogManager, item_id: str) -> None:
    """Зберігає кількість кімнат"""
    manager.current_context().dialog_data["rooms"] = item_id
    await manager.switch_to(state=SearchSetup.set_min_price)


async def save_min_price(message: Message, dialog: ManagedDialogAdapterProto, manager: DialogManager) -> None:
    """Зберігає мінімальну ціну"""
    await message.delete()
    manager.show_mode = ShowMode.EDIT
    if message.content_type == "text" and message.text.isdigit():
        await dialog.next()
        manager.current_context().dialog_data["min_price"] = message.text


async def save_max_price(message: Message, dialog: ManagedDialogAdapterProto, manager: DialogManager) -> None:
    """Зберігає максимальну ціну"""
    await message.delete()
    manager.show_mode = ShowMode.EDIT
    if message.content_type == "text" and message.text.isdigit():
        await dialog.next()
        manager.current_context().dialog_data["max_price"] = message.text


async def save_can_with_animals(callback: CallbackQuery, select: Any, manager: DialogManager, item_id: str) -> None:
    """Зберігає інформацію про наявність тварин"""
    manager.current_context().dialog_data["animals"] = item_id
    await manager.switch_to(state=SearchSetup.select_from_owners_only)


async def save_from_owners_only(callback: CallbackQuery, select: Any, manager: DialogManager, item_id: str) -> None:
    """Зберігає інформацію про показ оголошень тільки від власників квартир"""
    manager.current_context().dialog_data["owners"] = item_id
    await manager.switch_to(state=SearchSetup.show_search_result)


async def save_user_search_settings(callback: CallbackQuery, button: Button, manager: DialogManager) -> None:
    """Зберігає результати пошуку оголошень"""
    search_url: str = manager.current_context().dialog_data["search_url"]
    ads_ids: list = await search.get_ads_ids(search_url=search_url)
    await database.add_user(user_id=callback.from_user.id, search_url=search_url, ads_ids=ads_ids)
    await callback.message.edit_caption(
        caption="✔ Підписку оформлено!\n\n"
        "Я надсилатиму тобі нові оголошення в міру їх появи.\n"
        "Щоб скасувати підписку, введи команду /stop "
    )
    await manager.done()


async def reset_search(callback: CallbackQuery, button: Button, manager: DialogManager) -> None:
    """Скидає результати та починає новий діалог налаштування пошуку оголошень"""
    await manager.start(state=SearchSetup.input_city_name, mode=StartMode.RESET_STACK)


async def any_other_messages(message: Message, dialog: ManagedDialogAdapterProto, manager: DialogManager) -> None:
    """Видаляє необроблені повідомлення або команди від користувача"""
    await message.delete()
    manager.show_mode = ShowMode.EDIT


def register_dialog_handlers(dp: Dispatcher) -> None:
    """Реєструє обробники діалогів"""
    dp.register_message_handler(callback=start, commands="start", state="*")
    dp.register_message_handler(callback=stop, commands="stop", state="*")
