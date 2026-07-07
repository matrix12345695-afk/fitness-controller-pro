from sqlalchemy.ext.asyncio import AsyncSession

from app.enums import Language
from app.repositories.profiles import ProfileRepository
from app.repositories.users import UserRepository
from app.schemas.profile import ProfileCreate
from app.schemas.user import UserCreate


class RegistrationService:
    """
    User registration service.
    """

    def __init__(self, session: AsyncSession):
        self.session = session

        self.users = UserRepository(session)
        self.profiles = ProfileRepository(session)

    async def is_registered(
        self,
        telegram_id: int,
    ) -> bool:
        """
        Check if user already exists.
        """

        user = await self.users.get_by_telegram_id(
            telegram_id
        )

        return user is not None

    async def register_user(
        self,
        user_data: UserCreate,
        language: Language,
    ):
        """
        Create telegram user.
        """

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
        """
        Create profile.
        """

        obj = await self.profiles.create(
            user_id=user_id,
            full_name=profile.full_name,
            gender=profile.gender,
            birth_date=profile.birth_date,
            height=profile.height,
            start_weight=profile.start_weight,
        )

        await self.profiles.commit()

        return obj
