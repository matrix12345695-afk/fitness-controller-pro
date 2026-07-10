from app.services.profile import ProfileService


class AccountService:
    """
    User account service.
    """

    def __init__(
        self,
        session,
    ):
        self.profile_service = ProfileService(
            session,
        )

    async def get_account(
        self,
        user_id: int,
    ):
        """
        Get full account information.
        """

        statistics = await self.profile_service.statistics(
            user_id,
        )

        if statistics is None:
            return None

        profile = statistics["profile"]
        reports = statistics["reports"]
        last_report = statistics["last_report"]

        return {
            "full_name": profile.full_name,
            "gender": profile.gender.value,
            "birth_date": profile.birth_date,
            "height": profile.height,
            "start_weight": profile.start_weight,
            "current_weight": getattr(
                profile,
                "current_weight",
                None,
            ),
            "target_weight": getattr(
                profile,
                "target_weight",
                None,
            ),
            "reports": reports,
            "last_report": last_report,
        }
