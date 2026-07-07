from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from app.enums import Language
from app.keyboards.callbacks import LanguageCallback
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
):
    """
    Language selection.
    """

    language = Language(callback_data.language)

    await state.update_data(
        language=language.value,
    )

    await state.set_state(
        RegistrationState.gender,
    )

    text = (
        "🚻 Выберите пол.\n\n"
        "Или\n\n"
        "🚻 Jinsingizni tanlang."
    )

    await callback.message.edit_text(text)

    await callback.answer()
