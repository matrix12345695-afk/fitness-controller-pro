from sqlalchemy import select

from app.core.database import SessionLocal
from app.core.logger import logger
from app.models.question import Question


QUESTIONS = [
    (1, "water", "💧 Сув норма", "💧 Suv normasi", False),
    (2, "small_wc", "🚻 Кичик хожат", "🚻 Kichik hojat", False),
    (3, "big_wc", "🚽 Катта хожат", "🚽 Katta hojat", False),
    (4, "workout", "🏋️ Машқ тури", "🏋️ Mashq turi", True),
    (5, "walking", "🚶 Пешком юриш", "🚶 Piyoda yurish", True),
    (6, "breakfast", "🍳 Нонушта", "🍳 Nonushta", True),
    (7, "lunch", "🍛 Тушлик", "🍛 Tushlik", True),
    (8, "dinner", "🍽 Кечки овқат", "🍽 Kechki ovqat", True),
    (9, "sleep", "😴 Ухлаш", "😴 Uxlash", False),
]


async def seed_questions() -> None:
    async with SessionLocal() as session:

        result = await session.execute(
            select(Question)
        )

        if result.scalars().first():

            logger.info("Survey questions already exist.")

            return

        logger.info("Creating default survey questions...")

        for order, key, ru, uz, photo in QUESTIONS:

            session.add(
                Question(
                    order=order,
                    key=key,
                    text_ru=ru,
                    text_uz=uz,
                    photo_required=photo,
                    is_active=True,
                )
            )

        await session.commit()

        logger.success("Survey questions created.")
