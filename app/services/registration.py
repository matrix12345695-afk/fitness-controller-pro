from app.enums import Language
from app.repositories.profiles import ProfileRepository
from app.repositories.users import UserRepository
from app.schemas.profile import ProfileCreate
from app.schemas.user import UserCreate
from app.services.base import BaseService


class RegistrationService(BaseService):
    """
    Registration business logic.
    """

    def __init__(self, session):
        super().__init__(session)

        self.users = UserRepository(session)
        self.profiles = ProfileRepository(session)

    async def get_user(
        self,
        telegram_id: int,
    ):
        return await self.users.get_by_telegram_id(
            telegram_id
        )

    async def user_exists(
        self,
        telegram_id: int,
    ) -> bool:

        user = await self.get_user(
            telegram_id
        )

        return user is not None

    async def create_user(
        self,
        user_data: UserCreate,
        language: Language,
    ):

        user = await self.users.create(
            telegram_id=user_data.telegram_id,
            username=user_data.username,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
        )

        user.language = language

        await self.users.commit()

        return user

    async def create_profile(
        self,
        user_id: int,
        profile: ProfileCreate,
    ):

        profile = await self.profiles.create(
            user_id=user_id,
            full_name=profile.full_name,
            gender=profile.gender,
            birth_date=profile.birth_date,
            height=profile.height,
            start_weight=profile.start_weight,
        )

        await self.profiles.commit()

        return profile

    async def finish_registration(
        self,
        user_id: int,
        profile: ProfileCreate,
    ):

        return await self.create_profile(
            user_id,
            profile,
        )
