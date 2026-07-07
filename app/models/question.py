from sqlalchemy import Boolean, Integer, String, Text

from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import BaseModel


class Question(BaseModel):
    """
    Survey question.
    """

    __tablename__ = "questions"

    order: Mapped[int] = mapped_column(
        Integer,
        unique=True,
        nullable=False,
    )

    key: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
    )

    text_ru: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    text_uz: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    photo_required: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    def __repr__(self) -> str:
        return f"<Question(key={self.key})>"
