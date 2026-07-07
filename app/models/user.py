from datetime import datetime

from sqlalchemy import BigInteger, Boolean, DateTime, Enum, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.enums import Language, Role
from app.models.base import BaseModel


class User(BaseModel):
    """
    Telegram user.
    """

    __tablename__ = "users"

    telegram_id: Mapped[int] = mapped_column(
        BigInteger,
        unique=True,
        nullable=False,
        index=True,
    )

    username: Mapped[str | None] = mapped_column(
        String(64),
        nullable=True,
    )

    first_name: Mapped[str] = mapped_column(
        String(128),
        nullable=False,
    )

    last_name: Mapped[str | None] = mapped_column(
        String(128),
        nullable=True,
    )

    language: Mapped[Language] = mapped_column(
        Enum(Language),
        default=Language.RU,
        nullable=False,
    )

    role: Mapped[Role] = mapped_column(
        Enum(Role),
        default=Role.USER,
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    registered_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    profile = relationship(
        "Profile",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
    )

    reports = relationship(
        "Report",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return (
            f"<User(id={self.id}, "
            f"telegram_id={self.telegram_id}, "
            f"role={self.role})>"
        )
