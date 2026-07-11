from pathlib import Path

from aiogram import Bot


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

    async def download(
        self,
        telegram_file_id: str,
    ) -> Path:
        """
        Download photo from Telegram.
        """

        file = await self.bot.get_file(
            telegram_file_id,
        )

        filename = (
            self.temp_dir
            / f"{telegram_file_id}.jpg"
        )

        await self.bot.download_file(
            file.file_path,
            destination=filename,
        )

        return filename

    def cleanup(
        self,
    ):

        for image in self.temp_dir.glob(
            "*.jpg"
        ):

            try:
                image.unlink()

            except Exception:
                pass
