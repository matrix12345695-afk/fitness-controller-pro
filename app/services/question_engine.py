from app.models.question import Question
from app.repositories.questions import QuestionRepository


class QuestionEngine:
    """
    Universal survey engine.

    This class knows nothing about Telegram.
    It only manages the survey flow.
    """

    def __init__(
        self,
        question_repository: QuestionRepository,
    ):
        self.questions = question_repository

    async def get_questions(self) -> list[Question]:
        """
        Return all active questions.
        """
        return await self.questions.get_active()

    async def get_first_question(self) -> Question | None:
        """
        Return first active question.
        """
        questions = await self.questions.get_active()

        if not questions:
            return None

        return questions[0]

    async def get_next_question(
        self,
        current_order: int,
    ) -> Question | None:
        """
        Return next question.
        """
        return await self.questions.get_next(current_order)

    async def has_next(
        self,
        current_order: int,
    ) -> bool:
        """
        Check if next question exists.
        """
        question = await self.get_next_question(
            current_order
        )

        return question is not None

    async def is_last(
        self,
        current_order: int,
    ) -> bool:
        """
        Check if current question is last.
        """
        return not await self.has_next(
            current_order
        )

    def validate_answer(
        self,
        question: Question,
        text: str | None = None,
        has_photo: bool = False,
    ) -> tuple[bool, str | None]:
        """
        Validate answer before saving.
        """

        if question.photo_required:

            if not has_photo:
                return (
                    False,
                    "Для этого вопроса необходимо прикрепить фотографию.",
                )

        if text is not None:

            text = text.strip()

            if len(text) == 0:
                return (
                    False,
                    "Ответ не может быть пустым.",
                )

        return (
            True,
            None,
        )

    def get_question_text(
        self,
        question: Question,
        language: str,
    ) -> str:
        """
        Return localized question text.
        """

        if language == "uz":
            return question.text_uz

        return question.text_ru
