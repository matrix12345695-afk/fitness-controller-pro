from datetime import date

from sqlalchemy import func, select

from app.models.report import Report
from app.models.user import User
from app.repositories.base import BaseRepository


class DashboardRepository(BaseRepository):
    """
    Dashboard repository.
    """

    async def total_users(self) -> int:
        """
        Total registered users.
        """

        stmt = select(
            func.count(User.id)
        )

        result = await self.session.execute(stmt)

        return result.scalar_one()

    async def completed_today(self) -> int:
        """
        Completed reports today.
        """

        stmt = select(
            func.count(Report.id)
        ).where(
            Report.report_date == date.today()
        )

        result = await self.session.execute(stmt)

        return result.scalar_one()

    async def users_today(
        self,
    ):
        """
        Reports for today.
        """

        stmt = (
            select(Report)
            .where(
                Report.report_date == date.today()
            )
            .order_by(
                Report.user_id
            )
        )

        return await self.scalars(stmt)

    async def users_without_report_today(
        self,
    ):
        """
        Users who have not completed today's report.
        """

        today = date.today()

        subquery = (
            select(Report.user_id)
            .where(
                Report.report_date == today
            )
        )

        stmt = (
            select(User)
            .where(
                User.id.not_in(subquery)
            )
            .order_by(
                User.first_name
            )
        )

        return await self.scalars(stmt)

    async def completion_percent(
        self,
    ) -> int:
        """
        Completion percent.
        """

        total = await self.total_users()

        if total == 0:
            return 0

        completed = await self.completed_today()

        return round(
            completed / total * 100
        )

    async def not_completed_today(
        self,
    ) -> int:
        """
        Users without report.
        """

        total = await self.total_users()

        completed = await self.completed_today()

        return max(
            total - completed,
            0,
        )
