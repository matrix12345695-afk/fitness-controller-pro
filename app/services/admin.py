from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.dashboard import DashboardRepository
from app.repositories.users import UserRepository


class AdminService:
    """
    Admin service.
    """

    def __init__(
        self,
        session: AsyncSession,
    ):
        self.session = session

        self.users = UserRepository(
            session,
        )

        self.dashboard = DashboardRepository(
            session,
        )

    # ==========================================================
    # USERS
    # ==========================================================

    async def get_users(
        self,
    ):
        """
        Get all users.
        """

        return await self.users.get_all()

    async def get_user(
        self,
        user_id: int,
    ):
        """
        Get user by id.
        """

        return await self.users.get(
            user_id,
        )

    async def total_users(
        self,
    ) -> int:
        """
        Total users.
        """

        return await self.dashboard.total_users()

    # ==========================================================
    # DASHBOARD
    # ==========================================================

    async def dashboard_stats(
        self,
    ) -> dict:
        """
        Dashboard statistics.
        """

        return {
            "total_users": await self.dashboard.total_users(),
            "completed_today": await self.dashboard.completed_today(),
            "not_completed_today": await self.dashboard.not_completed_today(),
            "completion_percent": await self.dashboard.completion_percent(),
        }

    async def reports_today(
        self,
    ):
        """
        Reports for today.
        """

        return await self.dashboard.users_today()

    async def users_without_report_today(self):
        """
        Users without today's report.
        """

        return await self.dashboard.users_without_report_today()
