from sqlalchemy import func, select

from app.models.profile import Profile
from app.models.report import Report
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

        stmt = select(
            Profile,
        ).where(
            Profile.user_id == user_id,
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

        return await self.add(
            profile,
        )

    async def update_weight(
        self,
        profile: Profile,
        weight: float,
    ) -> Profile:
        """
        Update current weight.
        """

        profile.start_weight = weight

        await self.commit()

        return profile

    async def count_reports(
        self,
        user_id: int,
    ) -> int:
        """
        Count completed reports.
        """

        stmt = select(
            func.count(
                Report.id,
            )
        ).where(
            Report.user_id == user_id,
        )

        result = await self.session.execute(
            stmt,
        )

        return result.scalar_one()

    async def last_report(
        self,
        user_id: int,
    ) -> Report | None:
        """
        Get latest report.
        """

        stmt = (
            select(
                Report,
            )
            .where(
                Report.user_id == user_id,
            )
            .order_by(
                Report.created_at.desc(),
            )
            .limit(1)
        )

        return await self.scalar(
            stmt,
        )
