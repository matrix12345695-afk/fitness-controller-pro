import asyncio

from aiohttp import web

from app.core.bot import (
    bot,
    dp,
    on_shutdown,
    on_startup,
)
from app.core.config import settings
from app.core.logger import logger
from app.core.startup import startup
from app.core.webhook import (
    create_web_app,
    register_routes,
)


async def main() -> None:
    """
    Main application entry point.
    """

    logger.info("Launching Fitness Controller PRO...")

    await startup()

    await on_startup()

    app = create_web_app(
        bot=bot,
        dp=dp,
    )

    register_routes(app)

    runner = web.AppRunner(app)

    await runner.setup()

    site = web.TCPSite(
        runner=runner,
        host="0.0.0.0",
        port=settings.port,
    )

    await site.start()

    logger.success(
        f"Webhook started on port {settings.port}"
    )

    try:

        while True:
            await asyncio.sleep(3600)

    except (KeyboardInterrupt, SystemExit):

        logger.warning("Shutdown signal received.")

    finally:

        await on_shutdown()

        await runner.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
