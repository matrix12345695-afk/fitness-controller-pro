from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import BaseModel


class SurveySession(BaseModel):
    """
    Current survey progress.
    """

    __tablename__ = "survey_sessions"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )

    report_id: Mapped[int] = mapped_column(
        ForeignKey("reports.id", ondelete="CASCADE"),
        nullable=False,
    )

    current_question: Mapped[int] = mapped_column(
        Integer,
        default=1,
    )

    waiting_photo: Mapped[bool] = mapped_column(
        default=False,
    )
