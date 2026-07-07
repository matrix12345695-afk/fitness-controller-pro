from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from app.core.database import SessionLocal
from app.enums import Language
from app.keyboards.callbacks import LanguageCallback
from app.keyboards.reply import (
    gender_keyboard_ru,
    gender_keyboard_uz,
)
from app.schemas.user import UserCreate
from app.services.registration import RegistrationService
from app.states.registration import RegistrationState

router = Router()


@router.callback_query(
    LanguageCallback.filter(),
    RegistrationState.language,
)
async def select_language(
    callback: CallbackQuery,
    callback_data: LanguageCallback,
    state: FSMContext,
) -> None:
    """
    Handle language selection and create user.
    """

    language = Language(callback_data.language)

    async with SessionLocal() as session:

        service = RegistrationService(session)

        user = await service.get_user(
            callback.from_user.id,
        )

        if user is None:

            user = await service.create_user(
                UserCreate(
                    telegram_id=callback.from_user.id,
                    username=callback.from_user.username,
                    first_name=callback.from_user.first_name,
                    last_name=callback.from_user.last_name,
                ),
                language,
            )

    await state.update_data(
        language=language.value,
    )

    await state.set_state(
        RegistrationState.gender,
    )

    if language == Language.RU:

        await callback.message.edit_text(
            "🚻 <b>Выберите пол</b>"
        )

        await callback.message.answer(
            "Нажмите одну из кнопок ниже.",
            reply_markup=gender_keyboard_ru(),
        )

    else:

        await callback.message.edit_text(
            "🚻 <b>Jinsingizni tanlang</b>"
        )

        await callback.message.answer(
            "Quyidagi tugmalardan birini tanlang.",
            reply_markup=gender_keyboard_uz(),
        )

    await callback.answer()
