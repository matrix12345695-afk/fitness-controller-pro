from app.models.profile import Profile
from app.repositories.profiles import ProfileRepository


class ProfileService:
    """
    Service for user profile.
    """

    def __init__(
        self,
        session,
    ):
        self.repository = ProfileRepository(
            session,
        )

    async def get(
        self,
        user_id: int,
    ) -> Profile | None:
        """
        Get user profile.
        """

        return await self.repository.get(
            user_id,
        )

    async def create(
        self,
        user_id: int,
        full_name: str,
        gender,
        birth_date,
        height: int,
        start_weight: float,
    ) -> Profile:
        """
        Create profile.
        """

        return await self.repository.create(
            user_id=user_id,
            full_name=full_name,
            gender=gender,
            birth_date=birth_date,
            height=height,
            start_weight=start_weight,
        )

    async def update_weight(
        self,
        user_id: int,
        weight: float,
    ) -> Profile | None:
        """
        Update user weight.
        """

        profile = await self.repository.get(
            user_id,
        )

        if profile is None:
            return None

        return await self.repository.update_weight(
            profile,
            weight,
        )

    async def statistics(
        self,
        user_id: int,
    ) -> dict | None:
        """
        Get profile statistics.
        """

        profile = await self.repository.get(
            user_id,
        )

        if profile is None:
            return None

        reports = await self.repository.count_reports(
            user_id,
        )

        last_report = await self.repository.last_report(
            user_id,
        )

        return {
            "profile": profile,
            "reports": reports,
            "last_report": last_report,
        }
