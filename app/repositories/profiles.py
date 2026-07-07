from sqlalchemy import select

from app.models.profile import Profile
from app.repositories.base import BaseRepository


class ProfileRepository(BaseRepository):

    async def get(
        self,
        user_id: int,
    ) -> Profile | None:

        stmt = select(Profile).where(
            Profile.user_id == user_id
        )

        return await self.scalar(stmt)

    async def create(
        self,
        **kwargs,
    ) -> Profile:

        profile = Profile(**kwargs)

        return await self.add(profile)
