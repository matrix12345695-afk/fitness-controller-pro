from datetime import datetime

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.core.database import SessionLocal
from app.enums import Gender, Language
from app.keyboards.reply import (
    gender_keyboard_ru,
    gender_keyboard_uz,
    main_menu_ru,
    main_menu_uz,
)
from app.schemas.profile import ProfileCreate
from app.services.registration import RegistrationService
from app.states.registration import RegistrationState
from app.services.statistics import StatisticsService

router = Router()


@router.message(
    RegistrationState.gender,
    F.text.in_(
        [
            "👨 Мужской",
            "👩 Женский",
            "👨 Erkak",
            "👩 Ayol",
        ]
    ),
)
async def save_gender(
    message: Message,
    state: FSMContext,
):

    data = await state.get_data()

    language = Language(data["language"])

    if message.text in (
        "👨 Мужской",
        "👨 Erkak",
    ):
        gender = Gender.MALE
    else:
        gender = Gender.FEMALE

    await state.update_data(
        gender=gender.value,
    )

    await state.set_state(
        RegistrationState.birth_date,
    )

    if language == Language.RU:

        await message.answer(
            "📅 Введите дату рождения\n\n"
            "Например:\n"
            "21.05.1998"
        )

    else:

        await message.answer(
            "📅 Tug'ilgan sanani kiriting\n\n"
            "Masalan:\n"
            "21.05.1998"
        )


@router.message(RegistrationState.birth_date)
async def save_birth_date(
    message: Message,
    state: FSMContext,
):

    data = await state.get_data()

    language = Language(data["language"])

    try:

        birth_date = datetime.strptime(
            message.text,
            "%d.%m.%Y",
        ).date()

    except ValueError:

        if language == Language.RU:

            await message.answer(
                "❌ Неверный формат даты."
            )

        else:

            await message.answer(
                "❌ Sana noto'g'ri."
            )

        return

    await state.update_data(
        birth_date=birth_date,
    )

    await state.set_state(
        RegistrationState.height,
    )

    if language == Language.RU:

        await message.answer(
            "📏 Введите рост (см)"
        )

    else:

        await message.answer(
            "📏 Bo'yingizni kiriting (sm)"
        )


@router.message(RegistrationState.height)
async def save_height(
    message: Message,
    state: FSMContext,
):

    if not message.text.isdigit():

        await message.answer(
            "Введите число."
        )

        return

    await state.update_data(
        height=int(message.text),
    )

    await state.set_state(
        RegistrationState.weight,
    )

    data = await state.get_data()

    if data["language"] == "ru":

        await message.answer(
            "⚖️ Введите текущий вес"
        )

    else:

        await message.answer(
            "⚖️ Vazningizni kiriting"
        )


@router.message(RegistrationState.weight)
async def save_weight(
    message: Message,
    state: FSMContext,
):

    try:

        weight = float(
            message.text.replace(",", ".")
        )

    except ValueError:

        await message.answer(
            "Введите число."
        )

        return

    await state.update_data(
        start_weight=weight,
    )

    data = await state.get_data()

    async with SessionLocal() as session:

        service = RegistrationService(
            session,
        )

        user = await service.get_user(
            message.from_user.id,
        )

        await service.finish_registration(
            user.id,
            ProfileCreate(
                full_name=message.from_user.full_name,
                gender=Gender(data["gender"]),
                birth_date=data["birth_date"],
                height=data["height"],
                start_weight=weight,
            ),
        )

    await state.clear()

    if data["language"] == "ru":

        await message.answer(
            "✅ Регистрация завершена!",
            reply_markup=main_menu_ru(
                message.from_user.id,
            ),
        )

    else:

        await message.answer(
            "✅ Ro'yxatdan o'tish yakunlandi!",
            reply_markup=main_menu_uz(
                message.from_user.id,
            ),
        )
        
# ==========================================================
# MY STATISTICS
# ==========================================================

@router.message(
    F.text.in_(
        [
            "📊 Статистика",
            "📊 Statistika",
        ]
    )
)
async def my_statistics(
    message: Message,
):
    """
    Show user statistics.
    """

    async with SessionLocal() as session:

        statistics = StatisticsService(
            session,
        )

        stats = await statistics.build_statistics(
            message.from_user.id,
        )

    if stats is None:

        await message.answer(
            "❌ Статистика пока недоступна."
        )

        return

    profile = stats["profile"]

    full_name = (
        profile.full_name
        if profile
        else message.from_user.full_name
    )

    text = (
        "📊 <b>Моя статистика</b>\n\n"

        f"👤 <b>{full_name}</b>\n\n"

        "━━━━━━━━━━━━━━\n\n"

        f"📅 Отчётов: <b>{stats['reports']}</b>\n"

        f"📝 Ответов: <b>{stats['answers']}</b>\n"

        f"📸 Фото: <b>{stats['photos']}</b>\n"

        f"📈 Выполнение: <b>{stats['completion']}%</b>\n\n"

        f"⚖️ Стартовый вес: <b>{stats['start_weight'] or '-'} кг</b>\n"

        f"⚖️ Текущий вес: <b>{stats['current_weight'] or '-'} кг</b>\n"

        f"📉 Изменение: <b>{stats['difference'] or 0} кг</b>"
    )

    if stats["last_report"]:

        text += (
            "\n\n"
            "━━━━━━━━━━━━━━\n\n"

            f"🗓 Последний отчёт:\n"
            f"<b>{stats['last_report'].created_at.strftime('%d.%m.%Y')}</b>"
        )

    await message.answer(
        text,
        parse_mode="HTML",
    )        
