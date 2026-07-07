from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import BaseModel


class Settings(BaseModel):
    """
    Global bot settings.
    """

    __tablename__ = "settings"

    survey_start_hour: Mapped[int] = mapped_column(Integer, default=20)

    survey_start_minute: Mapped[int] = mapped_column(Integer, default=0)

    reminder1_hour: Mapped[int] = mapped_column(Integer, default=21)

    reminder1_minute: Mapped[int] = mapped_column(Integer, default=0)

    reminder2_hour: Mapped[int] = mapped_column(Integer, default=22)

    reminder2_minute: Mapped[int] = mapped_column(Integer, default=0)

    survey_close_hour: Mapped[int] = mapped_column(Integer, default=23)

    survey_close_minute: Mapped[int] = mapped_column(Integer, default=0)

    default_language: Mapped[str] = mapped_column(
        String(5),
        default="ru",
    )

    registration_enabled: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )
