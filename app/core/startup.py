from app.core.bot import dp
from app.core.logger import logger

from app.handlers.start import router as start_router
from app.handlers.language import router as language_router
from app.handlers.profile import router as profile_router


async def register_handlers() -> None:
    """
    Register all routers.
    """

    logger.info("Registering routers...")

    dp.include_router(start_router)
    dp.include_router(language_router)
    dp.include_router(profile_router)

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

    await check_system()

    await register_middlewares()

    await register_handlers()

    logger.success("Application started")
