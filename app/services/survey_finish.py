from sqlalchemy.ext.asyncio import AsyncSession

from app.core.bot import bot
from app.core.config import settings
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

        # ==========================================================
        # GROUP NOTIFICATION
        # ==========================================================

        try:

            full_name = report.user.first_name or "Без имени"

            if report.user.last_name:
                full_name += f" {report.user.last_name}"

            await bot.send_message(
                chat_id=settings.group_id,
                text=(
                    "━━━━━━━━━━━━━━━\n\n"
                    "✅ <b>Новый отчёт</b>\n\n"
                    f"👤 {full_name}\n\n"
                    f"📅 {report.report_date.strftime('%d.%m.%Y')}\n"
                    "💪 Отчёт успешно завершён\n\n"
                    "━━━━━━━━━━━━━━━"
                ),
                parse_mode="HTML",
            )

        except Exception:
            pass

        return {
            "success": True,
            "report": report,
        }
