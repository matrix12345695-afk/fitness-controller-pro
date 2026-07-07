from datetime import date

from sqlalchemy import desc, select

from app.models.report import Report
from app.repositories.base import BaseRepository


class ReportRepository(BaseRepository[Report]):
    """
    Repository for daily reports.
    """

    async def get(
        self,
        report_id: int,
    ) -> Report | None:

        stmt = select(Report).where(
            Report.id == report_id
        )

        return await self.scalar(stmt)

    async def create(
        self,
        user_id: int,
        report_date: date,
        status,
    ) -> Report:

        report = Report(
            user_id=user_id,
            report_date=report_date,
            status=status,
        )

        return await self.add(report)

    async def get_by_user_and_date(
        self,
        user_id: int,
        report_date: date,
    ) -> Report | None:

        stmt = select(Report).where(
            Report.user_id == user_id,
            Report.report_date == report_date,
        )

        return await self.scalar(stmt)

    async def get_today(
        self,
        user_id: int,
    ) -> Report | None:

        today = date.today()

        return await self.get_by_user_and_date(
            user_id=user_id,
            report_date=today,
        )

    async def get_user_reports(
        self,
        user_id: int,
    ) -> list[Report]:

        stmt = (
            select(Report)
            .where(
                Report.user_id == user_id
            )
            .order_by(
                desc(Report.report_date)
            )
        )

        return await self.scalars(stmt)

    async def get_reports_by_date(
        self,
        report_date: date,
    ) -> list[Report]:

        stmt = (
            select(Report)
            .where(
                Report.report_date == report_date
            )
            .order_by(
                Report.user_id
            )
        )

        return await self.scalars(stmt)

    async def set_status(
        self,
        report: Report,
        status,
    ) -> Report:

        report.status = status

        await self.commit()

        return report

    async def delete_report(
        self,
        report: Report,
    ) -> None:

        await self.delete(report)

        await self.commit()
