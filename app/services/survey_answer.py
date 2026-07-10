from sqlalchemy.ext.asyncio import AsyncSession

from app.models.question import Question
from app.repositories.answers import AnswerRepository
from app.repositories.photos import PhotoRepository
from app.services.question_engine import QuestionEngine


class SurveyAnswerService:
    """
    Process survey answers.
    """

    def __init__(
        self,
        session: AsyncSession,
        engine: QuestionEngine,
    ):
        self.session = session
        self.engine = engine

        self.answers = AnswerRepository(session)
        self.photos = PhotoRepository(session)

    async def execute(
        self,
        report_id: int,
        question: Question,
        text: str | None = None,
        telegram_file_id: str | None = None,
    ) -> dict:
        """
        Save answer and move to next question.
        """

        has_photo = telegram_file_id is not None

        valid, error = self.engine.validate_answer(
            question=question,
            text=text,
            has_photo=has_photo,
        )

        if not valid:
            return {
                "success": False,
                "error": error,
            }

        answer = await self.answers.create(
            report_id=report_id,
            question_id=question.id,
            answer=text or "",
        )

        await self.answers.commit()

        if telegram_file_id:

            await self.photos.create(
                answer_id=answer.id,
                telegram_file_id=telegram_file_id,
            )

            await self.photos.commit()

        next_question = await self.engine.get_next_question(
            question.order,
        )

        return {
            "success": True,
            "finished": next_question is None,
            "answer": answer,
            "next_question": next_question,
        }
