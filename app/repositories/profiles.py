from sqlalchemy import select

from app.models.profile import Profile
from app.repositories.base import BaseRepository


class ProfileRepository(
    BaseRepository[Profile]
):
    """
    Repository for Profile model.
    """

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
        user_id: int,
        full_name: str,
        gender,
        birth_date,
        height: int,
        start_weight: float,
    ) -> Profile:

        profile = Profile(
            user_id=user_id,
            full_name=full_name,
            gender=gender,
            birth_date=birth_date,
            height=height,
            start_weight=start_weight,
        )

        return await self.add(profile)

    async def update_weight(
        self,
        profile: Profile,
        weight: float,
    ) -> Profile:

        profile.start_weight = weight

        await self.commit()

        return profile
