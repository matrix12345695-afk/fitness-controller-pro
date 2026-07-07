from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel


class Photo(BaseModel):
    """
    Telegram photo linked to an answer.
    """

    __tablename__ = "photos"

    answer_id: Mapped[int] = mapped_column(
        ForeignKey("answers.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    telegram_file_id: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    answer = relationship(
        "Answer",
        back_populates="photos",
    )

    def __repr__(self) -> str:
        return f"<Photo(answer_id={self.answer_id})>"
