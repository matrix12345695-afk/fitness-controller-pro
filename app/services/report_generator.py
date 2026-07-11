from datetime import date

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.answer import Answer
from app.models.photo import Photo
from app.models.profile import Profile
from app.models.report import Report
from app.models.user import User


class ReportGeneratorService:
    """
    Prepare data for Excel export.
    """

    def __init__(
        self,
        session: AsyncSession,
    ):
        self.session = session

    # ==========================================================
    # DASHBOARD
    # ==========================================================

    async def dashboard(
        self,
        report_date: date | None = None,
    ) -> dict:
        """
        Dashboard statistics.
        """

        if report_date is None:
            report_date = date.today()

        total_users = (
            await self.session.execute(
                select(func.count(User.id))
            )
        ).scalar_one()

        completed = (
            await self.session.execute(
                select(func.count(Report.id)).where(
                    Report.report_date == report_date
                )
            )
        ).scalar_one()

        photos = (
            await self.session.execute(
                select(func.count(Photo.id))
            )
        ).scalar_one()

        avg_weight = (
            await self.session.execute(
                select(func.avg(Profile.start_weight))
            )
        ).scalar()

        not_completed = max(
            total_users - completed,
            0,
        )

        percent = (
            round(
                completed / total_users * 100
            )
            if total_users
            else 0
        )

        return {
            "date": report_date,
            "total_users": total_users,
            "completed": completed,
            "not_completed": not_completed,
            "percent": percent,
            "photos": photos,
            "average_weight": round(
                avg_weight or 0,
                1,
            ),
        }

    # ==========================================================
    # ANSWERS
    # ==========================================================

    async def answers(
        self,
        report_date: date | None = None,
    ) -> list[dict]:
        """
        Export answers for selected date.
        """

        if report_date is None:
            report_date = date.today()

        stmt = (
            select(Report)
            .where(
                Report.report_date == report_date
            )
            .options(
                selectinload(
                    Report.user
                ),
                selectinload(
                    Report.answers
                ).selectinload(
                    Answer.question
                ),
                selectinload(
                    Report.answers
                ).selectinload(
                    Answer.photos
                ),
            )
        )

        reports = (
            await self.session.execute(stmt)
        ).scalars().all()

        rows = []

        for report in reports:

            user = report.user

            full_name = (
                f"{user.first_name} {user.last_name or ''}"
            ).strip()

            for answer in report.answers:

                rows.append(
                    {
                        "user": full_name,
                        "date": report.report_date.strftime(
                            "%d.%m.%Y"
                        ),
                        "question": answer.question.text_ru,
                        "answer": answer.answer,
                        "photos": len(answer.photos),
                    }
                )

        return rows
