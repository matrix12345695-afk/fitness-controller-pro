from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.profiles import ProfileRepository


class ProfileService:

    def __init__(
        self,
        session: AsyncSession,
    ):
        self.repository = ProfileRepository(session)

    async def get_profile(
        self,
        user_id: int,
    ):
        return await self.repository.get(user_id)

    async def create_profile(
        self,
        **kwargs,
    ):
        profile = await self.repository.create(
            **kwargs
        )

        await self.repository.commit()

        return profile
