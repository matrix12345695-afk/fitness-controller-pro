from app.repositories.profiles import ProfileRepository
from app.services.base import BaseService


class ProfileService(BaseService):
    """
    Profile service.
    """

    def __init__(self, session):
        super().__init__(session)

        self.repository = ProfileRepository(session)

    async def get(
        self,
        user_id: int,
    ):
        return await self.repository.get(
            user_id
        )

    async def update_weight(
        self,
        profile,
        weight: float,
    ):

        return await self.repository.update_weight(
            profile,
            weight,
        )
