from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.answer import Answer
from app.models.photo import Photo
from app.models.profile import Profile
from app.models.report import Report
from app.models.user import User


class StatisticsService:
    """
    Statistics service.

    One service for:

    • User profile
    • Dashboard
    • Excel
    • Admin panel
    """

    def __init__(
        self,
        session: AsyncSession,
    ):
        self.session = session

    async def get_user_statistics(
        self,
        telegram_id: int,
    ) -> dict | None:
        """
        Build full statistics for one user.
        """

        stmt = (
            select(
                User,
                Profile,
            )
            .outerjoin(
                Profile,
                Profile.user_id == User.id,
            )
            .where(
                User.telegram_id == telegram_id,
            )
        )

        result = await self.session.execute(
            stmt,
        )

        row = result.first()

        if row is None:
            return None

        user, profile = row

        return {
            "user": user,
            "profile": profile,
        }
    # =====================================================
    # REPORTS
    # =====================================================

    async def count_reports(
        self,
        user_id: int,
    ) -> int:
        """
        Count all reports.
        """

        stmt = (
            select(
                func.count(
                    Report.id,
                )
            )
            .where(
                Report.user_id == user_id,
            )
        )

        result = await self.session.execute(
            stmt,
        )

        return result.scalar_one() or 0

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

        result = await self.session.execute(
            stmt,
        )

        return result.scalar_one_or_none()

    # =====================================================
    # ANSWERS
    # =====================================================

    async def count_answers(
        self,
        user_id: int,
    ) -> int:
        """
        Count all answers.
        """

        stmt = (
            select(
                func.count(
                    Answer.id,
                )
            )
            .join(
                Report,
                Report.id == Answer.report_id,
            )
            .where(
                Report.user_id == user_id,
            )
        )

        result = await self.session.execute(
            stmt,
        )

        return result.scalar_one() or 0

    # =====================================================
    # PHOTOS
    # =====================================================

    async def count_photos(
        self,
        user_id: int,
    ) -> int:
        """
        Count all uploaded photos.
        """

        stmt = (
            select(
                func.count(
                    Photo.id,
                )
            )
            .join(
                Answer,
                Answer.id == Photo.answer_id,
            )
            .join(
                Report,
                Report.id == Answer.report_id,
            )
            .where(
                Report.user_id == user_id,
            )
        )

        result = await self.session.execute(
            stmt,
        )

        return result.scalar_one() or 0
    # =====================================================
    # BUILD STATISTICS
    # =====================================================

    async def build_statistics(
        self,
        telegram_id: int,
    ) -> dict | None:
        """
        Build full statistics for user.
        """

        data = await self.get_user_statistics(
            telegram_id,
        )

        if data is None:
            return None

        user = data["user"]
        profile = data["profile"]

        reports = await self.count_reports(
            user.id,
        )

        answers = await self.count_answers(
            user.id,
        )

        photos = await self.count_photos(
            user.id,
        )

        last_report = await self.last_report(
            user.id,
        )

        start_weight = None
        current_weight = None
        difference = None

        if profile:

            start_weight = profile.start_weight

            current_weight = profile.start_weight

            difference = 0

        completion = 0

        if reports:

            completion = round(
                (
                    answers
                    / (reports * 9)
                )
                * 100,
                1,
            )

        return {
            "user": user,
            "profile": profile,
            "reports": reports,
            "answers": answers,
            "photos": photos,
            "completion": completion,
            "last_report": last_report,
            "start_weight": start_weight,
            "current_weight": current_weight,
            "difference": difference,
        }
      
