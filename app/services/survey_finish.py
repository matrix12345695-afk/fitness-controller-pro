from sqlalchemy.ext.asyncio import AsyncSession

from app.enums import ReportStatus
from app.repositories.reports import ReportRepository


class SurveyFinishService:
    """
    Finish daily survey.
    """

    def __init__(
        self,
        session: AsyncSession,
    ):
        self.session = session
        self.reports = ReportRepository(session)

    async def execute(
        self,
        report_id: int,
    ) -> dict:
        """
        Complete survey report.
        """

        report = await self.reports.get(
            report_id,
        )

        if report is None:
            return {
                "success": False,
                "error": "Report not found.",
            }

        report.status = ReportStatus.COMPLETED

        await self.session.commit()

        await self.session.refresh(report)

        return {
            "success": True,
            "report": report,
        }
