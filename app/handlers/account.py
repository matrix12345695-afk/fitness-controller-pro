from aiogram import F, Router
from aiogram.types import Message

from app.core.database import SessionLocal
from app.services.account import AccountService

router = Router()


@router.message(
    F.text.in_(
        [
            "👤 Мой профиль",
            "👤 Profil",
        ]
    )
)
async def my_profile(
    message: Message,
):
    """
    Show user profile.
    """

    async with SessionLocal() as session:

        service = AccountService(
            session,
        )

        account = await service.get_account(
            message.from_user.id,
        )

        if account is None:

            await message.answer(
                "❌ Профиль не найден."
            )

            return

        if account["gender"] == "MALE":
            gender = "👨 Мужской"
        else:
            gender = "👩 Женский"

        last_report = "Нет"

        if account["last_report"]:

            last_report = account[
                "last_report"
            ].created_at.strftime(
                "%d.%m.%Y"
            )

        text = (
            "👤 <b>МОЙ ПРОФИЛЬ</b>\n\n"

            f"👨 <b>Имя:</b> {account['full_name']}\n"

            f"{gender}\n"

            f"🎂 <b>Дата рождения:</b> "
            f"{account['birth_date']:%d.%m.%Y}\n"

            f"📏 <b>Рост:</b> "
            f"{account['height']} см\n"

            f"⚖️ <b>Вес:</b> "
            f"{account['start_weight']} кг\n\n"

            "━━━━━━━━━━━━━━\n"

            "📊 <b>СТАТИСТИКА</b>\n\n"

            f"✅ Опросов: {account['reports']}\n"

            f"📅 Последний отчёт: {last_report}"
        )

        await message.answer(
            text,
            parse_mode="HTML",
        )
