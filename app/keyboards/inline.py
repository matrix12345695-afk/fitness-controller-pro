from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.keyboards.callbacks import LanguageCallback


def language_keyboard():

    builder = InlineKeyboardBuilder()

    builder.row(
        InlineKeyboardButton(
            text="🇷🇺 Русский",
            callback_data=LanguageCallback(
                language="ru",
            ).pack(),
        )
    )

    builder.row(
        InlineKeyboardButton(
            text="🇺🇿 O'zbekcha",
            callback_data=LanguageCallback(
                language="uz",
            ).pack(),
        )
    )

    return builder.as_markup()
