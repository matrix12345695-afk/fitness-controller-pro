from sqlalchemy.ext.asyncio import AsyncSession

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
        Total users count.
        """

        return await self.users.count()

    # ==========================================================
    # DASHBOARD
    # ==========================================================

    async def dashboard(
        self,
    ) -> dict:
        """
        Dashboard data.
        """

        total = await self.total_users()

        return {
            "total_users": total,
            "completed_today": 0,
            "not_completed_today": total,
            "completion_percent": 0,
        }
