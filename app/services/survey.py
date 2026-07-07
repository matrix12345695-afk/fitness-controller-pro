from sqlalchemy.ext.asyncio import AsyncSession

from app.services.base import BaseService
from app.services.question_engine import QuestionEngine
from app.services.survey_answer import SurveyAnswerService
from app.services.survey_finish import SurveyFinishService
from app.services.survey_start import SurveyStartService


class SurveyService(BaseService):
    """
    Main Survey Service.

    Acts as facade for the whole survey process.
    """

    def __init__(
        self,
        session: AsyncSession,
    ):
        super().__init__(session)

        self.engine = QuestionEngine(session)

        self.start = SurveyStartService(
            session,
            self.engine,
        )

        self.answer = SurveyAnswerService(
            session,
            self.engine,
        )

        self.finish = SurveyFinishService(
            session,
        )

    async def start_survey(
        self,
        user_id: int,
        language: str,
    ):
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
    ):
        """
        Save answer and move to next question.
        """

        return await self.answer.execute(
            report_id=report_id,
            question_id=question_id,
            text=text,
            telegram_file_id=telegram_file_id,
        )

    async def finish_survey(
        self,
        report_id: int,
    ):
        """
        Complete report.
        """

        return await self.finish.execute(
            report_id=report_id,
        )
