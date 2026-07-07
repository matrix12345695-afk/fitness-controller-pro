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
    logger.info("========================================")
    logger.info(" Fitness Controller PRO")
    logger.info(" Version: 0.1.0")
    logger.info("========================================")
    logger.info("Bot initialized")
    logger.info("Dispatcher initialized")


# ==========================================================
# Shutdown
# ==========================================================

async def on_shutdown() -> None:
    logger.info("Stopping bot...")

    await bot.session.close()

    logger.info("Bot stopped")
