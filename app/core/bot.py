from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from app.core.config import settings
from app.core.logger import logger


# ==========================================================
# BOT
# ==========================================================

bot = Bot(
    token=settings.bot_token,
    default=DefaultBotProperties(
        parse_mode=ParseMode.HTML,
    ),
)


# ==========================================================
# STORAGE
# ==========================================================

storage = MemoryStorage()


# ==========================================================
# DISPATCHER
# ==========================================================

dp = Dispatcher(
    storage=storage,
)


# ==========================================================
# STARTUP
# ==========================================================

async def on_startup() -> None:
    """
    Bot startup.
    """

    logger.info("=======================================")
    logger.info("Fitness Controller PRO")
    logger.info("Webhook mode")
    logger.info("=======================================")

    webhook_url = (
        settings.webhook_url.rstrip("/")
        + settings.webhook_path
    )

    await bot.delete_webhook(
        drop_pending_updates=True,
    )

    await bot.set_webhook(
        url=webhook_url,
        secret_token=settings.webhook_secret,
        drop_pending_updates=True,
    )

    logger.success(f"Webhook installed: {webhook_url}")

    me = await bot.get_me()

    logger.success(
        f"Authorized as @{me.username}"
    )


# ==========================================================
# SHUTDOWN
# ==========================================================

async def on_shutdown() -> None:
    """
    Bot shutdown.
    """

    logger.info("Removing webhook...")

    try:
        await bot.delete_webhook()

    except Exception as e:
        logger.warning(
            f"Webhook remove error: {e}"
        )

    await bot.session.close()

    logger.success("Bot stopped")
