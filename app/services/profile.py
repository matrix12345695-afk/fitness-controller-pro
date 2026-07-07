from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.profiles import ProfileRepository


class ProfileService:

    def __init__(
        self,
        session: AsyncSession,
    ):
        self.profiles = ProfileRepository(session)

    async def get_profile(
        self,
        user_id: int,
    ):
        return await self.profiles.get(user_id)
