from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import BaseModel


class UserProgress(BaseModel):
    """
    User statistics.
    """

    __tablename__ = "user_progress"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )

    streak: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    total_reports: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    missed_reports: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )
