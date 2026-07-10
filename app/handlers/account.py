from aiogram import F, Router
from aiogram.types import Message

from app.core.database import SessionLocal
from app.services.account import AccountService
from app.services.registration import RegistrationService

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

        registration = RegistrationService(
            session,
        )

        user = await registration.get_user(
            message.from_user.id,
        )

        if user is None:

            await message.answer(
                "❌ Пользователь не найден."
            )

            return

        service = AccountService(
            session,
        )

        account = await service.get_account(
            user.id,
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

            last_report = (
                account["last_report"]
                .created_at.strftime("%d.%m.%Y")
            )

        birth_date = "-"

        if account["birth_date"]:

            birth_date = account["birth_date"].strftime(
                "%d.%m.%Y"
            )

        text = (
            "👤 <b>МОЙ ПРОФИЛЬ</b>\n\n"

            f"👨 <b>Имя:</b> {account['full_name']}\n"

            f"{gender}\n"

            f"🎂 <b>Дата рождения:</b> {birth_date}\n"

            f"📏 <b>Рост:</b> {account['height']} см\n"

            f"⚖️ <b>Вес:</b> {account['start_weight']} кг\n\n"

            "━━━━━━━━━━━━━━━━━━\n\n"

            "📊 <b>СТАТИСТИКА</b>\n\n"

            f"✅ Пройдено опросов: {account['reports']}\n"

            f"📅 Последний отчёт: {last_report}"
        )

        await message.answer(
            text,
            parse_mode="HTML",
        )
