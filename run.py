import asyncio

from app.core.bot import bot, dp, on_shutdown, on_startup
from app.core.logger import logger
from app.core.startup import startup


async def main() -> None:
    """
    Main application entry point.
    """

    try:
        logger.info("Launching Fitness Controller PRO...")

        await startup()

        await on_startup()

        await dp.start_polling(bot)

    except (KeyboardInterrupt, SystemExit):
        logger.warning("Shutdown signal received.")

    except Exception:
        logger.exception("Unexpected application error.")
        raise

    finally:
        await on_shutdown()


if __name__ == "__main__":
    asyncio.run(main())
