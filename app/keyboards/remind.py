from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)


def remind_confirm_keyboard() -> InlineKeyboardMarkup:
    """
    Reminder confirmation keyboard.
    """

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Отправить",
                    callback_data="remind_send",
                ),
                InlineKeyboardButton(
                    text="❌ Отмена",
                    callback_data="remind_cancel",
                ),
            ]
        ]
    )
