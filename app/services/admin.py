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
