from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def excel_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📅 Сегодня",
                    callback_data="excel_today",
                ),
                InlineKeyboardButton(
                    text="📆 Вчера",
                    callback_data="excel_yesterday",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="📈 Неделя",
                    callback_data="excel_week",
                ),
                InlineKeyboardButton(
                    text="📊 Месяц",
                    callback_data="excel_month",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="❌ Отмена",
                    callback_data="admin_back",
                ),
            ],
        ]
    )
