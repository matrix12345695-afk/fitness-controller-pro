from aiogram import F, Router
from aiogram.types import Message

from app.core.config import settings
from app.keyboards.reply import admin_menu

router = Router()


@router.message(
    F.text.in_(
        [
            "👨‍💼 Админ",
            "👨‍💼 Admin",
        ]
    )
)
async def admin_panel(
    message: Message,
):
    """
    Admin panel.
    """

    if message.from_user.id != settings.admin_id:

        await message.answer(
            "⛔ У вас нет доступа."
        )

        return

    text = (
        "👨‍💼 <b>Панель администратора</b>\n\n"

        "Добро пожаловать!\n\n"

        "Выберите необходимый раздел."
    )

    await message.answer(
        text,
        reply_markup=admin_menu(),
        parse_mode="HTML",
    )
