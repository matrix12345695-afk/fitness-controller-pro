from pathlib import Path
import sys

from loguru import logger

from app.core.config import settings


LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)


logger.remove()


logger.add(
    sys.stdout,
    level=settings.log_level,
    colorize=True,
    enqueue=True,
    backtrace=True,
    diagnose=True,
    format=(
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
        "<level>{message}</level>"
    ),
)


logger.add(
    LOG_DIR / "fitness_controller.log",
    level=settings.log_level,
    rotation="10 MB",
    retention="30 days",
    compression="zip",
    enqueue=True,
    backtrace=True,
    diagnose=True,
    encoding="utf-8",
    format=(
        "{time:YYYY-MM-DD HH:mm:ss} | "
        "{level} | "
        "{name}:{function}:{line} | "
        "{message}"
    ),
)
