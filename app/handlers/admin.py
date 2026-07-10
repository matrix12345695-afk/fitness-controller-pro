from app.keyboards.admin import users_keyboard
from aiogram import F, Router
from aiogram.types import Message

from app.core.config import settings
from app.core.database import SessionLocal

from app.keyboards.reply import admin_menu

from app.services.admin import AdminService

router = Router()


# ==========================================================
# ADMIN PANEL
# ==========================================================

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
    Open admin panel.
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


# ==========================================================
# USERS
# ==========================================================

@router.message(
    F.text == "👥 Пользователи",
)
async def users_list(
    message: Message,
):
    """
    Show all users.
    """

    if message.from_user.id != settings.admin_id:
        return

    async with SessionLocal() as session:

        service = AdminService(session)

        users = await service.get_users()

    if not users:

        await message.answer(
            "❌ Пользователей пока нет."
        )

        return

    await message.answer(
        "👥 <b>Список пользователей</b>\n\nВыберите пользователя:",
        reply_markup=users_keyboard(users),
        parse_mode="HTML",
    )

    for index, user in enumerate(
        users,
        start=1,
    ):

        full_name = user.first_name or ""

        if user.last_name:

            full_name += (
                f" {user.last_name}"
            )

        if not full_name.strip():

            full_name = (
                f"ID {user.id}"
            )

        text += (
            f"{index}. {full_name}\n"
        )

    text += (
        f"\n👤 Всего пользователей: {len(users)}"
    )

    await message.answer(
        text,
        parse_mode="HTML",
    )
