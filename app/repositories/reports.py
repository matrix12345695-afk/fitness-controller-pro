from datetime import date

from sqlalchemy import select

from app.models.report import Report
from app.repositories.base import BaseRepository


class ReportRepository(BaseRepository):

    async def get_today(
        self,
        user_id: int,
        report_date: date,
    ) -> Report | None:

        stmt = select(Report).where(
            Report.user_id == user_id,
            Report.report_date == report_date,
        )

        return await self.scalar(stmt)

    async def create(
        self,
        user_id: int,
        report_date: date,
    ) -> Report:

        report = Report(
            user_id=user_id,
            report_date=report_date,
        )

        return await self.add(report)
