from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def language_keyboard():

    builder = InlineKeyboardBuilder()

    builder.button(
        text="🇷🇺 Русский",
        callback_data="lang_ru",
    )

    builder.button(
        text="🇺🇿 O'zbekcha",
        callback_data="lang_uz",
    )

    builder.adjust(1)

    return builder.as_markup()
