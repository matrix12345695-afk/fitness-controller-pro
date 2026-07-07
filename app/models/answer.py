from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel


class Answer(BaseModel):
    """
    Answer for survey question.
    """

    __tablename__ = "answers"

    report_id: Mapped[int] = mapped_column(
        ForeignKey("reports.id", ondelete="CASCADE"),
        nullable=False,
    )

    question_id: Mapped[int] = mapped_column(
        ForeignKey("questions.id", ondelete="CASCADE"),
        nullable=False,
    )

    answer: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    report = relationship(
        "Report",
        back_populates="answers",
    )

    question = relationship(
        "Question",
    )

    photos = relationship(
        "Photo",
        back_populates="answer",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return (
            f"<Answer(report={self.report_id}, "
            f"question={self.question_id})>"
        )
