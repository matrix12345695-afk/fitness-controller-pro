from datetime import date, timedelta

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
        date_from: date | None = None,
        date_to: date | None = None,
    ) -> dict:
        """
        Dashboard statistics.
        """

        if date_to is None:
            date_to = date.today()

        if date_from is None:
            date_from = date_to

        total_users = (
            await self.session.execute(
                select(func.count(User.id))
            )
        ).scalar_one()

        completed = (
            await self.session.execute(
                select(func.count(Report.id)).where(
                    Report.report_date.between(
                        date_from,
                        date_to,
                    )
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
            "date": date_to,
            "date_from": date_from,
            "date_to": date_to,
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
        date_from: date | None = None,
        date_to: date | None = None,
    )
        """
        Export answers for selected date.
        """

        if date_to is None:
            date_to = date.today()
            
        if date_from is None:
            date_from = date_to

        stmt = (
            select(Report)
            .where(
                Report.report_date.between(
                    date_from,
                    date_to,
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

    async def photos(
        self,
        date_from: date | None = None,
        date_to: date | None = None,
    )
        """
        Export photos for selected date.
        """

        if date_to is None:
            date_to = date.today()

        if date_from is None:
            date_from = date_to

        stmt = (
            select(Report)
            .where(
                Report.report_date.between(
                    date_from,
                    date_to,
                )
            .options(
                selectinload(
                    Report.user
                ),
                selectinload(
                    Report.answers
                )
                .selectinload(
                    Answer.question
                ),
                selectinload(
                    Report.answers
                )
                .selectinload(
                    Answer.photos
                ),
            )
        )

        reports = (
            await self.session.execute(stmt)
        ).scalars().all()

        rows = []

        for report in reports:

            full_name = (
                f"{report.user.first_name} "
                f"{report.user.last_name or ''}"
            ).strip()

            for answer in report.answers:

                for photo in answer.photos:

                    rows.append(
                        {
                            "user": full_name,
                            "question": answer.question.text_ru,
                            "telegram_file_id": photo.telegram_file_id,
                        }
                    )

        return rows
