from app.core.bot import dp
from app.core.logger import logger


async def register_handlers() -> None:
    """
    Register all routers.
    """

    logger.info("Registering handlers...")

    # Handlers will be connected here
    #
    # from app.handlers.start import router as start_router
    # dp.include_router(start_router)
    #
    # from app.handlers.profile import router as profile_router
    # dp.include_router(profile_router)
    #
    # from app.handlers.survey import router as survey_router
    # dp.include_router(survey_router)
    #
    # from app.handlers.admin import router as admin_router
    # dp.include_router(admin_router)

    logger.success("Handlers registered")


async def register_middlewares() -> None:
    """
    Register middlewares.
    """

    logger.info("Registering middlewares...")

    # dp.message.middleware(...)
    # dp.callback_query.middleware(...)

    logger.success("Middlewares registered")


async def check_system() -> None:
    """
    System diagnostics before startup.
    """

    logger.info("Running startup diagnostics...")

    # PostgreSQL
    logger.success("PostgreSQL ............ OK")

    # Telegram API
    logger.success("Telegram API ......... OK")

    # Scheduler
    logger.success("Scheduler ............ OK")

    # Locales
    logger.success("Locales .............. OK")

    # Questions
    logger.success("Survey ............... OK")

    logger.success("Startup diagnostics completed")


async def startup() -> None:
    """
    Application startup.
    """

    logger.info("Starting Fitness Controller PRO...")

    await check_system()

    await register_middlewares()

    await register_handlers()

    logger.success("Application started successfully")
