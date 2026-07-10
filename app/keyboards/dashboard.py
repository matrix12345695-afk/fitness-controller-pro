from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)


def dashboard_keyboard() -> InlineKeyboardMarkup:
    """
    Dashboard keyboard.
    """

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🔄 Обновить",
                    callback_data="dashboard_refresh",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="📢 Напомнить",
                    callback_data="dashboard_remind",
                ),
                InlineKeyboardButton(
                    text="📷 Фото",
                    callback_data="dashboard_photos",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="📥 Excel",
                    callback_data="dashboard_excel",
                ),
                InlineKeyboardButton(
                    text="📈 Статистика",
                    callback_data="dashboard_stats",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="⬅️ Назад",
                    callback_data="admin_back",
                ),
            ],
        ]
    )
