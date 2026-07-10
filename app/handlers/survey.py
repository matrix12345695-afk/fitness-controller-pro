from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.core.database import SessionLocal
from app.keyboards.reply import (
    main_menu_ru,
    main_menu_uz,
)
from app.services.registration import RegistrationService
from app.services.survey import SurveyService
from app.states.survey import SurveyState

router = Router()


# ============================================================
# START SURVEY
# ============================================================

@router.message(
    F.text.in_(
        [
            "📝 Пройти опрос",
            "📝 So'rovnomani boshlash",
        ]
    )
)
async def start_survey(
    message: Message,
    state: FSMContext,
):
    """
    Start today's survey.
    """

    await state.clear()

    async with SessionLocal() as session:

        registration = RegistrationService(
            session,
        )

        user = await registration.get_user(
            message.from_user.id,
        )

        if user is None:

            await message.answer(
                "Сначала необходимо пройти регистрацию."
            )

            return

        survey = SurveyService(
            session,
        )

        result = await survey.start_survey(
            user_id=user.id,
            language=user.language.value,
        )

        report = result["report"]
        question = result["question"]

        await state.update_data(

            report_id=report.id,

            question_id=question.id,

            question_order=question.order,

            language=user.language.value,

        )

        await state.set_state(
            SurveyState.waiting_answer,
        )

        question_text = survey.engine.get_question_text(
            question,
            user.language.value,
        )

        if question.photo_required:

            question_text += (
                "\n\n"
                "📷 Прикрепите фотографию."
            )

        await message.answer(
            question_text,
        )
