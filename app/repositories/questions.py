from sqlalchemy import select

from app.models.question import Question
from app.repositories.base import BaseRepository


class QuestionRepository(BaseRepository[Question]):
    """
    Repository for survey questions.
    """

    async def get(
        self,
        question_id: int,
    ) -> Question | None:

        stmt = select(Question).where(
            Question.id == question_id
        )

        return await self.scalar(stmt)

    async def get_all(self) -> list[Question]:

        stmt = (
            select(Question)
            .order_by(Question.order)
        )

        return await self.scalars(stmt)

    async def get_active(self) -> list[Question]:

        stmt = (
            select(Question)
            .where(Question.is_active.is_(True))
            .order_by(Question.order)
        )

        return await self.scalars(stmt)

    async def get_next(
        self,
        current_order: int,
    ) -> Question | None:

        stmt = (
            select(Question)
            .where(
                Question.order > current_order,
                Question.is_active.is_(True),
            )
            .order_by(Question.order)
            .limit(1)
        )

        return await self.scalar(stmt)

    async def get_by_key(
        self,
        key: str,
    ) -> Question | None:

        stmt = select(Question).where(
            Question.key == key
        )

        return await self.scalar(stmt)

    async def create(
        self,
        order: int,
        key: str,
        text_ru: str,
        text_uz: str,
        photo_required: bool = False,
        is_active: bool = True,
    ) -> Question:

        question = Question(
            order=order,
            key=key,
            text_ru=text_ru,
            text_uz=text_uz,
            photo_required=photo_required,
            is_active=is_active,
        )

        return await self.add(question)

    async def activate(
        self,
        question: Question,
    ) -> Question:

        question.is_active = True

        await self.commit()

        return question

    async def deactivate(
        self,
        question: Question,
    ) -> Question:

        question.is_active = False

        await self.commit()

        return question
