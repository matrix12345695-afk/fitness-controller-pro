from datetime import datetime

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.enums import Gender
from app.keyboards.reply import gender_keyboard
from app.states.registration import RegistrationState

router = Router()


@router.message(RegistrationState.gender)
async def ask_gender(message: Message) -> None:
    """
    Ask user to choose gender.
    """

    await message.answer(
        "🚻 Выберите пол:",
        reply_markup=gender_keyboard(),
    )


@router.message(
    RegistrationState.gender,
    F.text.in_(["👨 Мужской", "👩 Женский"]),
)
async def save_gender(
    message: Message,
    state: FSMContext,
) -> None:

    gender = (
        Gender.MALE
        if message.text == "👨 Мужской"
        else Gender.FEMALE
    )

    await state.update_data(
        gender=gender.value,
    )

    await state.set_state(
        RegistrationState.birth_date,
    )

    await message.answer(
        "📅 Введите дату рождения\n\n"
        "Например:\n"
        "21.05.1998"
    )


@router.message(RegistrationState.birth_date)
async def save_birth_date(
    message: Message,
    state: FSMContext,
) -> None:

    try:
        birth_date = datetime.strptime(
            message.text,
            "%d.%m.%Y",
        ).date()

    except ValueError:

        await message.answer(
            "❌ Неверный формат.\n\n"
            "Введите дату так:\n"
            "21.05.1998"
        )
        return

    await state.update_data(
        birth_date=birth_date,
    )

    await state.set_state(
        RegistrationState.height,
    )

    await message.answer(
        "📏 Введите рост (см)\n\n"
        "Например:\n"
        "182"
    )


@router.message(RegistrationState.height)
async def save_height(
    message: Message,
    state: FSMContext,
) -> None:

    if not message.text.isdigit():

        await message.answer(
            "Введите рост числом."
        )
        return

    height = int(message.text)

    if height < 100 or height > 250:

        await message.answer(
            "Рост должен быть от 100 до 250 см."
        )
        return

    await state.update_data(
        height=height,
    )

    await state.set_state(
        RegistrationState.weight,
    )

    await message.answer(
        "⚖️ Введите текущий вес\n\n"
        "Например:\n"
        "92.5"
    )


@router.message(RegistrationState.weight)
async def save_weight(
    message: Message,
    state: FSMContext,
) -> None:

    try:
        weight = float(
            message.text.replace(",", ".")
        )

    except ValueError:

        await message.answer(
            "Введите вес числом."
        )
        return

    if weight < 20 or weight > 300:

        await message.answer(
            "Введите корректный вес."
        )
        return

    await state.update_data(
        start_weight=weight,
    )

    data = await state.get_data()

    # На следующем этапе здесь будет:
    #
    # RegistrationService.create_profile(...)
    #
    # RegistrationService.finish_registration(...)
    #
    # После подключения PostgreSQL данные будут
    # сразу сохраняться в базу.

    await state.clear()

    await message.answer(
        "🎉 Регистрация успешно завершена!\n\n"
        "Добро пожаловать в Fitness Controller PRO!"
    )
