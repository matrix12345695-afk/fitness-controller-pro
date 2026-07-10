from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.questions import QuestionRepository
from app.services.base import BaseService
from app.services.question_engine import QuestionEngine
from app.services.survey_answer import SurveyAnswerService
from app.services.survey_finish import SurveyFinishService
from app.services.survey_start import SurveyStartService


class SurveyService(BaseService):
    """
    Main Survey Service.

    Facade for the whole survey process.
    """

    def __init__(
        self,
        session: AsyncSession,
    ):
        super().__init__(session)

        question_repository = QuestionRepository(
            session,
        )

        self.engine = QuestionEngine(
            question_repository,
        )

        self.start = SurveyStartService(
            session=session,
            engine=self.engine,
        )

        self.answer = SurveyAnswerService(
            session=session,
            engine=self.engine,
        )

        self.finish = SurveyFinishService(
            session=session,
        )

    async def start_survey(
        self,
        user_id: int,
        language: str,
    ) -> dict:
        """
        Start today's survey.
        """

        return await self.start.execute(
            user_id=user_id,
            language=language,
        )

    async def process_answer(
        self,
        report_id: int,
        question_id: int,
        text: str | None = None,
        telegram_file_id: str | None = None,
    ) -> dict:
        """
        Process survey answer.
        """

        question = await self.engine.get_question(
            question_id,
        )

        if question is None:
            return {
                "success": False,
                "error": "Question not found.",
            }

        return await self.answer.execute(
            report_id=report_id,
            question=question,
            text=text,
            telegram_file_id=telegram_file_id,
        )

    async def finish_survey(
        self,
        report_id: int,
    ) -> dict:
        """
        Finish survey.
        """

        return await self.finish.execute(
            report_id=report_id,
        )
