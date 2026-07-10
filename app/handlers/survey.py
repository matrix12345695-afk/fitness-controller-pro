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
        
        if question is None:

            await message.answer(
                "Нет доступных вопросов."
            )

            return

        await state.update_data(

            report_id=report.id,

            question_id=question.id,

            question_order=question.order,

            language=user.language.value,

        )

        question_text = survey.engine.get_question_text(
            question,
            user.language.value,
        )

        if question.photo_required:

            await state.set_state(
                SurveyState.waiting_photo,
            )

            question_text += (
                "\n\n"
                "📷 Прикрепите фотографию."
            )

        else:

            await state.set_state(
                SurveyState.waiting_answer,
            )

        await message.answer(
            question_text,
        )

@router.message(
    SurveyState.waiting_answer,
    F.text,
)
async def process_answer(
    message: Message,
    state: FSMContext,
):
    """
    Process text answer.
    """

    data = await state.get_data()

    async with SessionLocal() as session:

        survey = SurveyService(
            session,
        )

        result = await survey.process_answer(
            report_id=data["report_id"],
            question_id=data["question_id"],
            text=message.text,
        )

        if not result["success"]:

            await message.answer(
                result["error"],
            )

            return

        if result["finished"]:

            await survey.finish_survey(
                data["report_id"],
            )

            await state.clear()

            language = data.get(
                "language",
                "ru",
            )

            if language == "uz":

        await message.answer(
            "✅ So'rovnoma muvaffaqiyatli yakunlandi!",
                reply_markup=main_menu_uz(
                message.from_user.id,
        )

            else:

        await message.answer(
            "✅ Опрос успешно завершён!",
            reply_markup=main_menu_ru(
                message.from_user.id,
        )

            return

        question = result["next_question"]

        await state.update_data(

            question_id=question.id,

            question_order=question.order,

        )

        question_text = survey.engine.get_question_text(
            question,
            data["language"],
        )
        
        if question.photo_required:

            await state.set_state(
                SurveyState.waiting_photo,
            )

            question_text += (
                "\n\n"
                "📷 Прикрепите фотографию."
            )

        else:

            await state.set_state(
                SurveyState.waiting_answer,
            )

        await message.answer(
            question_text,
        )

@router.message(
    SurveyState.waiting_photo,
    F.photo,
)
async def process_photo(
    message: Message,
    state: FSMContext,
):
    """
    Process photo answer.
    """

    data = await state.get_data()

    photo = message.photo[-1]

    async with SessionLocal() as session:

        survey = SurveyService(
            session,
        )

        result = await survey.process_answer(
            report_id=data["report_id"],
            question_id=data["question_id"],
            telegram_file_id=photo.file_id,
        )

        if not result["success"]:

            await message.answer(
                result["error"],
            )

            return

        if result["finished"]:

            await survey.finish_survey(
                data["report_id"],
            )

            await state.clear()

            language = data.get(
                "language",
                "ru",
            )

            if language == "uz":

        await message.answer(
            "✅ So'rovnoma muvaffaqiyatli yakunlandi!",
            reply_markup=main_menu_uz(
                message.from_user.id,
        )

            else:

        await message.answer(
            "✅ Опрос успешно завершён!",
            reply_markup=main_menu_ru(
                message.from_user.id,
        )

            return

        question = result["next_question"]

        await state.update_data(
            question_id=question.id,
            question_order=question.order,
        )

        question_text = survey.engine.get_question_text(
            question,
            data["language"],
        )

        if question.photo_required:

            await state.set_state(
                SurveyState.waiting_photo,
            )

            question_text += (
                "\n\n"
                "📷 Прикрепите фотографию."
            )

        else:

            await state.set_state(
                SurveyState.waiting_answer,
            )

        await message.answer(
            question_text,
        )

