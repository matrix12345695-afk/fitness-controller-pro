from sqlalchemy import select

from app.models.user import User
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    """
    Repository for User model.
    """

    async def get(
        self,
        user_id: int,
    ) -> User | None:

        stmt = select(User).where(
            User.id == user_id
        )

        return await self.scalar(stmt)

    async def get_by_telegram_id(
        self,
        telegram_id: int,
    ) -> User | None:

        stmt = select(User).where(
            User.telegram_id == telegram_id
        )

        return await self.scalar(stmt)

    async def create(
        self,
        telegram_id: int,
        username: str | None,
        first_name: str,
        last_name: str | None,
    ) -> User:

        user = User(
            telegram_id=telegram_id,
            username=username,
            first_name=first_name,
            last_name=last_name,
        )

        return await self.add(user)

    async def get_all(self):

        stmt = (
            select(User)
            .order_by(User.id)
        )

        return await self.scalars(stmt)

    async def deactivate(
        self,
        user: User,
    ) -> User:

        user.is_active = False

        await self.commit()

        return user
