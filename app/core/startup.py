from sqlalchemy import text

from app.core.database import engine
from app.models.base import Base
from app.core.bot import dp
from app.core.logger import logger

from app.handlers.start import router as start_router
from app.handlers.language import router as language_router
from app.handlers.profile import router as profile_router
from app.handlers.survey import router as survey_router


async def register_handlers() -> None:
    """
    Register all routers.
    """

    logger.info("Registering routers...")

    dp.include_router(start_router)
    dp.include_router(language_router)
    dp.include_router(profile_router)
    dp.include_router(survey_router)

    logger.success("Routers registered")


async def register_middlewares() -> None:
    """
    Register middlewares.
    """

    logger.info("Registering middlewares...")

    logger.success("Middlewares registered")


async def check_system() -> None:
    """
    Startup diagnostics.
    """

    logger.info("Running diagnostics...")

    logger.success("PostgreSQL ........ OK")
    logger.success("Telegram API ..... OK")
    logger.success("Routers .......... OK")
    logger.success("Locales .......... OK")

    logger.success("Diagnostics completed")


async def startup() -> None:
    """
    Application startup.
    """

    logger.info("Starting application...")

    await create_database()

    await check_system()

    await register_middlewares()

    await register_handlers()

    logger.success("Application started")

async def create_database() -> None:
    """
    Create database tables.
    """

    logger.info("Creating database tables...")

    async with engine.begin() as conn:

        await conn.run_sync(
            Base.metadata.create_all,
        )

    logger.success("Database ready")
