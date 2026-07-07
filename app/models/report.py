from datetime import date

from sqlalchemy import Date, Enum, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.enums import ReportStatus
from app.models.base import BaseModel


class Report(BaseModel):
    """
    Daily report.
    """

    __tablename__ = "reports"

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "report_date",
            name="uq_user_report_date",
        ),
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    report_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        index=True,
    )

    status: Mapped[ReportStatus] = mapped_column(
        Enum(ReportStatus),
        default=ReportStatus.IN_PROGRESS,
        nullable=False,
    )

    user = relationship(
        "User",
        back_populates="reports",
    )

    answers = relationship(
        "Answer",
        back_populates="report",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return (
            f"<Report(user={self.user_id}, "
            f"date={self.report_date})>"
        )
