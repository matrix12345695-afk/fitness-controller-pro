from datetime import date

from sqlalchemy.ext.asyncio import AsyncSession

from app.enums import ReportStatus
from app.repositories.questions import QuestionRepository
from app.repositories.reports import ReportRepository
from app.services.question_engine import QuestionEngine


class SurveyStartService:
    """
    Starts or resumes today's survey.
    """

    def __init__(
        self,
        session: AsyncSession,
        engine: QuestionEngine,
    ):
        self.session = session

        self.engine = engine

        self.reports = ReportRepository(session)
        self.questions = QuestionRepository(session)

    async def execute(
        self,
        user_id: int,
        language: str,
    ) -> dict:
        """
        Start today's survey.

        Returns:
            {
                "report": Report,
                "question": Question,
                "language": "ru"
            }
        """

        today = date.today()

        report = await self.reports.get_by_user_and_date(
            user_id=user_id,
            report_date=today,
        )

        if report is None:

            report = await self.reports.create(
                user_id=user_id,
                report_date=today,
                status=ReportStatus.IN_PROGRESS,
            )

            await self.reports.commit()

        question = await self.engine.get_first_question()

        if question is None:

            raise RuntimeError(
                "Survey questions not found."
            )

        return {
            "report": report,
            "question": question,
            "language": language,
        }
