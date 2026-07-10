from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)


def users_keyboard(users):
    """
    Inline keyboard with users.
    """

    keyboard = []

    for user in users:

        full_name = user.first_name or ""

        if user.last_name:
            full_name += f" {user.last_name}"

        if not full_name.strip():
            full_name = f"ID {user.id}"

        keyboard.append(
            [
                InlineKeyboardButton(
                    text=f"👤 {full_name}",
                    callback_data=f"user:{user.id}",
                )
            ]
        )

    keyboard.append(
        [
            InlineKeyboardButton(
                text="⬅️ Назад",
                callback_data="admin_back",
            )
        ]
    )

    return InlineKeyboardMarkup(
        inline_keyboard=keyboard,
    )
