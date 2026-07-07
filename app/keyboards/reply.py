from aiogram.types import KeyboardButton
from aiogram.types import ReplyKeyboardMarkup


def gender_keyboard_ru():

    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(
                    text="👨 Мужской",
                ),
                KeyboardButton(
                    text="👩 Женский",
                ),
            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def gender_keyboard_uz():

    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(
                    text="👨 Erkak",
                ),
                KeyboardButton(
                    text="👩 Ayol",
                ),
            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def main_menu_ru():

    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(
                    text="📝 Пройти опрос",
                )
            ],
            [
                KeyboardButton(
                    text="👤 Мой профиль",
                ),
                KeyboardButton(
                    text="📊 Статистика",
                ),
            ],
            [
                KeyboardButton(
                    text="ℹ️ Помощь",
                )
            ],
        ],
        resize_keyboard=True,
    )


def main_menu_uz():

    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(
                    text="📝 So'rovnomani boshlash",
                )
            ],
            [
                KeyboardButton(
                    text="👤 Profil",
                ),
                KeyboardButton(
                    text="📊 Statistika",
                ),
            ],
            [
                KeyboardButton(
                    text="ℹ️ Yordam",
                )
            ],
        ],
        resize_keyboard=True,
    )


def admin_menu():

    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(
                    text="👥 Пользователи",
                )
            ],
            [
                KeyboardButton(
                    text="📊 Отчёты",
                ),
                KeyboardButton(
                    text="📈 Статистика",
                ),
            ],
            [
                KeyboardButton(
                    text="📤 Excel",
                ),
                KeyboardButton(
                    text="⚙️ Настройки",
                ),
            ],
        ],
        resize_keyboard=True,
    )
