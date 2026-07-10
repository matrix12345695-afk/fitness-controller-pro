from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from app.core.config import settings
from app.core.logger import logger


# ==========================================================
# Telegram Bot
# ==========================================================

bot = Bot(
    token=settings.bot_token,
    default=DefaultBotProperties(
        parse_mode=ParseMode.HTML,
    ),
)


# ==========================================================
# FSM Storage
# ==========================================================

storage = MemoryStorage()


# ==========================================================
# Dispatcher
# ==========================================================

dp = Dispatcher(
    storage=storage,
)


# ==========================================================
# Startup
# ==========================================================

async def on_startup() -> None:
    """
    Startup hook.
    """

    logger.info("========================================")
    logger.info(" Fitness Controller PRO")
    logger.info(" Version: 1.0.0")
    logger.info("========================================")

    await bot.delete_webhook(
        drop_pending_updates=True,
    )

    await bot.set_webhook(
        url=f"{settings.webhook_url}{settings.webhook_path}",
        secret_token=settings.webhook_secret,
        drop_pending_updates=True,
    )

    logger.success("Webhook installed")
    logger.success("Bot initialized")


# ==========================================================
# Shutdown
# ==========================================================

async def on_shutdown() -> None:
    """
    Shutdown hook.
    """

    logger.info("Stopping bot...")

    await bot.delete_webhook()

    await bot.session.close()

    logger.success("Webhook removed")
    logger.success("Bot stopped")
