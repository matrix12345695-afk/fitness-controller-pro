from datetime import date

from sqlalchemy import Enum, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.enums import Gender
from app.models.base import BaseModel


class Profile(BaseModel):
    """
    User profile.
    """

    __tablename__ = "profiles"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
    )

    full_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    gender: Mapped[Gender] = mapped_column(
        Enum(Gender),
        nullable=False,
    )

    birth_date: Mapped[date]

    height: Mapped[int] = mapped_column(
        Integer,
    )

    start_weight: Mapped[float] = mapped_column(
        Float,
    )

    user = relationship(
        "User",
        back_populates="profile",
    )

    def __repr__(self) -> str:
        return f"<Profile(user_id={self.user_id})>"
