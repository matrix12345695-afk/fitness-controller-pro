from aiogram.types import KeyboardButton
from aiogram.types import ReplyKeyboardMarkup

from app.core.config import settings


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


def main_menu_ru(
    telegram_id: int | None = None,
):

    keyboard = [
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
    ]

    if telegram_id == settings.admin_id:

        keyboard.append(
            [
                KeyboardButton(
                    text="👨‍💼 Админ",
                )
            ]
        )

    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
    )


def main_menu_uz(
    telegram_id: int | None = None,
):

    keyboard = [
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
    ]

    if telegram_id == settings.admin_id:

        keyboard.append(
            [
                KeyboardButton(
                    text="👨‍💼 Admin",
                )
            ]
        )


    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
    )


def admin_menu():

    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(
                    text="👥 Пользователи",
                ),
                KeyboardButton(
                    text="📊 Сегодня",
                ),
            ],
            [
                KeyboardButton(
                    text="📈 Статистика",
                ),
                KeyboardButton(
                    text="📷 Фотографии",
                ),
            ],
            [
                KeyboardButton(
                    text="📥 Excel",
                ),
                KeyboardButton(
                    text="⚙️ Настройки",
                ),
            ],
            [
                KeyboardButton(
                    text="⬅️ Назад",
                ),
            ],
        ],
        resize_keyboard=True,
    )
