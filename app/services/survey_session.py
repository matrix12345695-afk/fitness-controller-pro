from dataclasses import dataclass
from typing import Optional


@dataclass
class SurveySession:
    """
    Current survey session.

    This object is stored in FSMContext and represents
    the user's current progress through the survey.
    """

    user_id: int

    report_id: Optional[int] = None

    language: str = "ru"

    current_question_id: Optional[int] = None

    current_order: int = 0

    waiting_photo: bool = False

    completed: bool = False

    def next_question(
        self,
        question_id: int,
        order: int,
        waiting_photo: bool,
    ) -> None:
        """
        Move to next question.
        """

        self.current_question_id = question_id
        self.current_order = order
        self.waiting_photo = waiting_photo

    def finish(self) -> None:
        """
        Mark survey as completed.
        """

        self.completed = True
        self.waiting_photo = False

    def to_dict(self) -> dict:
        """
        Convert session to dict for FSM storage.
        """

        return {
            "user_id": self.user_id,
            "report_id": self.report_id,
            "language": self.language,
            "current_question_id": self.current_question_id,
            "current_order": self.current_order,
            "waiting_photo": self.waiting_photo,
            "completed": self.completed,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "SurveySession":
        """
        Restore session from FSMContext.
        """

        return cls(
            user_id=data["user_id"],
            report_id=data.get("report_id"),
            language=data.get("language", "ru"),
            current_question_id=data.get("current_question_id"),
            current_order=data.get("current_order", 0),
            waiting_photo=data.get("waiting_photo", False),
            completed=data.get("completed", False),
        )
