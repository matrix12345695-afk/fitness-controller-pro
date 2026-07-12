from pathlib import Path
from uuid import uuid4

from aiogram import Bot
from loguru import logger


class PhotoExportService:
    """
    Downloads Telegram photos for Excel export.
    """

    def __init__(
        self,
        bot: Bot,
    ):
        self.bot = bot

        self.temp_dir = Path(
            "exports/photos"
        )

        self.temp_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

    # =====================================================
    # DOWNLOAD ONE PHOTO
    # =====================================================

    async def download(
        self,
        telegram_file_id: str,
    ) -> Path:
        """
        Download one photo from Telegram.
        """

        if not telegram_file_id:

            raise ValueError(
                "telegram_file_id is empty."
            )

        file = await self.bot.get_file(
            telegram_file_id,
        )

        filename = (
            self.temp_dir
            / f"{uuid4().hex}.jpg"
        )

        await self.bot.download_file(
            file.file_path,
            destination=filename,
        )

        logger.info(
            "Downloaded photo: {}",
            filename.name,
        )

        return filename

    # =====================================================
    # DOWNLOAD MANY
    # =====================================================

    async def download_many(
        self,
        telegram_file_ids: list[str],
    ) -> list[Path]:
        """
        Download multiple Telegram photos.
        """

        paths: list[Path] = []

        for telegram_file_id in telegram_file_ids:

            if not telegram_file_id:
                continue

            try:

                path = await self.download(
                    telegram_file_id,
                )

                paths.append(
                    path,
                )

            except Exception as e:

                logger.exception(
                    e,
                )

        return paths

    # =====================================================
    # CLEANUP
    # =====================================================

    def cleanup(
        self,
    ):
        """
        Remove temporary photos.
        """

        removed = 0

        for image in self.temp_dir.glob(
            "*.jpg",
        ):

            try:

                image.unlink()

                removed += 1

            except Exception as e:

                logger.exception(
                    e,
                )

        logger.info(
            "Removed {} temporary photos.",
            removed,
        )
