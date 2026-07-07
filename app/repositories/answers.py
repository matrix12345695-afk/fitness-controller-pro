from sqlalchemy import select

from app.models.answer import Answer
from app.repositories.base import BaseRepository


class AnswerRepository(BaseRepository[Answer]):
    """
    Repository for survey answers.
    """

    async def get(
        self,
        answer_id: int,
    ) -> Answer | None:
        """
        Get answer by ID.
        """

        stmt = select(Answer).where(
            Answer.id == answer_id
        )

        return await self.scalar(stmt)

    async def create(
        self,
        report_id: int,
        question_id: int,
        answer: str,
    ) -> Answer:
        """
        Create new answer.
        """

        obj = Answer(
            report_id=report_id,
            question_id=question_id,
            answer=answer,
        )

        return await self.add(obj)

    async def get_by_report(
        self,
        report_id: int,
    ) -> list[Answer]:
        """
        Get all answers of report.
        """

        stmt = (
            select(Answer)
            .where(
                Answer.report_id == report_id
            )
            .order_by(
                Answer.question_id
            )
        )

        return await self.scalars(stmt)

    async def get_by_question(
        self,
        question_id: int,
    ) -> list[Answer]:
        """
        Get all answers for one question.
        """

        stmt = (
            select(Answer)
            .where(
                Answer.question_id == question_id
            )
        )

        return await self.scalars(stmt)

    async def get_by_report_and_question(
        self,
        report_id: int,
        question_id: int,
    ) -> Answer | None:
        """
        Get answer for one question inside report.
        """

        stmt = (
            select(Answer)
            .where(
                Answer.report_id == report_id,
                Answer.question_id == question_id,
            )
        )

        return await self.scalar(stmt)

    async def update_answer(
        self,
        answer: Answer,
        value: str,
    ) -> Answer:
        """
        Update answer text.
        """

        answer.answer = value

        await self.commit()

        return answer

    async def delete_answer(
        self,
        answer: Answer,
    ) -> None:
        """
        Delete answer.
        """

        await self.delete(answer)

        await self.commit()
