from aiogram.types import (
    KeyboardButton,
    ReplyKeyboardMarkup,
)


def gender_keyboard() -> ReplyKeyboardMarkup:
    """
    Gender selection keyboard.
    """

    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="👨 Мужской"),
                KeyboardButton(text="👩 Женский"),
            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Выберите пол",
    )


def main_menu_ru() -> ReplyKeyboardMarkup:
    """
    Russian main menu.
    """

    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="📝 Пройти опрос"),
            ],
            [
                KeyboardButton(text="👤 Мой профиль"),
                KeyboardButton(text="📊 Моя статистика"),
            ],
            [
                KeyboardButton(text="ℹ️ Помощь"),
            ],
        ],
        resize_keyboard=True,
    )


def main_menu_uz() -> ReplyKeyboardMarkup:
    """
    Uzbek main menu.
    """

    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="📝 So'rovnomani boshlash"),
            ],
            [
                KeyboardButton(text="👤 Mening profilim"),
                KeyboardButton(text="📊 Mening statistikam"),
            ],
            [
                KeyboardButton(text="ℹ️ Yordam"),
            ],
        ],
        resize_keyboard=True,
    )


def admin_menu() -> ReplyKeyboardMarkup:
    """
    Administrator menu.
    """

    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="📊 Статистика"),
                KeyboardButton(text="📁 Отчёты"),
            ],
            [
                KeyboardButton(text="📤 Excel"),
                KeyboardButton(text="👥 Пользователи"),
            ],
            [
                KeyboardButton(text="⚙️ Настройки"),
            ],
        ],
        resize_keyboard=True,
    )
